# ============================================
#  Telangana Health Chat Assistant (Lavender + Teal Theme)
# ============================================

import os
import streamlit as st
import google.generativeai as genai
from gtts import gTTS
import sys

#  Fix import path dynamically
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../.."))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.utils.sidebar import render_sidebar
from src.utils.ui_theme import apply_global_styles

# -------------------------------
#  PAGE CONFIGURATION
# -------------------------------
st.set_page_config(page_title=" Health Chat Assistant", page_icon="", layout="wide")

# Apply global Lavender + Teal theme
apply_global_styles()

# Render sidebar
render_sidebar()

# -------------------------------
#  Custom Page Styling
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

        .chat-container {
            max-width: 900px;
            margin: auto;
            padding: 25px;
            background-color: #FFFFFF;
            border-radius: 18px;
            box-shadow: 0px 6px 15px rgba(0,0,0,0.1);
            display: flex;
            flex-direction: column;
            gap: 10px;
            animation: fadeIn 1s ease-in-out;
        }

        .user-bubble {
            background-color: #D1C4E9;
            color: #333;
            padding: 12px 16px;
            border-radius: 15px 15px 0px 15px;
            width: fit-content;
            align-self: flex-end;
            margin-left: auto;
        }

        .bot-bubble {
            background-color: #B2DFDB;
            color: #333;
            padding: 12px 16px;
            border-radius: 15px 15px 15px 0px;
            width: fit-content;
            align-self: flex-start;
            margin-right: auto;
        }

        .header-title {
            text-align: center;
            color: #00695C;
            font-size: 34px;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .header-subtitle {
            text-align: center;
            color: #5B4B8A;
            font-size: 17px;
            margin-bottom: 25px;
        }

        audio {
            width: 100%;
            margin-top: 10px;
        }

        .footer {
            text-align: center;
            color: #777;
            font-size: 14px;
            margin-top: 25px;
            padding-bottom: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# -------------------------------
#  Header Section
# -------------------------------
st.markdown("<h1 class='header-title'> Telangana Health Chat Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p class='header-subtitle'>Your personal AI-powered health awareness guide, built with  Gemini & gTTS</p>", unsafe_allow_html=True)

# -------------------------------
#  SETUP GOOGLE GEMINI
# -------------------------------
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.error(" Google API key not found! Please set it using:\n\n`setx GOOGLE_API_KEY \"your_key_here\"`")
    st.stop()

genai.configure(api_key=api_key)
model = genai.GenerativeModel("models/gemini-2.5-flash")

# -------------------------------
#  Initialize chat history
# -------------------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [
        {"role": "assistant", "content": " Hello! I'm your Telangana Health Awareness Assistant. How can I help you today?"}
    ]

# -------------------------------
#  Sidebar Chat Settings
# -------------------------------
with st.sidebar:
    st.markdown("###  Chat Settings")
    st.info(" Powered by Google Gemini 2.5 + gTTS for voice responses.")
    voice_lang = st.radio(" Select Voice Language", ["English", "Telugu"], index=0)

    if st.button(" Clear Chat"):
        st.session_state.chat_history = [
            {"role": "assistant", "content": "🧹 Chat cleared. How can I help you now?"}
        ]
        st.experimental_rerun()

# -------------------------------
#  Chat Container Layout
# -------------------------------
st.markdown("<div class='chat-container'>", unsafe_allow_html=True)

for msg in st.session_state.chat_history:
    if msg["role"] == "user":
        st.markdown(f"<div class='user-bubble'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='bot-bubble'>{msg['content']}</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# -------------------------------
#  Handle user input
# -------------------------------
user_input = st.chat_input("Ask me anything about diseases, prevention, or health awareness...")

if user_input:
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    st.markdown(f"<div class='user-bubble'>{user_input}</div>", unsafe_allow_html=True)

    try:
        with st.spinner("Thinking ..."):
            context = (
                "You are a Telangana Health Awareness Assistant. "
                "Provide helpful, respectful responses about health awareness, "
                "disease prevention, and hygiene. If users mention emergencies, advise them to consult a doctor."
            )

            response = model.generate_content(context + "\nUser: " + user_input)
            reply = response.text.strip()

            st.session_state.chat_history.append({"role": "assistant", "content": reply})
            st.markdown(f"<div class='bot-bubble'>{reply}</div>", unsafe_allow_html=True)

            #  Voice Output
            try:
                lang_code = "en" if voice_lang == "English" else "te"
                tts = gTTS(reply, lang=lang_code)
                audio_path = os.path.join(os.getcwd(), "reply_audio.mp3")
                tts.save(audio_path)
                st.audio(audio_path, format="audio/mp3", start_time=0)
            except Exception as audio_err:
                st.warning(f" Could not generate audio: {audio_err}")

    except Exception as e:
        st.error(f" Something went wrong: {e}")

# -------------------------------
#  Footer
# -------------------------------
st.markdown("""
    <div class='footer'>
        Developed with  by <b>Team 18</b> | Telangana Health Awareness 2025
    </div>
""", unsafe_allow_html=True)
