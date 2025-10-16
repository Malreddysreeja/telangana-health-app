# ============================================
#  Telangana Health Awareness Streamlit App
# (with Lavender–Teal Theme + Logo Header)
# ============================================

import os
import pandas as pd
import streamlit as st
from deep_translator import GoogleTranslator
from fpdf import FPDF
from src.utils.ui_theme import apply_global_styles

# -------------------------------
#  Page Configuration
# -------------------------------
st.set_page_config(
    page_title=" Telangana Health Awareness",
    page_icon="src/assets/logo.png",
    layout="wide"
)

# Apply global theme
apply_global_styles()

# -------------------------------
#  Header Section
# -------------------------------
st.markdown(f"""
    <div style='display:flex; align-items:center; justify-content:center; gap:12px;'>
        <img src='src/assets/logo.png' width='60'>
        <h1 style='color:#004D40; font-family:Poppins;'>Telangana Health Awareness Dashboard</h1>
    </div>
    <p style='text-align:center; color:#5B4B8A;'>Monitor health trends, awareness messages, and preventive guidance for Telangana districts.</p>
""", unsafe_allow_html=True)

# -------------------------------
# Simplified paths for Streamlit Cloud
fonts_path = os.path.join("data", "fonts", "DejaVuSans.ttf")
bold_fonts_path = os.path.join("data", "fonts", "DejaVuSans-Bold.ttf")
dataset_path = os.path.join("data", "raw", "telangana_health_dataset2025.csv")
icons_path = os.path.join("data", "icons")


#  Font check
if not os.path.exists(fonts_path) or not os.path.exists(bold_fonts_path):
    st.warning("Font files not found. Using default Streamlit fonts instead.")
    fonts_path = bold_fonts_path = None


# -------------------------------
#  District-to-Language Mapping
# -------------------------------
language_map = {district: "te" for district in [
    "Adilabad", "Bhadradri Kothagudem", "Jagtial", "Jangaon", "Jayashankar Bhupalpally", "Jogulamba Gadwal",
    "Kamareddy", "Karimnagar", "Khammam", "Komaram Bheem Asifabad", "Mahabubabad", "Mahabubnagar",
    "Mancherial", "Medak", "Medchal Malkajgiri", "Mulugu", "Nagarkurnool", "Nalgonda", "Narayanpet",
    "Nirmal", "Nizamabad", "Peddapalli", "Rajanna Sircilla", "Rangareddy", "Sangareddy", "Siddipet",
    "Suryapet", "Vikarabad", "Wanaparthy", "Warangal Rural", "Warangal Urban", "Yadadri Bhuvanagiri"
]}
language_map["Hyderabad"] = "ur"
language_map["default"] = "en"

# -------------------------------
#  Load Dataset
# -------------------------------
@st.cache_data
def load_data():
    if not os.path.exists(dataset_path):
        st.error(f"Dataset not found at {dataset_path}")
        return pd.DataFrame()
    return pd.read_csv(dataset_path)

df = load_data()

if df.empty:
    st.stop()
else:
    st.success(" Dataset loaded successfully!")

# -------------------------------
#  District Selection
# -------------------------------
districts = sorted(df["District"].dropna().unique())
user_district = st.selectbox(" Select your District:", districts)

# -------------------------------
#  Disease Insights
# -------------------------------
if user_district:
    district_data = df[df["District"] == user_district]

    if not district_data.empty:
        top_disease = (
            district_data.groupby("Disease")["Cases"]
            .sum()
            .sort_values(ascending=False)
            .index[0]
        )

        st.subheader(f" {user_district} — Most Reported Disease: {top_disease}")

        awareness_dict = {
            "Dengue": "Avoid mosquito bites, keep surroundings clean, and remove stagnant water.",
            "Malaria": "Use mosquito nets and avoid outdoor activities at dusk.",
            "COVID-19": "Wear masks, wash hands regularly, and maintain social distance.",
            "Cholera": "Drink clean water and maintain good hygiene.",
            "Typhoid": "Eat properly cooked food and avoid street food.",
            "Influenza": "Get vaccinated, wash hands, and avoid close contact when sick.",
        }

        awareness_message = awareness_dict.get(top_disease, "Stay healthy and maintain hygiene to prevent infections.")

        st.write("###  Awareness Message (English):")
        st.info(awareness_message)

        # Translation option
        target_lang = language_map.get(user_district, language_map["default"])
        translated_text = ""
        translate_toggle = st.checkbox(" Translate to Local Language")

        if translate_toggle and target_lang != "en":
            try:
                translated_text = GoogleTranslator(source="auto", target=target_lang).translate(awareness_message)
                st.write(f"###  Awareness Message ({target_lang.upper()}):")
                st.success(translated_text)
            except Exception as e:
                st.warning(f" Translation failed: {e}")

        # -------------------------------
        # 🎬 Educational Video
        # -------------------------------
        media_dict = {
            "Dengue": "https://www.youtube.com/watch?v=Fixp7OAYFfA",
            "Malaria": "https://www.youtube.com/watch?v=8-6KDqcUBC8",
            "COVID-19": "https://www.youtube.com/watch?v=BtN-goy9VOY",
            "Cholera": "https://www.youtube.com/watch?v=8-sqticNg5o&t=67s",
            "Typhoid": "https://www.youtube.com/watch?v=SrCjvP05mlQ&t=31s",
            "Influenza": "https://www.youtube.com/watch?v=mn710cT4xxs&t=11s",
        }

        video_url = media_dict.get(top_disease)
        if video_url:
            st.video(video_url)
        else:
            st.info(" No educational video available for this disease.")

        # -------------------------------
        #  PDF Download
        # -------------------------------
        def create_pdf(district, disease, english_msg, local_msg=None, lang_code=""):
            pdf = FPDF()
            pdf.add_page()

            pdf.add_font("DejaVu", "", fonts_path, uni=True)
            pdf.add_font("DejaVu", "B", bold_fonts_path, uni=True)

            icon_filename = disease.lower().replace(" ", "-") + ".png"
            icon_path = os.path.join(icons_path, icon_filename)
            if os.path.exists(icon_path):
                try:
                    pdf.image(icon_path, x=10, y=pdf.get_y(), w=15, h=15)
                    pdf.set_x(30)
                except Exception:
                    pdf.ln(10)
            else:
                pdf.ln(10)

            pdf.set_font("DejaVu", "B", 18)
            pdf.cell(0, 10, f"Health Awareness — {district}", ln=True, align="C")
            pdf.ln(10)

            pdf.set_font("DejaVu", "B", 14)
            pdf.cell(0, 10, f"Disease: {disease}", ln=True)
            pdf.ln(5)

            pdf.set_font("DejaVu", "", 12)
            pdf.multi_cell(0, 8, f"English Message:\n{english_msg}")
            pdf.ln(5)

            if local_msg:
                pdf.multi_cell(0, 8, f"Message ({lang_code.upper()}):\n{local_msg}")

            pdf_file = os.path.join(os.getcwd(), f"{district}_{disease}_awareness.pdf")
            pdf.output(pdf_file)
            return pdf_file

        pdf_file = create_pdf(user_district, top_disease, awareness_message, translated_text, target_lang)
        with open(pdf_file, "rb") as f:
            st.download_button(
                label=" Download Awareness Info as PDF",
                data=f,
                file_name=os.path.basename(pdf_file),
                mime="application/pdf"
            )

    else:
        st.warning(" No data available for this district.")
