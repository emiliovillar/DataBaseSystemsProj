# setup.py
import pandas as pd
import sqlite3
import database as db  # This imports your database.py file

def load_data():
    """Reads the CSV and populates the 4 database tables."""
    
    # 1. Create the database and tables
    db.create_tables()
    
    # 2. Read your clean data file
    df = pd.read_csv('final_project_data.csv')
    
    # 3. Connect to the DB
    conn = db.get_db()
    cursor = conn.cursor()
    
    # 4. Iterate and Insert row by row
    for index, row in df.iterrows():
        try:
            # We need to get the county name (not in your file, so we'll just use fips for now)
            # A real app would get this from another source, but this is fine.
            county_name = f"County {row['fips']}"
            state_abbr = "N/A" # Same as above
            
            # Insert into Counties table
            cursor.execute(
                "INSERT OR IGNORE INTO Counties (fips, county_name, state_abbr) VALUES (?, ?, ?)",
                (row['fips'], county_name, state_abbr)
            )
            
            # Insert into Demographics table
            cursor.execute(
                """INSERT INTO Demographics (fips, pop_total, pop_white, pop_black, pop_hispanic, income_median_household) 
                   VALUES (?, ?, ?, ?, ?, ?)""",
                (row['fips'], row['pop_total'], row['pop_white'], row['pop_black'], row['pop_hispanic'], row['income_median_household'])
            )
            
            # Insert into Housing table
            cursor.execute(
                "INSERT INTO Housing (fips, rent_median_gross, rent_burdened_pct) VALUES (?, ?, ?)",
                (row['fips'], row['rent_median_gross'], row['rent_burdened_pct'])
            )
            
            # Insert into Evictions table
            cursor.execute(
                "INSERT INTO Evictions (fips, evict_year, evict_filings) VALUES (?, ?, ?)",
                (row['fips'], row['evict_year'], row['evict_filings'])
            )
        
        except Exception as e:
            print(f"Error inserting row {index} for fips {row['fips']}: {e}")
            
    conn.commit()
    conn.close()
    print("Data has been successfully loaded into the database.")

if __name__ == "__main__":
    load_data()