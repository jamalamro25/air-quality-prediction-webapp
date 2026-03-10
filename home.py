import streamlit as st
import pandas as pd

# ===============================
# HOME PAGE APP
# ===============================
def app():

    # ===============================
    # PAGE TITLE & INTRO
    # ===============================
    st.markdown("""
        <h1 style='text-align:center; color:white; font-size:42px;'>
            🌏 India Air Quality Intelligence
        </h1>
        <p style='text-align:center; color:#cccccc; font-size:18px;'>
            An interactive analytics platform for exploring, modelling, 
            and visualising India’s air quality trends (2015–2020).<br>
            Developed as part of the <b>CMP7005 – Programming for Data Analysis</b> module.
        </p>
        <hr style='border:1px solid #333; margin-top:20px;'>
    """, unsafe_allow_html=True)

    # ===============================
    # PROJECT GOALS
    # ===============================
    st.markdown("""
        <h2 style='color:white;'>🔍 Project Goals</h2>
        <ul style='color:#dddddd; font-size:17px;'>
            <li>Monitor and analyse pollution patterns across major Indian cities</li>
            <li>Predict <b>AQI values</b> using Multiple Linear Regression and Random Forest Regression</li>
            <li>Classify <b>AQI categories</b> using a Decision Tree Classifier</li>
            <li>Provide an interactive dashboard for exploring AQI insights and comparisons</li>
        </ul>
        <br>
    """, unsafe_allow_html=True)

    # ===============================
    # QUICK SNAPSHOT SECTION (UNIFORM KPI CARDS)
    # ===============================
    st.markdown("<h2 style='text-align:center; color:white;'>📊 Quick Snapshot</h2>", unsafe_allow_html=True)
    st.write("")

    df = pd.read_csv("india_air_quality_cleaned.csv")

    rows = len(df)
    cities = df["City"].nunique()
    date_range = f"{df['Year'].min()}–{df['Year'].max()}"

    col1, col2, col3, col4 = st.columns(4)

    # --- Reusable KPI card ---
    def kpi_card(title, icon, value):
        return f"""
            <div style='
                border:1px solid #444; 
                border-radius:12px; 
                padding:25px; 
                text-align:center;
                height:150px;
                display:flex;
                flex-direction:column;
                justify-content:center;
            '>
                <h4 style='color:#f2f2f2; margin-bottom:8px; font-size:20px;'>
                    {icon} {title}
                </h4>
                <p style='color:white; font-size:20px; margin:0;'>
                    {value}
                </p>
            </div>
        """

    # KPI CARDS (Perfectly uniform)
    col1.markdown(kpi_card("Rows", "📌", f"{rows:,}"), unsafe_allow_html=True)
    col2.markdown(kpi_card("Cities", "🏙️", cities), unsafe_allow_html=True)
    col3.markdown(kpi_card("Date Range", "📅", date_range), unsafe_allow_html=True)
    col4.markdown(kpi_card("Targets", "🎯", "AQI<br>AQI Category"), unsafe_allow_html=True)

    st.markdown("<br><hr style='border:1px solid #333;'>", unsafe_allow_html=True)

    # ===============================
    # INDIA MAP (STATIC IMAGE)
    # ===============================
    st.markdown("""
        <h2 style='text-align:center; color:white;'>🗺️ India Map</h2>
        <p style='text-align:center; color:#cccccc; font-size:16px;'>
            Geographic overview of major cities across India.
        </p>
        <br>
    """, unsafe_allow_html=True)

    # If using Google Drive → update the path here
    image_path = "india_map_dark.jpg"

    try:
        st.image(image_path)
    except:
        st.warning("⚠️ Map image not found. Please upload 'india_map_dark.png' or correct the file path.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ===============================
    # NAVIGATOR FOOTER NOTE
    # ===============================
    st.markdown("""
        <div style='text-align:center; margin-top:20px; padding:15px;
                    background-color:#102030; border-radius:10px; color:#dddddd;'>
            Use the sidebar to navigate through data loading, preprocessing,
            visualisation, modeling, and insights.
        </div>
    """, unsafe_allow_html=True)



