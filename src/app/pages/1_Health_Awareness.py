# ============================================
#  Telangana Health Awareness Dashboard
# ============================================

import os
import sys
import streamlit as st
import runpy

#  Fix import path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if project_root not in sys.path:
    sys.path.append(project_root)

#  Import global theme + sidebar
from src.utils.sidebar import render_sidebar
from src.utils.ui_theme import apply_global_styles

# -------------------------------
#  PAGE CONFIGURATION
# -------------------------------
st.set_page_config(
    page_title=" Health Awareness",
    page_icon="",
    layout="wide"
)

# -------------------------------
#  APPLY GLOBAL THEME
# -------------------------------
apply_global_styles()
render_sidebar()

# -------------------------------
#  PAGE HEADER
# -------------------------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');
        
        .stApp {
            background: linear-gradient(to bottom right, #E8F5F4, #F4EAF8);
            font-family: 'Poppins', sans-serif;
            animation: fadeIn 1s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .page-header {
            text-align: center;
            color: #00695C; /* Teal */
            font-size: 34px;
            font-weight: 700;
            margin-top: 15px;
        }

        .page-subtitle {
            text-align: center;
            color: #5B4B8A; /* Lavender */
            font-size: 18px;
            margin-bottom: 25px;
        }

        .warning-box {
            background: #FFF3E0;
            border-left: 6px solid #FB8C00;
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }

        .footer {
            text-align: center;
            color: #777;
            font-size: 14px;
            margin-top: 30px;
            padding-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
#  PAGE TITLE + INFO
# -------------------------------
st.markdown("<h1 class='page-header'> Telangana Health Awareness Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Monitor health trends, awareness messages, and preventive guidance for Telangana districts.</p>", unsafe_allow_html=True)

# -------------------------------
#  RUN MAIN HEALTH AWARENESS APP
# -------------------------------
app_path = os.path.join(os.path.dirname(__file__), "..", "streamlit_app.py")

if os.path.exists(app_path):
    try:
        runpy.run_path(app_path)
    except Exception as e:
        st.error(f" An error occurred while loading the health awareness module: {e}")
else:
    st.markdown("<div class='warning-box'> <b>streamlit_app.py</b> not found. Please ensure it exists in the <b>app/</b> folder.</div>", unsafe_allow_html=True)

# -------------------------------
#  FOOTER
# -------------------------------
st.markdown("""
    <div class='footer'>
        Developed with  by <b>Team 18</b> | Telangana Health Awareness 2025
    </div>
""", unsafe_allow_html=True)
