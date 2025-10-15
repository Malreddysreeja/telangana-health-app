# ============================================
#  Telangana Health Message Center (Lavender + Teal Theme)
# ============================================

import sys
import os
import streamlit as st

#  Add the project root to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
if project_root not in sys.path:
    sys.path.append(project_root)

#  Import theme and sidebar
from src.utils.sidebar import render_sidebar
from src.utils.ui_theme import apply_global_styles
from src.utils.message_service import send_health_message

# -------------------------------
#  PAGE CONFIGURATION
# -------------------------------
st.set_page_config(page_title=" Message Center", page_icon="", layout="wide")

# Apply global Lavender + Teal theme
apply_global_styles()
render_sidebar()

# -------------------------------
#  Custom Styling
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
            color: #00695C; /* teal */
            font-size: 34px;
            font-weight: 700;
            margin-bottom: 6px;
        }

        .page-subtitle {
            text-align: center;
            color: #5B4B8A; /* lavender accent */
            margin-bottom: 25px;
        }

        .card {
            background-color: #ffffff;
            border-radius: 16px;
            padding: 25px;
            box-shadow: 0px 4px 12px rgba(0,0,0,0.1);
            margin: 20px auto;
            max-width: 750px;
            transition: all 0.3s ease;
            animation: fadeIn 1s ease-in-out;
        }

        .card:hover {
            transform: scale(1.01);
            box-shadow: 0px 6px 15px rgba(0,0,0,0.15);
        }

        input, textarea {
            border-radius: 8px !important;
            border: 1px solid #B39DDB !important;
            padding: 10px !important;
            width: 100%;
            font-family: 'Poppins', sans-serif;
        }

        .stButton>button {
            background: linear-gradient(to bottom, #009688, #B39DDB);
            color: white;
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.3s ease;
            height: 3em;
            width: 100%;
        }

        .stButton>button:hover {
            background: linear-gradient(to bottom, #00796B, #9575CD);
            transform: scale(1.05);
        }

        .success-msg {
            text-align: center;
            font-size: 18px;
            color: #00695C;
            font-weight: 600;
            margin-top: 15px;
        }

        .footer {
            text-align: center;
            color: #777;
            font-size: 14px;
            margin-top: 35px;
            padding-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
#  Page Header
# -------------------------------
st.markdown("<h1 class='page-header'> Health Awareness Message Center</h1>", unsafe_allow_html=True)
st.markdown("<p class='page-subtitle'>Send health awareness messages instantly via SMS or WhatsApp using Twilio</p>", unsafe_allow_html=True)

# -------------------------------
#  Message Form
# -------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("###  Compose Message")

recipient = st.text_input(" Recipient Number (with country code, e.g., +91XXXXXXXXXX):")
message = st.text_area(" Message Content:")
via_whatsapp = st.checkbox("Send via WhatsApp (instead of SMS)")
st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
#  Send Button Action
# -------------------------------
if st.button(" Send Message"):
    if not recipient or not message:
        st.warning(" Please enter both recipient number and message text.")
    else:
        with st.spinner("Sending message... "):
            try:
                result = send_health_message(recipient, message, via_whatsapp)
                if result["status"] == "success":
                    st.balloons()
                    st.markdown(f"<p class='success-msg'> Message sent successfully!<br>SID: {result['sid']}</p>", unsafe_allow_html=True)
                else:
                    st.error(f" Failed to send message: {result['message']}")
            except Exception as e:
                st.error(f" Error sending message: {e}")

# -------------------------------
# ℹ Sidebar Info
# -------------------------------
with st.sidebar:
    st.markdown("### ℹ Twilio Info")
    st.info(
        """
         **Twilio Message Center**
        - Supports SMS and WhatsApp messages  
        - Works with Twilio Sandbox for testing  
        - Use the checkbox for WhatsApp mode  
        - Verify your number in Twilio before sending  
        """
    )
    st.caption(" Ensure your Twilio credentials are set as environment variables.")

# -------------------------------
#  Footer
# -------------------------------
st.markdown("""
    <div class='footer'>
        Developed with  by <b>Team 18</b> | Telangana Health Awareness 2025
    </div>
""", unsafe_allow_html=True)
