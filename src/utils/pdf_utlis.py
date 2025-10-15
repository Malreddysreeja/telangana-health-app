from fpdf import FPDF
import os

def create_pdf(district, disease, message_en, message_translated, target_lang):
    pdf = FPDF()
    pdf.add_page()

    # ✅ Path to your font file
    fonts_path = os.path.join(os.path.dirname(__file__), "../../fonts/DejaVuSans.ttf")

    # ✅ Add Unicode font
    pdf.add_font("DejaVu", "", fonts_path, uni=True)
    pdf.set_font("DejaVu", "", 14)

    pdf.cell(200, 10, txt="Telangana Health Awareness Report", ln=True, align="C")
    pdf.ln(10)
    pdf.multi_cell(0, 10, f"District: {district}")
    pdf.multi_cell(0, 10, f"Most Reported Disease: {disease}")
    pdf.multi_cell(0, 10, f"Awareness Message (English): {message_en}")
    pdf.ln(5)
    pdf.multi_cell(0, 10, f"Awareness Message ({target_lang.upper()}): {message_translated}")

    output_path = f"{district}_Health_Awareness.pdf"
    pdf.output(output_path)
    return output_path
