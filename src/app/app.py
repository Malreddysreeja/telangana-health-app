# ============================================
#  Telangana Health Awareness Portal (Main App)
# ============================================

import os
import sys
import streamlit as st

#  Dynamically add project root to Python path
current_file = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

#  Import theme and sidebar safely
try:
    from src.utils.ui_theme import apply_global_styles
    from src.utils.sidebar import render_sidebar
except ModuleNotFoundError as e:
    st.error(f" Import error: {e}")
    st.stop()

#  Apply global Lavender + Teal styles
apply_global_styles()

# -------------------------------
#  PAGE CONFIGURATION
# -------------------------------
st.set_page_config(
    page_title="Telangana Health Awareness Portal",
    page_icon="https://en.wikipedia.org/wiki/Emblem_of_Telangana#/media/File:Emblem_of_Telangana.svg",
    layout="wide"
)

# -------------------------------
#  Render Sidebar
# -------------------------------
render_sidebar()

# -------------------------------
#  Custom Style Enhancements
# -------------------------------
st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

        .stApp {
            background: linear-gradient(to bottom right, #E8F5F4, #F4EAF8);
            font-family: 'Poppins', sans-serif;
        }

        h1, h2, h3 {
            font-family: 'Poppins', sans-serif;
        }

        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(10px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        .footer {
            text-align: center;
            color: #777;
            font-size: 14px;
            margin-top: 25px;
        }

        ul {
            color: #555;
            line-height: 1.8;
            margin-left: 25px;
        }

        li {
            margin-bottom: 5px;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
#  MAIN PAGE CONTENT
# -------------------------------
st.markdown("""
    <h1 style='text-align:center; color:#00695C;'> Telangana Health Awareness Portal</h1>
    <p style='text-align:center; color:#5B4B8A; font-size:18px;'>
        Empowering Telangana through Health Awareness & Digital Innovation
    </p>
""", unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

#  FIXED SECTION BELOW 
welcome_html = """
<div style="
    background-color:#ffffff;
    border-radius:16px;
    padding:30px;
    box-shadow:0 6px 15px rgba(0,0,0,0.1);
    animation: fadeIn 1.2s ease-in-out;
">
  <h3 style="color:#00695C;"> Welcome to the Telangana Health Awareness Portal</h3>

  <p style="color:#444;font-size:16px;">
    The <b>Telangana Health Awareness Portal</b> is an initiative to enhance
    community health awareness, disease prevention, and timely communication
    across all 33 districts of Telangana. Our mission is to create a well-informed,
    health-conscious society using the power of data and digital tools.
  </p>

  <p style="color:#444;font-size:16px;">
    This platform provides comprehensive health insights, real-time disease tracking,
    and digital awareness tools designed for both citizens and local health workers.
  </p>

  <ul style="color:#555;line-height:1.8;margin-left:25px;">
    <li> <b>Analytics Dashboard</b> — Explore district-level health statistics and visual reports</li>
    <li> <b>Health Awareness</b> — Discover disease-specific awareness messages and preventive measures</li>
    <li> <b>Health Chat Assistant</b> — Interact with an AI assistant for instant health guidance</li>
    <li> <b>Message Center</b> — Send health alerts via SMS or WhatsApp to communities</li>
  </ul>

  <p style="color:#444;font-size:16px;margin-top:10px;">
    Together, let’s build a healthier and more informed Telangana. 💙💜
  </p>
</div>
"""

st.components.v1.html(welcome_html, height=600)

st.markdown("<hr>", unsafe_allow_html=True)

# -------------------------------
#  FOOTER
# -------------------------------
st.markdown("""
    <div class='footer'>
        Developed with  by <b>Team 18</b> | Telangana Health Awareness 2025
    </div>
""", unsafe_allow_html=True)
