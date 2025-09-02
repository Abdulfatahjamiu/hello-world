import tkinter as tk
from tkinter import ttk
import sys
import os
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Add the parent directory to the path to import the controller
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.dashboard_controller import get_dashboard_stats
# Import all the other views for navigation
from .preregistration_view import PreregistrationView
from .parent_list_view import ParentListView
from .student_registration_view import StudentRegistrationView
from .student_list_view import StudentListView
from .payment_view import PaymentView
from .payment_history_view import PaymentHistoryView
from .payment_report_view import PaymentReportView
from .bus_view import BusView
from .driver_view import DriverView
from .route_view import RouteView
from .student_bus_assignment_view import StudentBusAssignmentView
from .pickup_dropoff_view import PickupDropoffView
from .academic_calendar_view import AcademicCalendarView
from .class_management_view import ClassManagementView
from .student_class_assignment_view import StudentClassAssignmentView


class DashboardView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("School Management Dashboard")
        # Make the window larger
        self.master.geometry("1200x800")
        self.pack(fill="both", expand=True)

        self.create_widgets()
        self.load_stats()

    def create_widgets(self):
        # Main layout
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand=True)

        # Sidebar
        self.sidebar = tk.Frame(self.main_frame, width=200, bg="#2c3e50")
        self.sidebar.pack(side="left", fill="y")

        # Main Content Area
        self.content_area = tk.Frame(self.main_frame, bg="#ecf0f1")
        self.content_area.pack(side="right", fill="both", expand=True)

        # --- Sidebar Buttons ---
        self.create_sidebar_buttons()

        # --- Content Area Widgets ---
        self.create_content_widgets()

    def create_sidebar_buttons(self):
        buttons = {
            "Dashboard": self.load_stats,
            "Parent Preregistration": lambda: self.open_view(PreregistrationView),
            "View Parents": lambda: self.open_view(ParentListView),
            "Student Registration": lambda: self.open_view(StudentRegistrationView),
            "View Students": lambda: self.open_view(StudentListView),
            "Record Payment": lambda: self.open_view(PaymentView),
            "Payment History": lambda: self.open_view(PaymentHistoryView),
            "Payment Reports": lambda: self.open_view(PaymentReportView),
            "Manage Buses": lambda: self.open_view(BusView),
            "Manage Drivers": lambda: self.open_view(DriverView),
            "Manage Routes": lambda: self.open_view(RouteView),
            "Assign Student to Bus": lambda: self.open_view(StudentBusAssignmentView),
            "Bus Pickup/Drop-off": lambda: self.open_view(PickupDropoffView),
            "Academic Calendar": lambda: self.open_view(AcademicCalendarView),
            "Class Management": lambda: self.open_view(ClassManagementView),
            "Assign Student to Class": lambda: self.open_view(StudentClassAssignmentView),
        }

        for text, command in buttons.items():
            btn = tk.Button(self.sidebar, text=text, command=command, bg="#34495e", fg="white", relief="flat", anchor="w", padx=10, pady=10)
            btn.pack(fill="x", pady=2)

    def create_content_widgets(self):
        # This frame will hold the dashboard widgets
        self.dashboard_frame = tk.Frame(self.content_area, bg="#ecf0f1")

        # Stats Frame
        stats_frame = tk.Frame(self.dashboard_frame, bg="#ecf0f1")
        stats_frame.pack(fill="x", pady=10, padx=10)

        self.total_students_label = self.create_stat_box(stats_frame, "Total Students")
        self.total_payments_label = self.create_stat_box(stats_frame, "Total Payments")
        self.pending_prereg_label = self.create_stat_box(stats_frame, "Pending Pre-registrations")

        # Chart Frame
        chart_frame = tk.Frame(self.dashboard_frame, bg="#ecf0f1")
        chart_frame.pack(fill="both", expand=True, pady=10, padx=10)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=chart_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.dashboard_frame.pack(fill="both", expand=True)

    def create_stat_box(self, parent, title):
        box = tk.Frame(parent, bg="white", relief="groove", borderwidth=2)
        box.pack(side="left", fill="x", expand=True, padx=10)
        title_label = tk.Label(box, text=title, bg="white", font=("Arial", 12, "bold"))
        title_label.pack(pady=(10, 0))
        value_label = tk.Label(box, text="0", bg="white", font=("Arial", 24, "bold"))
        value_label.pack(pady=(0, 10))
        return value_label

    def load_stats(self):
        stats = get_dashboard_stats()
        self.total_students_label.config(text=stats.get("total_students", 0))
        self.total_payments_label.config(text=f"${stats.get('total_payments', 0):,.2f}")
        self.pending_prereg_label.config(text=stats.get("pending_preregistrations", 0))

        # Update chart
        self.ax.clear()
        breakdown = stats.get("payment_breakdown", [])
        if breakdown:
            labels = [item[0] for item in breakdown]
            sizes = [item[1] for item in breakdown]
            self.ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
            self.ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
            self.ax.set_title("Payment Breakdown by Account")
        else:
            self.ax.text(0.5, 0.5, "No payment data available", horizontalalignment='center', verticalalignment='center')

        self.canvas.draw()

    def open_view(self, ViewClass):
        new_window = tk.Toplevel(self.master)
        ViewClass(new_window)

if __name__ == '__main__':
    root = tk.Tk()
    app = DashboardView(master=root)
    app.mainloop()
