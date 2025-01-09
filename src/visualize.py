import os
import sqlite3

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


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


def check_db():
    # Checks if the database exists and returns True if it does, otherwise exits the program.
    if not os.path.exists("../emissions_facility.db"):
        print(
            "Database does not exist. Please run db-create.py to create the database."
        )
        exit(1)
    conn = sqlite3.connect("../emissions_facility.db")
    cursor = conn.cursor()
    if not cursor.execute("SELECT * FROM emissions").fetchall():
        print("Database is empty. Please run db-populate.py to populate the database.")
        exit(1)
    return True


def load_data_facility_emissions():
    # Load data from populated database and return it as a pandas DataFrame.
    if check_db():
        conn = sqlite3.connect("../emissions_facility.db")
        emissions = pd.read_sql_query("SELECT * FROM emissions", conn)
        facility = pd.read_sql_query("SELECT * FROM facility", conn)
        return emissions, facility


def summarize_data(frame_a, frame_b):
    # Summarize data from two DataFrames and return the summary.
    print("Summarizing data...")
    print("Emissions data:")
    print(frame_a.describe())
    print("Facility data:")
    print(frame_b.describe())


def total_emissions_by_year(frame_a, frame_b, year):
    merged = merge_frames(frame_a, frame_b)
    total_emissions = merged.groupby(["facility_id", "year_y", "gas_id"]).sum()
    return total_emissions


def visualize_data(frame_a, frame_b, year):
    merged = merge_frames(frame_a, frame_b)
    merged = merged.drop(
        merged[
            (merged.gas_id != 1) & (merged.gas_id != 2) & (merged.gas_id != 3)
            | (merged.year_y != year)
        ].index
    )
    sns.set_theme(style="whitegrid")
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
    plt.show()


def merge_frames(frame_a, frame_b):
    return pd.merge(frame_a, frame_b, on="facility_id")


def main():
    check_db()
    emissions, facility = load_data_facility_emissions()
    summarize_data(emissions, facility)
    year = query_info()
    total_emissions = total_emissions_by_year(emissions, facility, year)
    print(total_emissions)
    visualize_data(emissions, facility, year)


if __name__ == "__main__":
    main()
