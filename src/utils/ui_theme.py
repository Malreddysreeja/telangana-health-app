# ============================================
#  Global Theme Styles — Telangana Health App
# (Lavender + Teal Glow + Page Transition)
# ============================================

import streamlit as st

def apply_global_styles():
    st.markdown("""
        <style>
        /* -----------------------------------------
            Global Font + Background
        ----------------------------------------- */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

        html, body, [class*="css"] {
            font-family: 'Poppins', sans-serif;
            background-color: #F6F4FA;
            scroll-behavior: smooth;
        }

        /* -----------------------------------------
            Page Fade-In Animation
        ----------------------------------------- */
        .stApp {
            animation: fadeInPage 1.2s ease-in-out;
            background: linear-gradient(to bottom right, #F6F4FA, #F3E5F5);
        }

        @keyframes fadeInPage {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        /* -----------------------------------------
            Section Cards (used app-wide)
        ----------------------------------------- */
        .card {
            background-color: #ffffff;
            border-radius: 18px;
            padding: 25px;
            box-shadow: 0 6px 15px rgba(0,0,0,0.08);
            transition: all 0.3s ease-in-out;
        }
        .card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 18px rgba(0,0,0,0.12);
        }

        /* -----------------------------------------
            Headers with Soft Glow
        ----------------------------------------- */
        h1, h2, h3 {
            color: #004D40;
            text-align: center;
            text-shadow: 0 0 10px rgba(173, 216, 230, 0.3);
            font-weight: 700;
        }

        /* Smaller headers (subtitles) */
        .sub-header {
            color: #5B4B8A;
            text-align: center;
            font-size: 17px;
            margin-bottom: 15px;
        }

        /* -----------------------------------------
            Buttons
        ----------------------------------------- */
        .stButton>button {
            background: linear-gradient(to bottom right, #009688, #B39DDB);
            color: white;
            font-weight: 600;
            border-radius: 10px;
            padding: 0.6em 1.2em;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            background: linear-gradient(to bottom right, #00796B, #9575CD);
            transform: scale(1.04);
            box-shadow: 0px 4px 12px rgba(0,0,0,0.15);
        }

        /* -----------------------------------------
            Metric Cards (used in dashboards)
        ----------------------------------------- */
        .metric-card {
            background: linear-gradient(to bottom right, #ffffff, #F3E5F5);
            border-radius: 16px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.08);
            text-align: center;
            padding: 20px;
            transition: 0.3s ease;
        }
        .metric-card:hover {
            transform: scale(1.03);
        }

        .metric-value {
            font-size: 28px;
            color: #00796B;
            font-weight: 700;
        }
        .metric-label {
            color: #4B4B4B;
            font-size: 14px;
            font-weight: 600;
        }

        /* -----------------------------------------
            Footer Text
        ----------------------------------------- */
        .footer {
            text-align: center;
            color: #777;
            font-size: 14px;
            margin-top: 30px;
            padding-bottom: 10px;
        }

        /* -----------------------------------------
            Glow on Hover for Interactive Areas
        ----------------------------------------- */
        .stMarkdown:hover, .stSelectbox:hover, .stTextInput:hover {
            transition: 0.3s;
            box-shadow: 0 0 8px rgba(145, 212, 200, 0.4);
            border-radius: 8px;
        }

        /* -----------------------------------------
            Scrollbar Styling
        ----------------------------------------- */
        ::-webkit-scrollbar {
            width: 8px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb {
            background: #B39DDB;
            border-radius: 10px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #9575CD;
        }
        </style>
    """, unsafe_allow_html=True)
