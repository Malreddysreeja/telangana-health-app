from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.image("data/icons/covid-19.png", x=10, y=10, w=30, h=30)
pdf.output("test.pdf")
print("✅ PDF created successfully!")
