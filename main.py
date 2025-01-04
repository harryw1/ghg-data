import pandas as pd
import requests


def query_info():
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
    url = f"https://data.epa.gov/dmapservice/ghg.pub_facts_subp_ghg_emission/year/equals/{year}"
    response = requests.get(url)
    data = response.json()
    return data


def get_data_facility_info(year):
    """
    Fetches data from the EPA API and stores it in an list of dictionaries.
    """
    url = f"https://data.epa.gov/dmapservice/ghg.pub_dim_facility/year/equals/{year}"
    response = requests.get(url)
    data = response.json()
    return data


def data_to_df(data):
    df = pd.DataFrame(data)
    return df


def main():
    year = query_info()
    emissions_data = get_data_facility_emissions(year)
    facility_data = get_data_facility_info(year)
    em_df = data_to_df(emissions_data)
    fac_df = data_to_df(facility_data)
    print(em_df)
    print(fac_df)


if __name__ == "__main__":
    main()
