# CSCI 3304 Project: Housing & Eviction Barrier Analysis

**Course:** CSCI 3304 - Data for Breaking Barriers
**Project Theme:** A database-driven web application analyzing the relationship between housing affordability, demographics, and eviction outcomes.

---

## 1. 📜 Project Purpose & Overview

The "barrier" this project addresses is **access to affordable, stable housing**. High eviction rates are not just a legal issue; they are a critical social, economic, and health barrier that can lock families in a cycle of poverty.

The goal of this project is to build a data system that allows users to identify, analyze, and highlight the relationship between three key factors:
1.  **Local Demographics:** (e.g., median income, population, racial makeup)
2.  **Housing Costs:** (e.g., median rent, percentage of income spent on rent)
3.  **Eviction Outcomes:** (e.g., total eviction filings)

By linking these datasets, our application enables users to ask complex questions and find "barrier hotspots"—for example, which U.S. counties have a combination of low incomes, high rent burden, and high eviction filings.

---

## 2. ✨ Key Features

This system is built to meet all core project requirements:
* **Relational Database:** A 4-table normalized SQLite database (`project.db`) stores and relates all data by county.
* **Data-Driven Population:** The database is populated from real-world data sources using a one-time Python script (`setup.py`).
* **Full CRUD Functionality:** The application provides full Create, Read, Update, and Delete operations for the `Evictions` table.
* **Interactive Front-End:** A simple, functional UI built with Streamlit (`app.py`) allows users to interact with the database.
* **Analytical Queries:** The system is designed to run 5 non-trivial analytical queries that highlight the "barrier" theme.

---

## 3. 🗄️ Database Schema (Structure)

We chose a relational database (SQLite) because our data is highly structured and fits a 4-table schema, with `Counties` as the central "hub" table. All other data is linked via a `fips` (Federal Information Processing Standard) code.



### SQL Schema Definition

```sql
/* 1. The central 'hub' table for county info */
CREATE TABLE IF NOT EXISTS Counties (
    fips INTEGER PRIMARY KEY,
    county_name TEXT,
    state_abbr TEXT
);

/* 2. Demographic data from Census ACS */
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

/* 3. Housing affordability data from Census ACS */
CREATE TABLE IF NOT EXISTS Housing (
    housing_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fips INTEGER NOT NULL,
    rent_median_gross REAL,
    rent_burdened_pct REAL, -- Pct of renters paying >35% of income
    FOREIGN KEY (fips) REFERENCES Counties (fips)
);

/* 4. Eviction outcome data from Eviction Lab */
CREATE TABLE IF NOT EXISTS Evictions (
    eviction_id INTEGER PRIMARY KEY AUTOINCREMENT,
    fips INTEGER NOT NULL,
    evict_year INTEGER,
    evict_filings INTEGER,
    FOREIGN KEY (fips) REFERENCES Counties (fips)
);
```

---

## 4. 📊 Data Sources

Our final merged dataset (`final_project_data.csv`) was created by cleaning and merging data from two primary sources, joined on the county `FIPS` code.

1.  **Eviction Data:**
    * **Source:** The Eviction Lab at Princeton University
    * **Dataset:** County-level eviction estimates (2000-2018).
    * **Note:** We are using the most recent year available in the file (2018) as a proxy for current eviction trends.

2.  **Demographic & Housing Data:**
    * **Source:** U.S. Census Bureau
    * **Dataset:** ACS 5-Year Estimates Data Profiles (2023).
    * **Tables Used:**
        * `DP03 (Economic)`: Median Household Income
        * `DP04 (Housing)`: Median Gross Rent, Rent Burdened %
        * `DP05 (Demographics)`: Total Population, Race

---

## 5. 🛠️ Technology Stack

* **Backend & DB:** Python & SQLite
* **Data Processing:** Pandas (used in `setup.py` for data loading)
* **Frontend:** Streamlit

---

## 6. 🚀 How to Run This Project

1.  **Clone the Repository (or download the ZIP)**
    ```bash
    git clone [your-git-repo-url-here]
    cd [your-project-folder-name]
    ```

2.  **Install Dependencies**
    This project requires `streamlit` and `pandas`.
    ```bash
    pip install streamlit pandas
    ```

3.  **Build the Database (One-Time Setup)**
    Run the `setup.py` script. This will:
    * Create a new file named `project.db`.
    * Read `final_project_data.csv`.
    * Populate all 4 database tables with 3,100+ county records.

    ```bash
    python setup.py
    ```
    *(You only need to do this once.)*

4.  **Launch the Streamlit App**
    ```bash
    streamlit run app.py
    ```
    Your default web browser will automatically open with the running application.

---

## 7. 📂 Project File Structure

```
.
├── app.py                  # The main Streamlit front-end application
├── database.py             # All SQLite database logic (connection, CRUD functions)
├── setup.py                # One-time script to create and populate the database
├── final_project_data.csv  # The final, cleaned, and merged dataset (our source)
├── project.db              # The SQLite database file (GENERATED by setup.py)
└── README.md               # This file
```

---

## 8. 🔎 Analytical Queries (Week 3 Plan)

The core function of this app is to run 5 analytical queries that highlight barriers. These queries will be accessible from the front end.

