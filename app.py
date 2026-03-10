import streamlit as st
from multiapp import MultiApp

import home
import data_loading
import data_preprocessing
import data_visualization
import modeling
import dashboard


# ==================================================
# 🌑 PROFESSIONAL DARK NAVY THEME (CSS Injection)
# ==================================================

dark_theme_css = """
<style>

/* Main App Background */
[data-testid="stAppViewContainer"] {
    background-color: #0f172a;  /* Dark Navy */
    color: #e2e8f0;             /* Soft Gray Text */
}

/* Sidebar Background */
[data-testid="stSidebar"] {
    background-color: #1e293b;  /* Deep Slate Blue */
    color: #e2e8f0;
}

/* Sidebar Text Color */
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}

/* Main Body Text */
h1, h2, h3, h4, h5, h6, p, span {
    color: #e2e8f0 !important;
}

/* Transparent Header */
[data-testid="stHeader"] {
    background-color: rgba(255, 255, 255, 0);
}

/* Toolbar Fix */
[data-testid="stToolbar"] {
    right: 2rem;
}

/* Buttons */
.stButton>button {
    background-color: #14b8a6;   /* Teal */
    color: white;
    border-radius: 6px;
    border: none;
    padding: 0.6rem 1.2rem;
    font-weight: 600;
}
.stButton>button:hover {
    background-color: #0d9488;   /* Darker Teal */
}
</style>
"""
st.markdown(dark_theme_css, unsafe_allow_html=True)



# ==================================================
# 🌍 GLOBAL PAGE SETTINGS
# ==================================================

st.set_page_config(
    page_title="India Air Quality Intelligence",
    page_icon="🌫️",
    layout="wide"
)



# ==================================================
# 🚀 MULTI-PAGE APPLICATION INITIALISATION
# ==================================================

app = MultiApp()

app.add_app("🏠 Home", home.app)
app.add_app("📂 Data Loading", data_loading.app)
app.add_app("🧹 Data Preprocessing", data_preprocessing.app)
app.add_app("📊 Data Visualization", data_visualization.app)
app.add_app("🤖 Modeling & Evaluation", modeling.app)
app.add_app("📈 Insights Dashboard", dashboard.app)



# ==================================================
# ▶️ RUN APPLICATION
# ==================================================

app.run()
