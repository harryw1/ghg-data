import os
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def query_info():
    """
    Asks the user for a target year and returns it.

    Args:
        None

    Returns:
        int: The target year chosen by the user.

    Raises:
        ValueError: If the user enters an invalid year.
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


def check_db():
    """
    Checks if the database exists and returns True if it does, otherwise exits.

    Args:
        None

    Returns:
        bool: Whether the database exists or not.
    """

    # Check if database exists
    if not os.path.exists("../emissions_facility.db"):
        print(
            "Database does not exist. Please run db-create.py to create the database."
        )
        exit(1)

    # Connect to database and execute query
    conn = sqlite3.connect("../emissions_facility.db")
    cursor = conn.cursor()
    if not cursor.execute("SELECT * FROM emissions").fetchall():
        print("Database is empty. Please run db-populate.py to populate the database.")
        exit(1)

    # Return True if database exists
    return True


def load_data_facility_emissions():
    """
    Loads data from populated database and returns it as a pandas DataFrame.

    Args:
        None

    Returns:
        tuple: A tuple containing two DataFrames, 'emissions' and 'facility'.
    """

    # Check if database exists
    if check_db():
        # Connect to database
        conn = sqlite3.connect("../emissions_facility.db")

        # Load data from database
        emissions = pd.read_sql_query("SELECT * FROM emissions", conn)
        facility = pd.read_sql_query("SELECT * FROM facility", conn)

        # Return DataFrames
        return emissions, facility


def summarize_data(frame_a, frame_b):
    """
    Summarizes data from two DataFrames and returns the summary.

    Args:
        frame_a (DataFrame): The first DataFrame to summarize.
        frame_b (DataFrame): The second DataFrame to summarize.

    Returns:
        None
    """

    print("Summarizing data...")
    print("Emissions data:")
    print(frame_a.describe())
    print("Facility data:")
    print(frame_b.describe())


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

    # Merge DataFrames
    merged = merge_frames(frame_a, frame_b)

    # Calculate total emissions
    total_emissions = merged.groupby(["facility_id", "year_y", "gas_id"]).sum()

    # Return total emissions
    return total_emissions


def visualize_data(frame_a, frame_b, year):
    """
    Visualizes the data for a given year.

    Args:
        frame_a (DataFrame): The DataFrame containing the emissions data.
        frame_b (DataFrame): The DataFrame containing the facility data.
        year (int): The target year to visualize data for.

    Returns:
        None
    """

    # Merge DataFrames
    merged = merge_frames(frame_a, frame_b)

    # Drop unnecessary rows from merged DataFrame
    merged = merged.drop(
        merged[
            (merged.gas_id != 1) & (merged.gas_id != 2) & (merged.gas_id != 3)
            | (merged.year_y != year)
        ].index
    )

    # Set matplotlib theme
    sns.set_theme(style="whitegrid")

    # Create histogram
    sns.histplot(
        merged,
        x="year_y",
        y="co2e_emission",
        bins=30,
        discrete=(True, False),
        log_scale=(False, True),
        cbar=True,
        cbar_kws=dict(shrink=0.75),
    )

    # Display histogram
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

    # Merge DataFrames
    return pd.merge(frame_a, frame_b, on="facility_id")


def main():
    """
    Main function that runs the program.

    Args:
        None

    Returns:
        None
    """

    # Check if database exists
    check_db()

    # Load data from populated database
    emissions, facility = load_data_facility_emissions()

    # Summarize data
    summarize_data(emissions, facility)

    # Ask user for target year
    year = query_info()

    # Calculate total emissions by year
    total_emissions = total_emissions_by_year(emissions, facility, year)

    # Print total emissions
    print(total_emissions)

    # Visualize data for given year
    visualize_data(emissions, facility, year)


if __name__ == "__main__":
    main()
