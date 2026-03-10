import streamlit as st
import pandas as pd
from data_utils import load_data

def app():
    st.title("📂 Data Loading")
    st.caption("Get acquainted with the air quality dataset before deep analysis.")

    df = load_data()

    st.markdown("### 👀 Data Preview")
    n_rows = st.slider("Select number of rows to preview:", 5, 100, 10, step=5)
    st.dataframe(df.head(n_rows))

    st.markdown("### 📊 Descriptive Statistics")
    numeric_cols = df.select_dtypes(include="number").columns
    st.dataframe(df[numeric_cols].describe().T)

    st.markdown("### ❓ Missing Values Overview")
    missing = df.isna().sum()
    missing = missing[missing > 0].sort_values(ascending=False)
    if missing.empty:
        st.success("No missing values detected in the dataset ✅")
    else:
        st.warning("Columns with missing values:")
        st.dataframe(missing.to_frame("Missing_Count"))

