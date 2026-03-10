import streamlit as st
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    r2_score,
    mean_absolute_error,
    mean_squared_error,
    accuracy_score,
    classification_report
)

import plotly.express as px


# ======================================================
# MAIN APP FUNCTION (called by MultiApp)
# ======================================================
def app(df=None):

    # Load dataframe if not passed by MultiApp
    if df is None:
        df = pd.read_csv("india_air_quality_cleaned.csv")

    # ======================================================
    # FIX – ENSURE LAG FEATURES EXIST
    # ======================================================
    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

    if "AQI_Lag1" not in df.columns:
        df["AQI_Lag1"] = df.groupby("City")["AQI"].shift(1)

    if "AQI_Lag7" not in df.columns:
        df["AQI_Lag7"] = df.groupby("City")["AQI"].shift(7)

    df = df.dropna(subset=["AQI_Lag1", "AQI_Lag7"])

    # ======================================================
    # PAGE HEADER
    # ======================================================
    st.title("🤖 Modeling & Evaluation")
    st.write("Regression and classification models for AQI prediction and categorisation.")

    # ======================================================
    # MAKE ALL METRIC NUMBERS WHITE
    # ======================================================
    metric_style = """
    <style>
    [data-testid="stMetricValue"] {
        color: white !important;
    }
    </style>
    """
    st.markdown(metric_style, unsafe_allow_html=True)

    # ======================================================
    # FEATURE SELECTION
    # ======================================================
    all_features = [
        "AQI_Lag1", "AQI_Lag7",
        "PM2.5", "PM10", "NO", "NO2", "NOx",
        "NH3", "CO", "SO2", "O3"
    ]

    default_features = ["AQI_Lag1", "AQI_Lag7", "PM2.5", "PM10", "CO"]

    selected_features = st.multiselect(
        "Select features to include in the models:",
        options=all_features,
        default=default_features
    )

    # Info message when defaults are used
    if set(selected_features) == set(default_features):
        st.success(
            "⭐ **Strongest predictors selected by default**\n\n"
            "- AQI_Lag1 (yesterday’s AQI)\n"
            "- AQI_Lag7 (last week’s AQI)\n"
            "- PM2.5, PM10, CO\n\n"
            "This configuration achieved the **highest model performance (R² ≈ 0.88–0.89)**."
        )

    X = df[selected_features]
    y_reg = df["AQI"]

    # ======================================================
    # TRAIN–TEST SPLIT (REGRESSION)
    # ======================================================
    X_train, X_test, y_train, y_test = train_test_split(
        X, y_reg, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # ======================================================
    # MULTIPLE LINEAR REGRESSION
    # ======================================================
    st.subheader("📈 Multiple Linear Regression")

    lr = LinearRegression()
    lr.fit(X_train_scaled, y_train)
    lr_pred = lr.predict(X_test_scaled)

    lr_r2 = r2_score(y_test, lr_pred)
    lr_mae = mean_absolute_error(y_test, lr_pred)
    lr_rmse = np.sqrt(mean_squared_error(y_test, lr_pred))

    col1, col2, col3 = st.columns(3)
    col1.metric("R² Score", f"{lr_r2:.3f}")
    col2.metric("MAE", f"{lr_mae:.2f}")
    col3.metric("RMSE", f"{lr_rmse:.2f}")

    coef_df = pd.DataFrame({
        "Feature": selected_features,
        "Coefficient": lr.coef_
    }).sort_values(by="Coefficient", ascending=False)

    st.write("**Feature Coefficients**")
    st.dataframe(coef_df, use_container_width=True)

    st.markdown("---")

    # ======================================================
    # RANDOM FOREST REGRESSOR
    # ======================================================
    st.subheader("🌲 Random Forest Regressor")

    rf = RandomForestRegressor(
        n_estimators=200,
        max_depth=15,
        random_state=42,
        n_jobs=-1
    )
    rf.fit(X_train, y_train)
    rf_pred = rf.predict(X_test)

    rf_r2 = r2_score(y_test, rf_pred)
    rf_mae = mean_absolute_error(y_test, rf_pred)
    rf_rmse = np.sqrt(mean_squared_error(y_test, rf_pred))

    col1, col2, col3 = st.columns(3)
    col1.metric("R² Score", f"{rf_r2:.3f}")
    col2.metric("MAE", f"{rf_mae:.2f}")
    col3.metric("RMSE", f"{rf_rmse:.2f}")

    rf_feat = pd.DataFrame({
        "Feature": selected_features,
        "Importance": rf.feature_importances_
    }).sort_values(by="Importance", ascending=False)

    st.write("**Feature Importance**")
    st.dataframe(rf_feat, use_container_width=True)

    st.markdown("---")

    # ======================================================
    # MODEL COMPARISON
    # ======================================================
    st.subheader("📊 Regression Model Comparison")

    comparison_df = pd.DataFrame({
        "Model": ["Multiple Linear Regression", "Random Forest Regressor"],
        "R² Score": [lr_r2, rf_r2],
        "MAE": [lr_mae, rf_mae],
        "RMSE": [lr_rmse, rf_rmse]
    })

    st.dataframe(
        comparison_df.style.format({
            "R² Score": "{:.3f}",
            "MAE": "{:.2f}",
            "RMSE": "{:.2f}"
        }),
        use_container_width=True
    )

    st.markdown("---")

    # ======================================================
    # DECISION TREE CLASSIFIER (AQI CATEGORY)
    # ======================================================
    st.subheader("🌳 Decision Tree Classifier (AQI Category)")

    y_class = df["AQI_Bucket"]

    le = LabelEncoder()
    y_class_enc = le.fit_transform(y_class)

    X_train_c, X_test_c, y_train_c, y_test_c = train_test_split(
        X, y_class_enc,
        test_size=0.2,
        random_state=42,
        stratify=y_class_enc
    )

    dt = DecisionTreeClassifier(
        max_depth=6,
        min_samples_leaf=50,
        random_state=42
    )
    dt.fit(X_train_c, y_train_c)
    y_pred_c = dt.predict(X_test_c)

    acc = accuracy_score(y_test_c, y_pred_c)

    # FIX — Classification accuracy also white
    st.metric("🎯 Classification Accuracy", f"{acc:.3f}")

    st.markdown("---")

    # ======================================================
    # CONFUSION MATRIX
    # ======================================================
    st.subheader("📊 Confusion Matrix")

    cm = pd.crosstab(
        y_test_c,
        y_pred_c,
        rownames=["Actual"],
        colnames=["Predicted"]
    )

    fig_cm = px.imshow(
        cm,
        text_auto=True,
        color_continuous_scale="Blues",
        labels=dict(color="Count")
    )
    fig_cm.update_layout(height=500)
    st.plotly_chart(fig_cm, use_container_width=True)

    st.markdown("---")

    # ======================================================
    # CATEGORY DISTRIBUTION
    # ======================================================
    st.subheader("📉 AQI Category Distribution")

    class_dist = df["AQI_Bucket"].value_counts().reset_index()
    class_dist.columns = ["AQI Category", "Count"]

    fig_dist = px.bar(
        class_dist,
        x="AQI Category",
        y="Count",
        color="Count",
        color_continuous_scale="Viridis"
    )
    st.plotly_chart(fig_dist, use_container_width=True)

    st.markdown("---")

    # ======================================================
    # CLASSIFICATION REPORT
    # ======================================================
    st.subheader("📄 Classification Report")

    report_df = pd.DataFrame(
        classification_report(
            y_test_c,
            y_pred_c,
            target_names=le.classes_,
            output_dict=True
        )
    ).transpose()

    st.dataframe(report_df.style.format("{:.2f}"), use_container_width=True)

    # ======================================================
    # INTERPRETATION
    # ======================================================
    st.info(
        """
        **Interpretation:**
        - Random Forest outperforms Linear Regression due to non-linear relationships.
        - Lag features (AQI_Lag1, AQI_Lag7) significantly improve predictive accuracy.
        - Decision Tree performs well on dominant AQI categories.
        - Lower recall for extreme AQI levels is due to class imbalance.
        """
    )
