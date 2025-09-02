from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

def generate_payment_receipt(payment_id, student_name, amount, account, payment_date):
    """
    Generates a PDF payment receipt.
    """
    try:
        file_name = f"payment_receipt_{payment_id}.pdf"
        c = canvas.Canvas(file_name, pagesize=letter)
        width, height = letter

        # School Logo (placeholder)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2.0, height - 1*inch, "Future Leaders Academy")

        # Title
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width / 2.0, height - 1.5*inch, "Payment Receipt")

        # Details
        c.setFont("Helvetica", 12)
        c.drawString(1*inch, height - 2*inch, f"Receipt No: {payment_id}")
        c.drawString(1*inch, height - 2.2*inch, f"Date: {payment_date}")
        c.drawString(1*inch, height - 2.6*inch, f"Received from: {student_name}")
        c.drawString(1*inch, height - 2.8*inch, f"Amount: ${amount:.2f}")
        c.drawString(1*inch, height - 3.0*inch, f"For: {account}")

        # Thank you message
        c.drawCentredString(width / 2.0, height - 4*inch, "Thank you for your payment!")

        c.save()
        return file_name
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None
