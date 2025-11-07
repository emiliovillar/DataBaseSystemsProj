# database.py
import sqlite3

DB_NAME = 'project.db'

def get_db():
    """Connects to the SQLite database."""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row  # Allows you to access columns by name
    return conn

def create_tables():
    """Creates the 4 database tables one time."""
    conn = get_db()
    cursor = conn.cursor()
    
    # 1. Counties (The "Hub" Table)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Counties (
        fips INTEGER PRIMARY KEY,
        county_name TEXT,
        state_abbr TEXT
    );
    """)
    
    # 2. Demographics Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Demographics (
        demo_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fips INTEGER NOT NULL,
        pop_total INTEGER,
        pop_white INTEGER,
        pop_black INTEGER,
        pop_hispanic INTEGER,
        income_median_household REAL,
        FOREIGN KEY (fips) REFERENCES Counties (fips)
    );
    """)
    
    # 3. Housing Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Housing (
        housing_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fips INTEGER NOT NULL,
        rent_median_gross REAL,
        rent_burdened_pct REAL,
        FOREIGN KEY (fips) REFERENCES Counties (fips)
    );
    """)
    
    # 4. Evictions Table (This is what we'll do CRUD on)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Evictions (
        eviction_id INTEGER PRIMARY KEY AUTOINCREMENT,
        fips INTEGER NOT NULL,
        evict_year INTEGER,
        evict_filings INTEGER,
        FOREIGN KEY (fips) REFERENCES Counties (fips)
    );
    """)
    
    conn.commit()
    conn.close()
    print("Database and tables created successfully.")

# --- FULL CRUD PATH FOR 'Evictions' (Week 2 Requirement) ---

# CREATE
def add_eviction_record(fips, year, filings):
    conn = get_db()
    conn.execute(
        "INSERT INTO Evictions (fips, evict_year, evict_filings) VALUES (?, ?, ?)",
        (fips, year, filings)
    )
    conn.commit()
    conn.close()

# READ
def get_all_eviction_records():
    conn = get_db()
    # We JOIN with Counties to get the human-readable county name
    records = conn.execute("""
        SELECT e.eviction_id, e.fips, c.county_name, e.evict_year, e.evict_filings
        FROM Evictions e
        JOIN Counties c ON e.fips = c.fips
        ORDER BY e.evict_filings DESC
    """).fetchall()
    conn.close()
    return records

# UPDATE
def update_eviction_record(eviction_id, fips, year, filings):
    conn = get_db()
    conn.execute(
        "UPDATE Evictions SET fips = ?, evict_year = ?, evict_filings = ? WHERE eviction_id = ?",
        (fips, year, filings, eviction_id)
    )
    conn.commit()
    conn.close()

# DELETE
def delete_eviction_record(eviction_id):
    conn = get_db()
    conn.execute("DELETE FROM Evictions WHERE eviction_id = ?", (eviction_id,))
    conn.commit()
    conn.close()

# Helper function to get a list of counties for our dropdown menus
def get_county_list():
    conn = get_db()
    counties = conn.execute("SELECT fips, county_name FROM Counties ORDER BY county_name").fetchall()
    conn.close()
    return counties