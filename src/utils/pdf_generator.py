from fpdf import FPDF
import os

def create_pdf(district, disease, message_en, message_te, output_path="output.pdf"):
    pdf = FPDF()
    pdf.add_page()

    # Add fonts for Unicode Telugu support (DejaVu Sans recommended)
    fonts_path = os.path.join(os.path.dirname(__file__), "../../fonts/DejaVuSans.ttf")

    if os.path.exists(fonts_path):
        pdf.add_font("DejaVu", "", fonts_path, uni=True)
        pdf.set_font("DejaVu", "", 14)
    else:
        pdf.set_font("Arial", "B", 14)

    pdf.cell(200, 10, txt=f"Telangana Health Awareness — {district}", ln=True, align="C")
    pdf.ln(10)
    pdf.set_font("DejaVu", "", 12)
    pdf.cell(200, 10, txt=f"Disease: {disease}", ln=True, align="L")
    pdf.ln(10)
    pdf.multi_cell(0, 8, f"English Message:\n{message_en}")
    pdf.ln(8)
    pdf.multi_cell(0, 8, f"Telugu Message:\n{message_te}")

    pdf.output(output_path)
    return output_path
