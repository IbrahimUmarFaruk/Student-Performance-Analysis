# IMPORTING OPERATING SYSTEM AND CHANGING THE WORKING DIRECTORY
import streamlit as st 
import pandas as pd
import plotly.express as px

import os 
os.chdir("C:/Users/LENOVO/OneDrive/Documents/Data Science Projects/STUDENT PERFORMANCE ANALYSIS")


# 1.PAGE SETUP
st.set_page_config(page_title ="STUDENT PERFORMANCE DASHBOARD", layout="wide")

st.title("STUDENT ACADEMIC PERFORMANCE DASHBOARD")
st.write("INTERACTIVE ANALYSIS OF STUDENT DATA")

# 2. LOAD DATA
# Using a function with @st.cache_data so it doesn't reload every time. 
@st.cache_data 
def load_data():
    df = pd.read_excel('Cleaned_Student_Data.xlsx')
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Could not find 'Cleaned_Student_Data.xlsx'. Please run Part 2 first!")
    st.stop()

# 3. SIDEBAR FILTERS
st.sidebar.header("Filter Data")

# FILTERING  BY GENDER
gender_filter = st.sidebar.multiselect("Select Gender:", options=df['Gender'].unique(), default=df['Gender'].unique())

# FILTERING BY PERFORMANCE
Performance_filter = st.sidebar.multiselect("Select Performance Category:", options=df['Performance_Category'].unique(), default=df['Performance_Category'].unique())

# APPLYING FILTERS
df_selection = df.query("Gender == @gender_filter & Performance_Category == @Performance_filter")

# 4. KEY METRICS (KPIs)
st.markdown("## Key Metrics")
col1, col2, col3, col4 = st.columns(4)

total_students = len(df_selection)
avg_score = df_selection['Average_Score'].mean()
avg_study = df_selection['Study_Hours_Weekly'].mean()
avg_attendance = df_selection['Attendance_Rate'].mean()

col1.metric("Total Students", f"{total_students}")
col2.metric("Average Score", f"{avg_score:.1f}")
col3.metric("Average Study Hours", f"{avg_study:.1f}")
col4.metric("Average Attendance", f"{avg_attendance:.1f}%")

st.markdown("---")

# 5.CHARTS
col_left, col_right = st.columns(2)

# Chart A: Study Hours Vs Average Score (Scatter Plot)
with col_left:
    st.subheader("Does Studying Help?")
    fig_scatter = px.scatter(df_selection, x="Study_Hours_Weekly", y="Average_Score", color="Performance_Category", size="Attendance_Rate", hover_data=['Student_ID'], title="Study Hours Vs Grades")

st.plotly_chart(fig_scatter, use_container_width=True)

# Chart B: Performance Distribution (Bar Chart)
with col_right:
    st.subheader("Performance Counts")
    # Counting Students in Each Category
    counts = df_selection['Performance_Category'].value_counts().reset_index()
    counts.columns = ['Category', 'Count']
    fig_bar = px.bar(counts, x='Category', y='Count', color='Category', title="Number of Students by Category")
    st.plotly_chart(fig_bar, use_container_width=True)

# 6. VIEW RAW DATA
if st.checkbox("Show Raw Data"):
    st.dataframe(df_selection)
    