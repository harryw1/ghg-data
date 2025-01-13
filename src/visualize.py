import os
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def query_info():
    """
    Asks the user for a target year and returns it.

    Returns:
        int: The target year chosen by the user.

    Raises:
        ValueError: If the user enters an invalid year.
    """

    def is_valid_year(year):
        return 1970 <= year <= 2023

    while True:
        try:
            year = int(input("Enter a year: "))
            if not is_valid_year(year):
                print("Please enter a year between 1970 and 2023.")
                exit(1)
            return year
        except ValueError:
            print("Please enter a valid year.")
            exit(1)


def check_db():
    """
    Checks if the database exists and returns True if it does, otherwise exits.

    Returns:
        bool: Whether the database exists or not.
    """

    def db_exists():
        return os.path.exists("../emissions_facility.db")

    def db_not_empty(cursor):
        return bool(cursor.execute("SELECT * FROM emissions").fetchall())

    if not db_exists():
        print(
            "Database does not exist. Please run db-create.py to create the database."
        )
        exit(1)

    conn = sqlite3.connect("../emissions_facility.db")
    cursor = conn.cursor()
    if not db_not_empty(cursor):
        print("Database is empty. Please run db-populate.py to populate the database.")
        exit(1)

    return True


def load_data_facility_emissions():
    """
    Loads data from populated database and returns it as a pandas DataFrame.

    Returns:
        tuple: A tuple containing two DataFrames, 'emissions' and 'facility'.
    """

    def load_data_from_db():
        conn = sqlite3.connect("../emissions_facility.db")
        emissions = pd.read_sql_query("SELECT * FROM emissions", conn)
        facility = pd.read_sql_query("SELECT * FROM facility", conn)
        return emissions, facility

    if check_db():
        return load_data_from_db()


def summarize_data(frame_a, frame_b):
    """
    Summarizes data from two DataFrames and returns the summary.

    Args:
        frame_a (DataFrame): The first DataFrame to summarize.
        frame_b (DataFrame): The second DataFrame to summarize.
    """

    def print_summary(frame, name):
        print(f"{name} data:")
        print(frame.describe())

    print("Summarizing data...")
    print_summary(frame_a, "Emissions")
    print_summary(frame_b, "Facility")


def total_emissions_by_year(frame_a, frame_b, year):
    """
    Calculates the total emissions for a given year.

    Args:
        frame_a (DataFrame): The DataFrame containing the emissions data.
        frame_b (DataFrame): The DataFrame containing the facility data.
        year (int): The target year to calculate emissions for.

    Returns:
        DataFrame: A DataFrame containing the total emissions by facility, year and gas.
    """
    merged = merge_frames(frame_a, frame_b)
    total_emissions = merged.groupby(["facility_id", "year_y", "gas_id"]).sum()
    return total_emissions


def visualize_data(frame_a, frame_b, year):
    """
    Visualizes the data for a given year.

    Args:
        frame_a (DataFrame): The DataFrame containing the emissions data.
        frame_b (DataFrame): The DataFrame containing the facility data.
        year (int): The target year to visualize data for.
    """

    def map_state_to_region(state, regions):
        return next(
            (region for region, states in regions.items() if state in states), "Other"
        )

    merged = merge_frames(frame_a, frame_b)
    merged = merged.drop(
        merged[
            (merged.gas_id != 1) & (merged.gas_id != 2) & (merged.gas_id != 3)
            | (merged.year_y != year)
        ].index
    )
    print(merged.info())

    regions = {
        "Northeast": ["CT", "ME", "MA", "NH", "RI", "VT", "NJ", "NY", "PA"],
        "Midwest": [
            "IL",
            "IN",
            "IA",
            "KS",
            "MI",
            "MN",
            "MO",
            "NE",
            "ND",
            "OH",
            "SD",
            "WI",
        ],
        "South": [
            "DE",
            "FL",
            "GA",
            "MD",
            "NC",
            "SC",
            "VA",
            "DC",
            "WV",
            "AL",
            "KY",
            "MS",
            "TN",
            "AR",
            "LA",
            "OK",
            "TX",
        ],
        "West": [
            "AZ",
            "CO",
            "ID",
            "MT",
            "NV",
            "NM",
            "UT",
            "WY",
            "AK",
            "CA",
            "HI",
            "OR",
            "WA",
        ],
    }

    merged["region"] = merged["state"].map(lambda x: map_state_to_region(x, regions))
    aggregated_data = merged.groupby(["region"])["co2e_emission"].sum().reset_index()
    aggregated_data = aggregated_data[aggregated_data.region != "Other"]

    sns.set_theme(style="whitegrid")
    sns.barplot(data=aggregated_data, x="region", y="co2e_emission")
    plt.show()


def merge_frames(frame_a, frame_b):
    """
    Merges two DataFrames on the 'facility_id' column.

    Args:
        frame_a (DataFrame): The first DataFrame to merge.
        frame_b (DataFrame): The second DataFrame to merge.

    Returns:
        DataFrame: The merged DataFrame.
    """
    return pd.merge(frame_a, frame_b, on="facility_id")


def main():
    """
    Main function that runs the program.
    """
    check_db()
    emissions, facility = load_data_facility_emissions()
    summarize_data(emissions, facility)
    year = query_info()
    total_emissions = total_emissions_by_year(emissions, facility, year)
    print(total_emissions)
    visualize_data(emissions, facility, year)


if __name__ == "__main__":
    main()
