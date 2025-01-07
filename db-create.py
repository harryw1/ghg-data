import sqlite3

# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect("emissions_facility.db")
cursor = conn.cursor()

# Create the emissions table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS emissions (
        co2e_emission REAL,
        facility_id INTEGER,
        gas_id INTEGER,
        sub_part_id INTEGER,
        year INTEGER,
        FOREIGN KEY (facility_id) REFERENCES facility (facility_id)
    )
"""
)

# Create the facility table
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS facility (
        address1 TEXT,
        address2 TEXT,
        bamm_approved TEXT,
        bamm_used_desc TEXT,
        cems_used TEXT,
        city TEXT,
        co2_captured TEXT,
        comments TEXT,
        county TEXT,
        county_fips TEXT,
        eggrt_facility_id INTEGER,
        emission_classification_code TEXT,
        emitted_co2_supplied TEXT,
        facility_id INTEGER,
        facility_name TEXT,
        facility_types TEXT,
        frs_id TEXT,
        latitude REAL,
        longitude REAL,
        naics_code TEXT,
        parent_company TEXT,
        process_stationary_cml TEXT,
        program_name TEXT,
        program_sys_id TEXT,
        reported_industry_types TEXT,
        reported_subparts TEXT,
        reporting_status TEXT,
        rr_monitoring_plan TEXT,
        rr_monitoring_plan_filename TEXT,
        rr_mrv_plan_url TEXT,
        state TEXT,
        state_name TEXT,
        submission_id INTEGER,
        tribal_land_id TEXT,
        uu_rd_exempt TEXT,
        year INTEGER,
        zip TEXT,
        PRIMARY KEY (facility_id, year)
    )
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS c_subpart (
        facility_id INTEGER,
        facility_name TEXT,
        ghg_gas_name TEXT,
        ghg_quantity REAL,
        reporting_year INTEGER,
        FOREIGN KEY (facility_id, reporting_year) REFERENCES facility (facility_id, year)
    )
"""
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS d_subpart (
        facility_id INTEGER,
        facility_name TEXT,
        ghg_name TEXT,
        ghg_quantity REAL,
        reporting_year INTEGER,
        FOREIGN KEY (facility_id) REFERENCES facility (facility_id)
    )
"""
)

# Commit the changes and close the connection
conn.commit()
conn.close()
