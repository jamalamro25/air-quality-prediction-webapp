import streamlit as st
import pandas as pd

# ======================================================
# DATA PREPROCESSING PAGE
# ======================================================
def app(df=None):

    # Load data if not passed from MultiApp
    if df is None:
        df = pd.read_csv("india_air_quality_cleaned.csv")

    st.title("🧼 Data Preprocessing & Feature Engineering")
    st.write("Summary of the data cleaning and feature engineering steps applied before analysis and modelling.")

    st.markdown("---")

    # ======================================================
    # CLEANING SUMMARY (UPDATED – NO FORWARD FILL)
    # ======================================================
    st.subheader("🧼 Cleaning Summary")

    st.markdown(
        """
        **Key preprocessing steps applied in the notebook (mirrored here conceptually):**

        - Removed rows with critical missing values in key pollutant and AQI fields  
        - Ensured all pollutant variables were converted to numeric format  
        - Converted **Date** to proper datetime format  
        - Extracted temporal components: **Year, Month, Day, and Season**  
        - Removed obvious outliers using domain-informed thresholds for pollutant concentrations  
        - Created temporal **lag features** to capture AQI persistence:
          - `AQI_Lag1` – previous day AQI  
          - `AQI_Lag7` – AQI from the previous week  
        - Engineered additional features to support regression and classification models  
        - Encoded **AQI_Bucket** as the target variable for classification tasks  
        """
    )

    st.markdown("---")

    # ======================================================
    # ENGINEERED FEATURES PREVIEW
    # ======================================================
    st.subheader("🧬 Engineered Feature Columns (Preview)")

    engineered_cols = [
        "AQI",
        "PM2.5",
        "PM10",
        "CO",
        "NO2",
        "O3",
        "SO2",
        "NO",
        "Month",
        "AQI_Bucket"
    ]

    existing_cols = [c for c in engineered_cols if c in df.columns]

    st.write(f"**Total engineered / modelling features found:** {len(existing_cols)}")

    st.dataframe(
        df[existing_cols].head(10),
        use_container_width=True
    )

    st.markdown("---")

    # ======================================================
    # NOTE FOR MODELLING
    # ======================================================
    st.info(
        """
        **Note:**
        - No data imputation (e.g. forward fill or interpolation) was applied.
        - Lag features were preferred to preserve temporal structure and improve predictive performance.
        - All modelling results shown later are based on this cleaned and engineered dataset.
        """
    )
