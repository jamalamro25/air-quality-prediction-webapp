import streamlit as st
import pandas as pd

DATA_PATH = "india_air_quality_cleaned.csv"  # 🔴 CHANGE to your actual file name

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    return df
