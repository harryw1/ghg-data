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


def get_data(year):
    """
    Fetches data from the EPA API and stores it in an list of dictionaries.
    """
    url = f"https://data.epa.gov/dmapservice/ghg.pub_facts_subp_ghg_emission/year/equals/{year}"
    response = requests.get(url)
    data = response.json()
    return data


def main():
    year = query_info()
    data = get_data(year)
    print(data)


if __name__ == "__main__":
    main()
