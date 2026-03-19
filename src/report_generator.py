from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import datetime

def generate_pdf(filename, title, lines):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, title)

    c.setFont("Helvetica", 11)
    y = height - 100

    for line in lines:
        c.drawString(50, y, line)
        y -= 20

    c.setFont("Helvetica-Oblique", 9)
    c.drawString(50, 40, f"Generated on {datetime.datetime.now()}")

    c.save()
