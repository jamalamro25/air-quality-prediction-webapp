import streamlit as st
import plotly.express as px
from data_utils import load_data

def app():
    st.title("📊 Data Visualization")
    st.caption("Explore pollution trends, city comparisons, and relationships interactively.")

    df = load_data()

    numeric_cols = df.select_dtypes(include="number").columns.tolist()
    pollutant_cols = [c for c in numeric_cols if c in ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3", "NO"]]

    st.markdown("### 1️⃣ Distribution Exploration")
    selected = st.multiselect(
        "Select numeric columns to show histograms:",
        pollutant_cols,
        default=pollutant_cols[:3] if len(pollutant_cols) >= 3 else pollutant_cols
    )

    for col in selected:
        fig = px.histogram(df, x=col, nbins=50, title=f"Distribution of {col}")
        fig.update_layout(height=300, margin=dict(l=20, r=20, t=40, b=20))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### 2️⃣ City-Level Comparison")

    if "City" in df.columns and pollutant_cols:
        city = st.selectbox("Select pollutant for city comparison:", pollutant_cols)
        city_avg = df.groupby("City")[city].mean().reset_index().sort_values(city, ascending=False)

        fig = px.bar(
            city_avg,
            x="City", y=city,
            title=f"Average {city} by City",
            labels={city: f"Average {city}"},
        )
        fig.update_layout(xaxis_tickangle=-45, height=450, margin=dict(l=20, r=20, t=40, b=100))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")
    st.markdown("### 3️⃣ Correlation Analysis")

    corr_cols = pollutant_cols + ["AQI"] if "AQI" in df.columns else pollutant_cols
    corr_df = df[corr_cols].corr()

    fig = px.imshow(
        corr_df,
        text_auto=True,
        color_continuous_scale="RdBu_r",
        title="Correlation Heatmap (Pollutants & AQI)"
    )
    fig.update_layout(height=600, margin=dict(l=40, r=40, t=60, b=40))
    st.plotly_chart(fig, use_container_width=True)
