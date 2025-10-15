# ============================================
#  Telangana Health Dashboard (Home Page)
# ============================================

import streamlit as st
import sys, os

#  Fix import path dynamically
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../.."))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.utils.sidebar import render_sidebar
from src.utils.ui_theme import apply_global_styles
st.image(
    "https://en.wikipedia.org/wiki/Emblem_of_Telangana#/media/File:Emblem_of_Telangana.svg",
    width=120
)

# --- Page Config ---
st.set_page_config(page_title=" Home Dashboard", page_icon="https://en.wikipedia.org/wiki/Emblem_of_Telangana#/media/File:Emblem_of_Telangana.svg", layout="wide")

# --- Apply Global Theme ---
apply_global_styles()

# --- Render Sidebar ---
render_sidebar()

# --- Custom Styling (Page-specific) ---
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
            color: #00695C;
            font-size: 36px;
            font-weight: 700;
            margin-top: 10px;
        }

        .page-subtitle {
            text-align: center;
            color: #5B4B8A;
            font-size: 18px;
            margin-bottom: 25px;
        }

        .stat-card {
            background: linear-gradient(to bottom right, #ffffff, #F3E5F5);
            padding: 25px;
            border-radius: 16px;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
            text-align: center;
            transition: 0.3s ease;
            animation: fadeIn 1s ease-in-out;
        }
        .stat-card:hover {
            transform: scale(1.03);
            box-shadow: 0px 6px 14px rgba(0,0,0,0.15);
        }

        .stat-number {
            font-size: 38px;
            color: #009688;
            font-weight: 700;
        }

        .stat-label {
            color: #444;
            font-size: 16px;
            font-weight: 600;
            margin-top: 5px;
        }

        .stButton>button {
            background: linear-gradient(to bottom, #009688, #B39DDB);
            color: white;
            border-radius: 10px;
            font-weight: 600;
            transition: 0.3s;
        }
        .stButton>button:hover { 
            background: linear-gradient(to bottom, #00796B, #9575CD);
            transform: scale(1.05); 
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

# --- Page Header ---
st.markdown("<h1 class='page-header'> Telangana Health Dashboard</h1>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Your digital hub for health awareness, analytics, and communication</p>", unsafe_allow_html=True)

# --- Info Box ---
st.info("Navigate using the sidebar to explore **Health Awareness**, **Analytics**, and **Message Center** modules.")

# --- Dashboard Stats ---
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>33</div>
            <div class='stat-label'>Districts Covered</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>12,540</div>
            <div class='stat-label'>Messages Sent</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class='stat-card'>
            <div class='stat-number'>18</div>
            <div class='stat-label'>Active Diseases Tracked</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- Footer Section ---
st.markdown("""
    <div class='footer'>
        Developed with  by <b>Team 18</b> | Telangana Health Awareness 2025
    </div>
""", unsafe_allow_html=True)
