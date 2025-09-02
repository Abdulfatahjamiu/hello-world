from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch

def generate_transport_schedule(student_name, route_name, bus_number, driver_name):
    """
    Generates a PDF transport schedule for a student.
    """
    try:
        file_name = f"transport_schedule_{student_name.replace(' ', '_')}.pdf"
        c = canvas.Canvas(file_name, pagesize=letter)
        width, height = letter

        # School Logo (placeholder)
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width / 2.0, height - 1*inch, "Future Leaders Academy")

        # Title
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width / 2.0, height - 1.5*inch, "Transport Schedule")

        # Student Name
        c.setFont("Helvetica-Bold", 12)
        c.drawString(1*inch, height - 2.5*inch, f"Student: {student_name}")

        # Details
        c.setFont("Helvetica", 12)
        c.drawString(1*inch, height - 3*inch, f"Route: {route_name}")
        c.drawString(1*inch, height - 3.2*inch, f"Bus Number: {bus_number}")
        c.drawString(1*inch, height - 3.4*inch, f"Driver: {driver_name}")

        # Note
        c.drawString(1*inch, height - 4*inch, "Please be at your pickup point on time.")

        c.save()
        return file_name
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None
