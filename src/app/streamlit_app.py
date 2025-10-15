import os
import pandas as pd
import streamlit as st
from deep_translator import GoogleTranslator
from fpdf import FPDF

# ------------------------------- #
# 0️⃣ Project Root & Paths
# ------------------------------- #
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
fonts_path = os.path.join(project_root, "data", "fonts", "DejaVuSans.ttf")
bold_fonts_path = os.path.join(project_root, "data", "fonts", "DejaVuSans-Bold.ttf")
dataset_path = os.path.join(project_root, "data", "raw", "telangana_health_dataset2025.csv")
icons_path = os.path.join(project_root, "data", "icons")

# Safety check for fonts
if not os.path.exists(fonts_path) or not os.path.exists(bold_fonts_path):
    st.error(f"Font files not found in {os.path.dirname(fonts_path)}\nPlease place DejaVuSans.ttf and DejaVuSans-Bold.ttf in data/fonts/")
    st.stop()

# ------------------------------- #
# 1️⃣ District-to-Language Mapping
# ------------------------------- #
language_map = {
    "Hyderabad": "ur", "Adilabad": "te", "Bhadradri Kothagudem": "te",
    "Jagtial": "te", "Jangaon": "te", "Jayashankar Bhupalpally": "te",
    "Jogulamba Gadwal": "te", "Kamareddy": "te", "Karimnagar": "te",
    "Khammam": "te", "Komaram Bheem Asifabad": "te", "Mahabubabad": "te",
    "Mahabubnagar": "te", "Mancherial": "te", "Medak": "te",
    "Medchal Malkajgiri": "te", "Mulugu": "te", "Nagarkurnool": "te",
    "Nalgonda": "te", "Narayanpet": "te", "Nirmal": "te",
    "Nizamabad": "te", "Peddapalli": "te", "Rajanna Sircilla": "te",
    "Rangareddy": "te", "Sangareddy": "te", "Siddipet": "te",
    "Suryapet": "te", "Vikarabad": "te", "Wanaparthy": "te",
    "Warangal Rural": "te", "Warangal Urban": "te", "Yadadri Bhuvanagiri": "te",
    "default": "en",
}

# ------------------------------- #
# 2️⃣ Load Dataset
# ------------------------------- #
@st.cache_data
def load_data():
    if not os.path.exists(dataset_path):
        st.error(f"Dataset not found at {dataset_path}")
        return pd.DataFrame()
    return pd.read_csv(dataset_path)

df = load_data()
st.title(" Telangana Health Awareness App")

if df.empty:
    st.stop()
else:
    st.success(" Dataset loaded successfully!")

# ------------------------------- #
# 3️⃣ District Selection
# ------------------------------- #
districts = sorted(df["District"].dropna().unique())
user_district = st.selectbox(" Select your District:", districts)

# ------------------------------- #
# 4️⃣ Filter Data & Top Disease
# ------------------------------- #
if user_district:
    district_data = df[df["District"] == user_district]

    if not district_data.empty:
        top_disease = (
            district_data.groupby("Disease")["Cases"].sum()
            .sort_values(ascending=False)
            .index[0]
        )

        st.subheader(f" {user_district} — Most Reported Disease: {top_disease}")

        # Awareness messages
        awareness_dict = {
            "Dengue": "Avoid mosquito bites, keep surroundings clean, and remove stagnant water.",
            "Malaria": "Use mosquito nets and avoid outdoor activities at dusk.",
            "COVID-19": "Wear masks, wash hands regularly, and maintain social distance.",
            "Cholera": "Drink clean water and maintain good hygiene.",
            "Typhoid": "Eat properly cooked food and avoid street food.",
            "Influenza": "Get vaccinated, wash hands, and avoid close contact when sick.",
        }

        awareness_message = awareness_dict.get(
            top_disease, "Stay healthy and maintain hygiene to prevent infections."
        )

        st.write("###  Awareness Message (English):")
        st.info(awareness_message)

        # Translate toggle
        target_lang = language_map.get(user_district, language_map["default"])
        translated_text = ""
        translate_toggle = st.checkbox(" Translate to Local Language")

        if translate_toggle and target_lang != "en":
            try:
                translated_text = GoogleTranslator(source="auto", target=target_lang).translate(awareness_message)
                st.write(f"###  Awareness Message ({target_lang.upper()}):")
                st.success(translated_text)
            except Exception as e:
                st.warning(f"Translation failed: {e}")

        # Educational videos
        media_dict = {
            "Dengue": {"video": "https://www.youtube.com/watch?v=Fixp7OAYFfA"},
            "Malaria": {"video": "https://www.youtube.com/watch?v=8-6KDqcUBC8"},
            "COVID-19": {"video": "https://www.youtube.com/watch?v=BtN-goy9VOY"},
            "Cholera": {"video": "https://www.youtube.com/watch?v=8-sqticNg5o&t=67s"},
            "Typhoid": {"video": "https://www.youtube.com/watch?v=SrCjvP05mlQ&t=31s"},
            "Influenza": {"video": "https://www.youtube.com/watch?v=mn710cT4xxs&t=11s"},
        }

        video_url = media_dict.get(top_disease, {}).get("video")
        if video_url:
            try:
                st.video(video_url)
            except Exception:
                st.warning(" Video unavailable.")
        else:
            st.info(" No educational video available for this disease.")

        # ------------------------------- #
        # 8️⃣ PDF Download Function (with icons)
        # ------------------------------- #
        def create_pdf(district, disease, english_msg, local_msg=None, lang_code=""):
            pdf = FPDF()
            pdf.add_page()

            # Add fonts
            pdf.add_font("DejaVu", "", fonts_path, uni=True)
            pdf.add_font("DejaVu", "B", bold_fonts_path, uni=True)

            # Optional icon
            icon_filename = disease.lower().replace(" ", "-") + ".png"
            icon_path = os.path.join(icons_path, icon_filename)
            if os.path.exists(icon_path) and os.path.getsize(icon_path) > 0:
                try:
                    pdf.image(icon_path, x=10, y=pdf.get_y(), w=15, h=15)
                    pdf.set_x(30)
                except Exception:
                    pdf.ln(10)
            else:
                pdf.ln(10)

            # Heading
            pdf.set_font("DejaVu", "B", 18)
            pdf.cell(0, 10, f"Health Awareness — {district}", ln=True, align="C")
            pdf.ln(10)

            # Disease
            pdf.set_font("DejaVu", "B", 14)
            pdf.cell(0, 10, f"Disease: {disease}", ln=True)
            pdf.ln(5)

            # English message
            pdf.set_font("DejaVu", "", 12)
            pdf.multi_cell(0, 8, f"English Message:\n{english_msg}")
            pdf.ln(5)

            # Local language message
            if local_msg:
                pdf.multi_cell(0, 8, f"Message ({lang_code.upper()}):\n{local_msg}")

            # Save PDF
            pdf_file = os.path.join(os.getcwd(), f"{district}_{disease}_awareness.pdf")
            pdf.output(pdf_file)
            return pdf_file

        # ------------------------------- #
        # 9️⃣ PDF Download Button
        # ------------------------------- #
        pdf_file = create_pdf(user_district, top_disease, awareness_message, translated_text, target_lang)
        with open(pdf_file, "rb") as f:
            st.download_button(
                label=" Download Awareness Info as PDF",
                data=f,
                file_name=os.path.basename(pdf_file),
                mime="application/pdf"
            )

    else:
        st.warning("No data found for this district.")
