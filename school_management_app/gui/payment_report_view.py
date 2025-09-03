import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import os
import csv
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from core.payment_controller import get_payments_by_filter
from core.student_controller import get_student_names

class PaymentReportView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Payment Reports")
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.create_widgets()
        self.load_students()

    def create_widgets(self):
        filter_frame = tk.LabelFrame(self, text="Filters", padx=10, pady=10)
        filter_frame.pack(fill="x", expand="yes", padx=10, pady=5)

        # Filters
        self.student_label = tk.Label(filter_frame, text="Student:")
        self.student_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.student_var = tk.StringVar()
        self.student_dropdown = ttk.Combobox(filter_frame, textvariable=self.student_var, width=28, state="readonly")
        self.student_dropdown.grid(row=0, column=1, padx=5)

        self.start_date_label = tk.Label(filter_frame, text="Start Date (YYYY-MM-DD):")
        self.start_date_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.start_date_entry = tk.Entry(filter_frame, width=30)
        self.start_date_entry.grid(row=1, column=1, padx=5)

        self.end_date_label = tk.Label(filter_frame, text="End Date (YYYY-MM-DD):")
        self.end_date_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.end_date_entry = tk.Entry(filter_frame, width=30)
        self.end_date_entry.grid(row=2, column=1, padx=5)

        self.account_label = tk.Label(filter_frame, text="Account:")
        self.account_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        self.account_var = tk.StringVar()
        self.account_dropdown = ttk.Combobox(filter_frame, textvariable=self.account_var, values=["", "School Fees", "Materials"], width=28, state="readonly")
        self.account_dropdown.grid(row=3, column=1, padx=5)

        self.filter_button = tk.Button(filter_frame, text="Apply Filters", command=self.apply_filters)
        self.filter_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Results table
        results_frame = tk.LabelFrame(self, text="Results", padx=10, pady=10)
        results_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.columns = ("ID", "Student", "Amount", "Account", "Date", "Academic Year", "Term")
        self.tree = ttk.Treeview(results_frame, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        self.export_button = tk.Button(self, text="Export to CSV", command=self.export_to_csv)
        self.export_button.pack(pady=10)

    def load_students(self):
        self.students = get_student_names()
        student_names = [""] + [f"{name} (ID: {sid})" for sid, name in self.students]
        self.student_dropdown['values'] = student_names

    def apply_filters(self):
        student_info = self.student_var.get()
        student_id = None
        if student_info:
            match = re.search(r'\(ID: (\d+)\)', student_info)
            if match:
                student_id = int(match.group(1))

        start_date = self.start_date_entry.get() or None
        end_date = self.end_date_entry.get() or None
        account = self.account_var.get() or None

        self.payments = get_payments_by_filter(student_id=student_id, start_date=start_date, end_date=end_date, account=account)

        for row in self.tree.get_children():
            self.tree.delete(row)
        for payment in self.payments:
            self.tree.insert("", "end", values=payment)

    def export_to_csv(self):
        if not hasattr(self, 'payments') or not self.payments:
            messagebox.showerror("Error", "No data to export.")
            return

        try:
            with open("payment_report.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self.columns)
                writer.writerows(self.payments)
            messagebox.showinfo("Success", "Report exported to payment_report.csv")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = PaymentReportView(master=root)
    app.mainloop()
