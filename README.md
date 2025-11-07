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
