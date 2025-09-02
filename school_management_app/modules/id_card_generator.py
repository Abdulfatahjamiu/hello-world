from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
import os

def generate_id_card(student_name, student_id, student_class, photo_path):
    """
    Generates a PDF ID card for a student.
    """
    try:
        file_name = f"id_card_{student_name.replace(' ', '_')}.pdf"
        c = canvas.Canvas(file_name, pagesize=(3.375*inch, 2.125*inch)) # Credit card size

        # Card background
        c.setFillColor(HexColor("#f0f4f9"))
        c.rect(0, 0, 3.375*inch, 2.125*inch, fill=1, stroke=0)

        # Header
        c.setFillColor(HexColor("#1173d4"))
        c.rect(0, 1.5*inch, 3.375*inch, 0.625*inch, fill=1, stroke=0)
        c.setFillColor(HexColor("#ffffff"))
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(1.6875*inch, 1.8*inch, "SCHOOL NAME")
        c.setFont("Helvetica", 8)
        c.drawCentredString(1.6875*inch, 1.65*inch, "Student ID Card")

        # Photo
        if photo_path and os.path.exists(os.path.join('..', photo_path)):
            try:
                c.drawImage(os.path.join('..', photo_path), 0.25*inch, 0.75*inch, width=1*inch, height=1*inch, preserveAspectRatio=True, anchor='n')
            except Exception as e:
                print(f"Error drawing image on ID card: {e}")
                c.rect(0.25*inch, 0.75*inch, 1*inch, 1*inch, fill=0) # Placeholder box
                c.drawString(0.3*inch, 1.1*inch, "No Photo")
        else:
            c.rect(0.25*inch, 0.75*inch, 1*inch, 1*inch, fill=0) # Placeholder box
            c.drawString(0.3*inch, 1.1*inch, "No Photo")

        # Details
        c.setFillColor(HexColor("#182739"))
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1.5*inch, 1.25*inch, student_name)
        c.setFont("Helvetica", 8)
        c.drawString(1.5*inch, 1.1*inch, f"ID: {student_id}")
        c.drawString(1.5*inch, 0.95*inch, f"Class: {student_class}")

        # Barcode (placeholder)
        # In a real app, you'd use a library to generate a real barcode image
        c.rect(0.25*inch, 0.25*inch, 2.875*inch, 0.3*inch, fill=0)
        c.setFont("Helvetica", 6)
        c.drawCentredString(1.6875*inch, 0.15*inch, f"*{student_id}*")


        c.save()
        return file_name
    except Exception as e:
        print(f"Error generating ID card: {e}")
        return None
