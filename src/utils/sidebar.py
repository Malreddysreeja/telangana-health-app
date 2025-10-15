# ============================================
#  Custom Sidebar for Telangana Health App
# (Lavender–Teal Theme + Dynamic Highlight + Glowing Hover Tooltips + Local Logo)
# ============================================

import streamlit as st
import os

def render_sidebar():
    # -------------------------------
    #  Sidebar Styling (Animated + Glow Tooltip)
    # -------------------------------
    st.markdown("""
        <style>
        /* --- Sidebar Container --- */
        [data-testid="stSidebar"] {
            background: linear-gradient(to bottom right, #B2DFDB, #E1BEE7);
            border-top-right-radius: 20px;
            border-bottom-right-radius: 20px;
            width: 230px !important;
            padding-top: 10px;
            box-shadow: 2px 0 12px rgba(0,0,0,0.08);
            transition: all 0.8s ease;
            animation: slideFadeIn 1.2s ease-out;
            opacity: 0.98;
        }

        /* --- Combined Slide + Fade Animation --- */
        @keyframes slideFadeIn {
            0% { transform: translateX(-260px); opacity: 0; }
            60% { transform: translateX(10px); opacity: 0.7; }
            100% { transform: translateX(0); opacity: 1; }
        }

        /* --- Font Styling --- */
        [data-testid="stSidebar"] * {
            font-family: 'Poppins', sans-serif;
        }

        /* --- Sidebar Header Label --- */
        [data-testid="stSidebarNav"]::before {
            content: " Telangana Health Awareness";
            font-size: 20px;
            font-weight: 600;
            color: #004D40;
            text-align: center;
            display: block;
            padding: 12px 0;
            animation: fadeInText 1.5s ease-in-out;
        }

        /* --- Text Fade-In Animation --- */
        @keyframes fadeInText {
            from { opacity: 0; }
            to { opacity: 1; }
        }

        /* --- Sidebar Links --- */
        [data-testid="stSidebar"] a {
            position: relative;
            color: #004D40 !important;
            font-weight: 500;
            text-decoration: none;
            transition: 0.25s ease;
            border-radius: 8px;
            padding: 6px 10px 6px 14px;
            opacity: 0.9;
            display: block;
        }

        /* --- Hover Glow --- */
        [data-testid="stSidebar"] a:hover {
            color: #00695C !important;
            background-color: rgba(255, 255, 255, 0.25);
            box-shadow: 0 0 12px rgba(255,255,255,0.5);
            transform: translateX(4px);
            transition: 0.3s ease;
            opacity: 1;
        }

        /* --- Active Highlight Bar --- */
        [data-testid="stSidebar"] a[data-active="true"] {
            font-weight: 700 !important;
            color: #004D40 !important;
            background-color: rgba(255, 255, 255, 0.35);
            border-left: 5px solid #00796B;
            padding-left: 10px;
            box-shadow: inset 4px 0 6px rgba(0,0,0,0.05);
            border-radius: 8px;
            transition: all 0.4s ease;
        }

        /* --- Tooltip Styling --- */
        [data-testid="stSidebar"] a::after {
            content: attr(data-tooltip);
            position: absolute;
            left: 240px;
            top: 50%;
            transform: translateY(-50%);
            background: rgba(0, 105, 92, 0.95);
            color: white;
            font-size: 13px;
            padding: 6px 10px;
            border-radius: 6px;
            white-space: nowrap;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
        }

        [data-testid="stSidebar"] a:hover::after {
            opacity: 1;
            transform: translateY(-50%) translateX(4px);
            box-shadow: 0 0 8px rgba(255,255,255,0.7);
        }

        /* --- Footer Caption --- */
        .footer-caption {
            color: #333;
            text-align: center;
            font-size: 12px;
            margin-top: 25px;
            opacity: 0.8;
        }
        </style>
    """, unsafe_allow_html=True)

    # -------------------------------
    #  App Branding (Using Local Logo)
    # -------------------------------
    logo_path = os.path.join(os.path.dirname(__file__), "../../assets/logo.png")
    if os.path.exists(logo_path):
        st.sidebar.image(logo_path, width=90)
    else:
        # Fallback in case logo missing
        st.sidebar.image(
            "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4f/Emblem_of_Telangana.svg/512px-Emblem_of_Telangana.svg.png",
            width=70
        )

    st.sidebar.markdown(
        "<h2 style='color:#004D40; text-align:center; font-size:20px;'>Telangana Health</h2>",
        unsafe_allow_html=True
    )
    st.sidebar.markdown(
        "<p style='text-align:center; color:#4A148C; font-size:14px;'>Awareness & Analytics</p>",
        unsafe_allow_html=True
    )

    st.sidebar.markdown("---")

    # -------------------------------
    #  Dynamic Page Navigation (with Glowing Tooltip)
    # -------------------------------
    st.sidebar.markdown("<p style='color:#004D40;font-weight:600;margin-top:15px;'> Navigate Pages</p>", unsafe_allow_html=True)

    # Detect current page filename
    current_page = os.path.basename(st.session_state.get("_page_script_run_context", {}).get("page_script_path", ""))

    # Define pages and tooltips
    pages = {
        "0_Home_Dashboard.py": (" Home Dashboard", "Go to Home Dashboard"),
        "1_Health_Awareness.py": (" Health Awareness", "View Health Awareness Insights"),
        "2_Analytics_Dashboard.py": (" Analytics Dashboard", "Explore Health Data Analytics"),
        "3_Chat_Assistant.py": (" Chat Assistant", "Chat with AI Health Assistant"),
        "4_Message_Center.py": (" Message Center", "Send Health Messages via Twilio"),
    }

    # Render page links with glowing tooltips
    for file_name, (label, tooltip) in pages.items():
        active = "true" if current_page == file_name else "false"
        st.sidebar.markdown(
            f"<a href='#{file_name}' data-active='{active}' data-tooltip='{tooltip}'>{label}</a>",
            unsafe_allow_html=True
        )

    st.sidebar.markdown("---")

    # -------------------------------
    # ℹ About Section
    # -------------------------------
    st.sidebar.markdown("<p style='color:#004D40;font-weight:600;'>ℹ About App</p>", unsafe_allow_html=True)
    st.sidebar.info(
        """
         **Telangana Health Awareness App**
        - District-level analytics  
        - AI chatbot for awareness  
        - Multilingual messaging  
        - WhatsApp/SMS integration  

         Developed by **Team 18**  
          Built with Streamlit
        """
    )

    # -------------------------------
    #  Footer
    # -------------------------------
    st.sidebar.markdown(
        "<p class='footer-caption'>© 2025 Telangana Health Awareness | Streamlit Dashboard</p>",
        unsafe_allow_html=True
    )