1.  **Barrier Hotspot Query (Parameterized):**
    * **Description:** "Find all counties where median income is *below* a user-input threshold AND the rent-burdened percentage is *above* a user-input threshold."
    * **Barrier:** This directly identifies counties where low-income renters are most at risk.

2.  **Demographic Disparity Query:**
    * **Description:** "Compare the average eviction filings in counties where the population is >30% Black vs. counties where it is <10% Black."
    * **Barrier:** This explores the relationship between racial demographics and eviction outcomes.

3.  **Top 10 Eviction Leaders:**
    * **Description:** "List the top 10 counties with the highest number of `evict_filings`."
    * **Barrier:** This identifies the epicenters of the eviction crisis.
    * **Implementation Status:**  
This query is now **fully implemented** in the app (Week 3).  
- The SQL logic lives in `database.py` → function: `get_top10_eviction_leaders()`.  
- The Streamlit UI (in `app.py`) includes a button labeled **"Show Top 10 Counties by Eviction Filings"**.  
- When clicked, it displays the results in a clean, interactive table showing **County**, **State**, and **Eviction Filings**.  

**Example Output:**
| County | State | Eviction Filings |
|---------|--------|-----------------|
| Harris | TX | 1200 |
| Dallas | TX | 950 |
| ... | ... | ... |

4.  **Affordability vs. Filings Correlation:**
    * **Description:** "Show counties where `rent_median_gross` is in the top 25% but `income_median_household` is in the bottom 25%."
    * **Barrier:** This finds areas with the worst affordability mismatch.

5.  **State-Level Summary (Parameterized):**
    * **Description:** "For a user-selected state, show the average `rent_burdened_pct` and total `evict_filings` for all counties in that state."
    * **Barrier:** This allows for state-by-state comparisons.

---

## 👥 Team Members

Emilio Villar
Alejandra Flores

## 9. 📅 Weekly Goals & Timeline

This plan outlines our team's goals for each week, aligned with the project's official timeline.

---

### **Week 1: Topic Selection & Planning (Oct 20-26)**

* [✅] **Choose Topic:** Finalized project on Housing Affordability & Eviction Barriers.
* [✅] **Identify Data Sources:** Located and assessed Eviction Lab and Census ACS data.
* [✅] **Initial Data Model:** Sketched out a 4-table relational model (Counties, Demographics, Housing, Evictions).
* [✅] **Data Exploration:** Used Colab to explore, clean, and merge the raw CSVs into one final dataset (`final_project_data.csv`).
* **Deliverable:** Week 1 planning complete.

---

### **Week 2: Database Setup & Initial CRUD (Oct 27-Nov 2)**

* [✅] **Create Database:** Wrote `database.py` to define the 4-table schema in SQLite.
* [✅] **Populate Database:** Wrote `setup.py` to read `final_project_data.csv` and populate all 3,100+ rows into the database (`project.db`).
* [✅] **Implement CRUD:** Built the Streamlit UI in `app.py` with full Create, Read, Update, and Delete functionality for the `Evictions` table.
* **Deliverable:** **Week 2 check-in complete.** (Database created, sample data loaded, one CRUD path working).

---

### **Week 3: Query Development (Nov 2-9)**

* [**To-Do**] **Implement 3 Queries:** Implement three of our five planned analytical queries.
    * Query 1: Barrier Hotspot Query (Parameterized).
    * Query 2: Top 10 Eviction Leaders.
    * Query 3: Demographic Disparity Query.
* [**To-Do**] **Front-End for Queries:** Build the UI components (e.g., sliders, text inputs, buttons) in `app.py` to run these three queries and display their results in a table.
* **Deliverable:** **Week 3 check-in.** (Three queries functional through UI).
## 🧠 Week 3 Update (Nov 11, 2025)
- Implemented **Top 10 Eviction Leaders Analytical Query**
- Added corresponding **Streamlit front-end button** in `app.py`
- Updated `database.py` with SQL query function
- Verified data displays correctly with test records
- Updated README.md with new query description
---

### **Week 4: Integration & Full CRUD (Nov 10-16)**

* [**To-Do**] **Implement Final 2 Queries:**
    * Query 4: Affordability vs. Filings Correlation.
    * Query 5: State-Level Summary (Parameterized).
* [**To-Do**] **Second CRUD Entity:** Implement full CRUD (Create, Read, Update, Delete) for a second entity (e.g., the `Demographics` table).
* [**To-Do**] **Code Cleanup:** Refine the UI, add helper text, and ensure all components are working smoothly together.
* **Deliverable:** **Week 4 check-in.** (All 5 queries + full CRUD for 2 entities operational).

---

### **Week 5: Final Demo & Report (Nov 17-23)**

* [**To-Do**] **Final Report:** Complete the 3-6 page brief report.
    * Write problem motivation.
    * Create final ER diagram.
    * Describe query insights.
    * Take screenshots of the final front-end.
    * Write "Lessons Learned" section.
* [**To-Do**] **Presentation:** Create the slide deck for the in-class presentation.
* [**To-Do**] **Practice Demo:** Do a full run-through of the final application demo.
* **Deliverable:** **Final system demo & written report submitted.**

---

### **Final Presentations (Dec 1 & 3)**

* [**To-Do**] Deliver in-class presentation and demo.
