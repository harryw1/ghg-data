import sqlite3

import requests_cache


def query_info():
    """
    Asks the user for a target year and returns it.
    """
    while True:
        try:
            year = int(input("Enter a year: "))
            if year < 1970 or year > 2023:
                print("Please enter a year between 1970 and 2023.")
                exit(1)
            break
        except ValueError:
            print("Please enter a valid year.")
            exit(1)
    return year


def get_data_facility_emissions(year):
    """
    Fetches data from the EPA API and stores it in an list of dictionaries.
    """
    print("Fetching emissions data...")
    session = requests_cache.CachedSession("emissions_cache")
    url = f"https://data.epa.gov/dmapservice/ghg.pub_facts_subp_ghg_emission/year/equals/{year}"
    response = session.get(url)
    data = response.json()
    return data


def get_data_facility_info(year):
    """
    Fetches data from the EPA API and stores it in an list of dictionaries.
    """
    print("Fetching facility data...")
    session = requests_cache.CachedSession("facility_cache")
    url = f"https://data.epa.gov/dmapservice/ghg.pub_dim_facility/year/equals/{year}"
    response = session.get(url)
    data = response.json()
    return data


def get_c_subpart_data(year):
    """
    Fetches data from the EPA API and stores it in an list of dictionaries.
    """
    print("Fetching C subpart data...")
    session = requests_cache.CachedSession("c_subpart_cache")
    url = f"https://data.epa.gov/dmapservice/ghg.c_subpart_level_information/reporting_year/equals/{year}"
    response = session.get(url)
    data = response.json()
    return data


def get_d_subpart_data(year):
    """
    Fetches data from the EPA API and stores it in an list of dictionaries.
    """
    print("Fetching D subpart data...")
    session = requests_cache.CachedSession("d_subpart_cache")
    url = f"https://data.epa.gov/dmapservice/ghg.d_subpart_level_information/reporting_year/equals/{year}"
    response = session.get(url)
    data = response.json()
    return data


def insert_data_from_list(data, table_name):
    """
    Inserts data from a list of dictionaries into an SQLite table.
    """
    conn = sqlite3.connect("emissions_facility.db")
    cursor = conn.cursor()

    for row in data:
        columns = ", ".join(row.keys())
        placeholders = ", ".join("?" * len(row))
        sql = f"""
            INSERT OR REPLACE INTO {table_name} ({columns})
            VALUES ({placeholders})
        """
        cursor.execute(sql, tuple(row.values()))

    conn.commit()
    conn.close()


def main():
    year = query_info()
    emissions_data = get_data_facility_emissions(year)
    insert_data_from_list(emissions_data, "emissions")
    facility_data = get_data_facility_info(year)
    insert_data_from_list(facility_data, "facility")
    c_subpart_data = get_c_subpart_data(year)
    insert_data_from_list(c_subpart_data, "c_subpart")
    d_subpart_data = get_d_subpart_data(year)
    insert_data_from_list(d_subpart_data, "d_subpart")


if __name__ == "__main__":
    main()
