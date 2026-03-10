import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ============================
# Load Data Once
# ============================
@st.cache_data
def load_data():
    df = pd.read_csv("india_air_quality_cleaned.csv")
    df["Date"] = pd.to_datetime(df["Date"])
    df["Year"] = df["Date"].dt.year
    df["Month"] = df["Date"].dt.month
    df["Day"] = df["Date"].dt.day_name()
    return df

# ============================
# Main Dashboard App
# ============================
def app():

    # ============================
    # Title + Subtitle
    # ============================
    st.markdown(
        """
        <h1 style='text-align:center; color:#e2e8f0;'>📊 Insights Dashboard</h1>
        <p style='text-align:center; color:#cbd5e1;'>High-level interactive overview of India's air quality patterns.</p>
        """,
        unsafe_allow_html=True
    )

    df = load_data()

    # ============================
    # Sidebar Filters
    # ============================
    st.sidebar.header("🔍 Filters")
    city_filter = st.sidebar.multiselect(
        "Select Cities", options=df["City"].unique(), default=df["City"].unique()
    )

    df_filtered = df[df["City"].isin(city_filter)]

    # ============================
    # KPI Cards (White Text)
    # ============================
    avg_aqi = df_filtered["AQI"].mean()
    max_aqi = df_filtered["AQI"].max()
    min_aqi = df_filtered["AQI"].min()

    col1, col2, col3 = st.columns(3)
    col1.metric("🌍 Average AQI", f"{avg_aqi:.1f}")
    col2.metric("🔥 Max AQI Recorded", int(max_aqi))
    col3.metric("💧 Min AQI Recorded", int(min_aqi))

    # Force KPI text to be white
    st.markdown(
        """
        <style>
        [data-testid="stMetricLabel"] { color: #e2e8f0 !important; }
        [data-testid="stMetricValue"] { color: #ffffff !important; }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    # ============================
    # VISUAL 1 – AQI Trend Over Time
    # ============================
    st.subheader("📈 AQI Trend Over Time")

    trend_df = df_filtered.groupby("Date")["AQI"].mean().reset_index()

    fig1 = px.line(
        trend_df,
        x="Date",
        y="AQI",
        title="Average AQI Over Time",
        markers=True,
        color_discrete_sequence=["#4FD1C5"]
    )

    fig1.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
        title_font_color="#e2e8f0"
    )

    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("---")

    # ============================
    # VISUAL 2 – City Comparison
    # ============================
    st.subheader("🌆 City Comparison")

    city_avg = df_filtered.groupby("City")["AQI"].mean().sort_values(ascending=False)

    fig2 = px.bar(
        city_avg,
        x=city_avg.values,
        y=city_avg.index,
        orientation="h",
        title="Average AQI by City",
        color=city_avg.values,
        color_continuous_scale="RdYlGn_r",
    )

    fig2.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
        title_font_color="#e2e8f0",
        xaxis=dict(color="#e2e8f0"),
        yaxis=dict(color="#e2e8f0")
    )

    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("---")

    # ============================
    # VISUAL 3 – Radar Chart
    # ============================
    st.subheader("🧪 Pollutant Distribution (Radar Chart)")

    pollutants = ["PM2.5", "PM10", "NO2", "SO2", "CO", "O3"]
    avg_pollutants = df_filtered[pollutants].mean()

    fig3 = go.Figure()
    fig3.add_trace(go.Scatterpolar(
        r=avg_pollutants.values,
        theta=pollutants,
        fill="toself",
        line_color="#F9A825"
    ))

    fig3.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(visible=True, color="#e2e8f0")
        ),
        showlegend=False,
        font_color="#e2e8f0",
        title_font_color="#e2e8f0"
    )

    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("---")

    # ============================
    # VISUAL 4 – Seasonal Heatmap
    # ============================
    st.subheader("📅 Seasonal AQI Heatmap")

    seasonal_data = df_filtered.groupby(["Year", "Month"])["AQI"].mean().reset_index()

    fig4 = px.density_heatmap(
        seasonal_data,
        x="Month",
        y="Year",
        z="AQI",
        color_continuous_scale="Viridis",
        title="Heatmap of AQI by Year & Month",
    )

    fig4.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
        title_font_color="#e2e8f0"
    )

    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("---")

    # ============================
    # VISUAL 5 – Pie Chart (AQI Category)
    # ============================
    st.subheader("🥧 AQI Category Distribution")

    aqi_bins = [0, 50, 100, 200, 300, 400, 500]
    labels = ["Good", "Satisfactory", "Moderate", "Poor", "Very Poor", "Severe"]

    df_filtered["AQI_Category"] = pd.cut(
        df_filtered["AQI"], bins=aqi_bins, labels=labels, include_lowest=True
    )

    cat_counts = df_filtered["AQI_Category"].value_counts()

    fig5 = px.pie(
        names=cat_counts.index,
        values=cat_counts.values,
        title="Distribution of AQI Categories",
        color_discrete_sequence=px.colors.qualitative.Set3,
    )

    fig5.update_traces(textinfo="percent+label")

    fig5.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
        title_font_color="#e2e8f0"
    )

    st.plotly_chart(fig5, use_container_width=True)
    st.markdown("---")

    # ============================
    # VISUAL 6 – Correlation Heatmap
    # ============================
    st.subheader("🔗 Pollutant Correlation Heatmap")

    corr = df_filtered[pollutants + ["AQI"]].corr()

    fig6 = px.imshow(
        corr,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        title="Correlation Between Pollutants and AQI",
    )

    fig6.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
        title_font_color="#e2e8f0"
    )

    st.plotly_chart(fig6, use_container_width=True)
    st.markdown("---")

    # ============================
    # VISUAL 7 – AQI by Weekday
    # ============================
    st.subheader("📆 AQI by Day of Week")

    weekday_avg = df_filtered.groupby("Day")["AQI"].mean().reindex([
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
    ])

    fig7 = px.bar(
        weekday_avg,
        x=weekday_avg.index,
        y=weekday_avg.values,
        title="Average AQI by Day of Week",
        color=weekday_avg.values,
        color_continuous_scale="Bluered",
    )

    fig7.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e2e8f0",
        title_font_color="#e2e8f0",
        xaxis=dict(color="#e2e8f0"),
        yaxis=dict(color="#e2e8f0")
    )

    st.plotly_chart(fig7, use_container_width=True)
