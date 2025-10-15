# ============================================
#  Telangana District Health Analytics Dashboard
# ============================================

import os
import pandas as pd
import streamlit as st
import plotly.express as px

#  Fix path + import global theme + sidebar
from src.utils.ui_theme import apply_global_styles
from src.utils.sidebar import render_sidebar

# Apply global lavender–teal theme
apply_global_styles()

# -------------------------------
#  PAGE CONFIGURATION
# -------------------------------
st.set_page_config(
    page_title=" Health Analytics Dashboard",
    page_icon=" ",
    layout="wide"
)

# Render sidebar for navigation
render_sidebar()

# -------------------------------
#  Page Styling
# -------------------------------
st.markdown("""
    <style>
        .page-header {
            text-align: center;
            color: #00695C;
            font-size: 34px;
            font-weight: 700;
            margin-bottom: 5px;
        }
        .page-subtitle {
            text-align: center;
            color: #5B4B8A;
            font-size: 17px;
            margin-bottom: 25px;
        }
        .fadein {
            animation: fadeIn 1s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
#  PAGE HEADER
# -------------------------------
st.markdown("<h1 class='page-header fadein'> Telangana District Health Analytics Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle fadein'>Explore district-wise disease data and visualize health insights interactively.</p>", unsafe_allow_html=True)

# -------------------------------
#  Dataset Path
# -------------------------------
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
dataset_path = os.path.join(project_root, "data", "raw", "telangana_health_dataset2025.csv")

# -------------------------------
#  Load Dataset
# -------------------------------
@st.cache_data
def load_data():
    if not os.path.exists(dataset_path):
        st.error(f"Dataset not found at: {dataset_path}")
        return pd.DataFrame()
    return pd.read_csv(dataset_path)

df = load_data()
if df.empty:
    st.stop()

# -------------------------------
#  Validate Dataset
# -------------------------------
required_cols = {"District", "Disease", "Cases"}
if not required_cols.issubset(df.columns):
    st.error(f"Dataset must include columns: {required_cols}")
    st.stop()

# -------------------------------
#  District Selection
# -------------------------------
districts = sorted(df["District"].dropna().unique())
col1, col2 = st.columns([1.5, 2])

with col1:
    selected_district = st.selectbox(" Select a District:", districts)

with col2:
    st.info("Explore yearly and disease-wise trends below ")

district_data = df[df["District"] == selected_district]

if district_data.empty:
    st.warning("No data available for this district.")
    st.stop()

# -------------------------------
#  Top Reported Diseases (Bar Chart)
# -------------------------------
st.markdown("<div class='card fadein'>", unsafe_allow_html=True)
st.subheader(f" Top Reported Diseases in {selected_district}")

top_disease_data = (
    district_data.groupby("Disease")["Cases"]
    .sum()
    .reset_index()
    .sort_values(by="Cases", ascending=False)
)

fig_bar = px.bar(
    top_disease_data.head(10),
    x="Disease",
    y="Cases",
    color="Cases",
    text_auto=True,
    color_continuous_scale=["#A7FFEB", "#26A69A", "#004D40"],
    title=f"Top Diseases in {selected_district}",
)
fig_bar.update_layout(
    xaxis_title="Disease",
    yaxis_title="Reported Cases",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Poppins", size=14),
)
st.plotly_chart(fig_bar, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
#  Yearly Disease Trend (Line Chart)
# -------------------------------
if "Year" in df.columns:
    st.markdown("<div class='card fadein'>", unsafe_allow_html=True)
    st.subheader(" Yearly Disease Trends")

    year_trend = (
        district_data.groupby(["Year", "Disease"])["Cases"].sum().reset_index()
    )
    fig_line = px.line(
        year_trend,
        x="Year",
        y="Cases",
        color="Disease",
        markers=True,
        title=f"Yearly Trend of Diseases in {selected_district}",
    )
    fig_line.update_layout(
        xaxis_title="Year",
        yaxis_title="Cases",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Poppins", size=14),
    )
    st.plotly_chart(fig_line, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.info(" No 'Year' column found in dataset. Add it to enable trend visualization.")

# -------------------------------
#  Summary Statistics
# -------------------------------
st.markdown("<div class='card fadein'>", unsafe_allow_html=True)
st.subheader(" Summary Statistics")

total_cases = int(district_data["Cases"].sum())
num_diseases = district_data["Disease"].nunique()

col3, col4 = st.columns(2)
with col3:
    st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{total_cases:,}</div>
            <div class='metric-label'>Total Reported Cases</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class='metric-card'>
            <div class='metric-value'>{num_diseases}</div>
            <div class='metric-label'>Unique Diseases Reported</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
#  Footer
# -------------------------------
st.markdown("""
    <div class='footer'>
        Developed with 💜💙 by <b>Team 18</b> | Telangana Health Awareness 2025
    </div>
""", unsafe_allow_html=True)
