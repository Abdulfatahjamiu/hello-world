from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

def generate_admission_letter(student_name, class_name, registration_date, parent_name, gender):
    """
    Generates a PDF admission letter for a student.
    """
    try:
        file_name = f"admission_letter_{student_name.replace(' ', '_')}.pdf"
        c = canvas.Canvas(file_name, pagesize=letter)
        width, height = letter

        # School Logo (placeholder)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2.0, height - 1*inch, "Future Leaders Academy")

        # Title
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width / 2.0, height - 1.5*inch, "Admission Letter")

        # Date
        c.setFont("Helvetica", 12)
        c.drawString(1*inch, height - 2*inch, f"Date: {registration_date}")

        # Addressed to Parent
        c.drawString(1*inch, height - 2.5*inch, f"Dear Mr./Mrs. {parent_name},")

        # Body
        text = c.beginText(1*inch, height - 3*inch)
        text.setFont("Helvetica", 12)
        pronoun = "he/she"
        if gender.lower() == 'male':
            pronoun = "he"
        elif gender.lower() == 'female':
            pronoun = "she"

        text.textLine(f"We are pleased to inform you that your child, {student_name}, has been admitted to")
        text.textLine(f"Future Leaders Academy in Class {class_name}. The registration was completed on {registration_date}.")
        text.textLine(f"We believe {pronoun} will be a great addition to our school.")
        text.textLine("")
        text.textLine("We are excited to have you as part of our school community.")
        text.textLine("Please feel free to contact us if you have any questions.")
        c.drawText(text)

        # Sincerely
        c.drawString(1*inch, height - 5*inch, "Sincerely,")
        c.drawString(1*inch, height - 5.2*inch, "The Admissions Office")

        c.save()
        return file_name
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None
