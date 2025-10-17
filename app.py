import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.title("Placement Data Analytics")

DATA_FILE = "data.csv"

# Load data if file exists, else create empty DataFrame with correct columns
if os.path.exists(DATA_FILE):
    df = pd.read_csv(DATA_FILE)
else:
    df = pd.DataFrame(columns=["Year", "S.No", "Roll No", "Name of the Student", "Branch", "Name of the Employer"])

# --- Summary Cards ---
total_students = len(df)
total_branches = df['Branch'].nunique()
total_recruiters = df['Name of the Employer'].nunique()

col1, col2, col3 = st.columns(3)
col1.metric("Total Students", total_students)
col2.metric("Unique Branches", total_branches)
col3.metric("Recruiters", total_recruiters)

# Display full table
st.subheader("Full Placement Data")
st.dataframe(df)

# --- Bar Chart: Students Placed per Branch ---
st.subheader("Number of Students Placed per Branch")
if not df.empty:
    branch_counts = df['Branch'].value_counts()
    st.bar_chart(branch_counts)
else:
    st.info("No data available to display the chart.")

# --- Sunburst Chart: Employer > Branch > Name of the Student ---
st.subheader("Sunburst Chart: Employer → Branch → Student Name")
if not df.empty:
    fig = px.sunburst(
        df,
        path=["Name of the Employer", "Branch", "Name of the Student"],
        title="Placement Hierarchy"
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No data available to display the sunburst chart.")

# --- Add New Data Form ---
st.subheader("Add New Placement Record")
with st.form("add_record"):
    year = st.text_input("Year")
    sno = st.text_input("S.No")
    rollno = st.text_input("Roll No")
    student = st.text_input("Name of the Student")
    branch = st.text_input("Branch")
    employer = st.text_input("Name of the Employer")
    submitted = st.form_submit_button("Add Record")
    if submitted:
        if all([year, sno, rollno, student, branch, employer]):
            new_row = {
                "Year": year,
                "S.No": sno,
                "Roll No": rollno,
                "Name of the Student": student,
                "Branch": branch,
                "Name of the Employer": employer
            }
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            df.to_csv(DATA_FILE, index=False)
            st.success("Record added successfully! Please refresh the page to see the update.")
        else:
            st.error("Please fill in all fields.")
            

