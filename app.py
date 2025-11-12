# app.py
import streamlit as st
import database as db  # This imports your database.py
import pandas as pd

st.set_page_config(layout="wide")
st.title("CSCI 3304: Housing & Eviction Analysis 🏠")

# --- WEEK 2: FULL CRUD FOR ONE ENTITY (Evictions) ---
st.header("Eviction Records (CRUD)")
st.markdown("This section fulfills the Week 2 requirement for full CRUD on one entity.")

# Get all current eviction records
all_records = db.get_all_eviction_records()

# --- READ ---
st.subheader("R: Read All Eviction Records")
if all_records:
    # Convert list of Row objects to DataFrame for nice display
    # THIS IS THE FIX
    df_records = pd.DataFrame(all_records)
else:
    st.write("No eviction records found.")

# --- CREATE, UPDATE, DELETE ---
st.subheader("C/U/D: Create, Update, or Delete a Record")

# Get a list of counties to populate dropdowns
county_list = db.get_county_list()
# Create a dictionary for easy lookup: {fips: county_name}
county_dict = {fips: name for fips, name in county_list}
# Create a reverse lookup for finding index: {fips: index_in_list}
county_fips = [fips for fips, name in county_list]

col1, col2 = st.columns(2)

with col1:
    # --- UPDATE / DELETE Form ---
    st.markdown("#### Update or Delete")
    
    # Create a selectbox for Update/Delete
    # Format: "ID: 123 - County: 1001"
    record_options = [f"ID: {r['eviction_id']} - {county_dict.get(r['fips'])}" for r in all_records]
    
    if record_options:
        selected_record_str = st.selectbox("Select a Record to Update or Delete:", record_options)
        
        # Find the full record object from the selected string
        selected_id = int(selected_record_str.split(" ")[1])
        selected_record = next((r for r in all_records if r['eviction_id'] == selected_id), None)
        
        if selected_record:
            # Get the index of the county for the dropdown
            try:
                selected_fips_index = county_fips.index(selected_record['fips'])
            except ValueError:
                selected_fips_index = 0 # Default to first if not found

            with st.form("update_form"):
                st.write(f"**Editing Record ID:** {selected_record['eviction_id']}")
                
                # Form fields pre-filled with selected record's data
                up_fips = st.selectbox("County FIPS:", county_fips, index=selected_fips_index, format_func=lambda x: f"{x} - {county_dict.get(x)}")
                up_year = st.number_input("Year:", value=selected_record['evict_year'])
                up_filings = st.number_input("Eviction Filings:", value=selected_record['evict_filings'])

                # --- UPDATE Button ---
                if st.form_submit_button("Update Record"):
                    db.update_eviction_record(selected_record['eviction_id'], up_fips, up_year, up_filings)
                    st.success(f"Record {selected_record['eviction_id']} updated!")
                    st.rerun() # Refresh the page to show changes

                # --- DELETE Button ---
                if st.form_submit_button("DELETE Record", type="primary"):
                    db.delete_eviction_record(selected_record['eviction_id'])
                    st.warning(f"Record {selected_record['eviction_id']} deleted!")
                    st.rerun() # Refresh the page
    else:
        st.write("No records to update or delete.")


with col2:
    # --- CREATE Form ---
    st.markdown("#### Create New Record")
    with st.form("create_form"):
        st.write("Add a new eviction filing record to the database.")
        
        # Form fields for new record
        new_fips = st.selectbox("County FIPS:", county_fips, format_func=lambda x: f"{x} - {county_dict.get(x)}")
        new_year = st.number_input("Year:", value=2018)
        new_filings = st.number_input("Eviction Filings:", value=0)

        # --- CREATE Button ---
        if st.form_submit_button("Create Record"):
            db.add_eviction_record(new_fips, new_year, new_filings)
            st.success("New record added!")
            st.rerun() # Refresh the page

# --- WEEK 3: Analytical Queries (Stubbed out) ---
st.header("Analytical Queries (Week 3)")

st.write("This is where your 5 analytical queries will go.")
# --- WEEK 3: Analytical Queries ---
st.header("Analytical Queries (Week 3)")
st.markdown("These queries highlight barriers related to housing and eviction data.")

# === Query 1: Barrier Hotspot ===
st.subheader("Query 1: Barrier Hotspot (Low Income & High Rent Burden)")
st.write("Find counties where median income is below a threshold and rent burden percentage is above a threshold.")

income_threshold = st.number_input("Income below ($):", value=50000)
rent_burden_threshold = st.number_input("Rent burden above (%):", value=35)

if st.button("Run Query 1"):
    result = db.query_barrier_hotspot(income_threshold, rent_burden_threshold)
    if len(result) > 0:
        st.dataframe(result)
    else:
        st.info("No results found for the selected thresholds.")

# === Query 2: Top 10 Eviction Leaders ===
st.subheader("Query 2: Top 10 Eviction Leaders")
if st.button("Run Query 2"):
    result = db.get_top10_eviction_leaders()
    if len(result) > 0:
        st.dataframe(result)
    else:
        st.info("No eviction data found.")

# === Query 3: Demographic Disparity ===
st.subheader("Query 3: Demographic Disparity (Race & Evictions)")
if st.button("Run Query 3"):
    result = db.query_demographic_disparity()
    if len(result) > 0:
        st.dataframe(result)
    else:
        st.info("No data found for demographic disparity query.")

# === Query 4: Affordability vs. Filings ===
st.subheader("Query 4: Affordability vs. Filings Correlation")
if st.button("Run Query 4"):
    result = db.query_affordability_vs_filings()
    if len(result) > 0:
        st.dataframe(result)
    else:
        st.info("No results found for affordability vs. filings.")

# === Query 5: State-Level Summary ===
st.subheader("Query 5: State-Level Summary (By State)")
state_input = st.text_input("Enter State Abbreviation (e.g., TX, CA, FL):").upper()
if st.button("Run Query 5"):
    result = db.query_state_summary(state_input)
    if len(result) > 0:
        st.dataframe(result)
    else:
        st.info("No results found for that state.")
