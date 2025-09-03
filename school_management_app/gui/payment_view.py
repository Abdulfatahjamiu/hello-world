import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import os
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from core.student_controller import get_student_names
from core.payment_controller import add_payment

class PaymentView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Record Payment")
        self.pack(padx=20, pady=20)
        self.create_widgets()
        self.load_students()

    def create_widgets(self):
        form_frame = tk.Frame(self)
        form_frame.pack()

        # Student Dropdown
        tk.Label(form_frame, text="Student:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.student_var = tk.StringVar()
        self.student_dropdown = ttk.Combobox(form_frame, textvariable=self.student_var, state="readonly")
        self.student_dropdown.grid(row=0, column=1, pady=5)

        # Other fields
        self.entries = {}
        labels = {"amount": "Amount:", "payment_date": "Payment Date (YYYY-MM-DD):"}
        for i, (key, text) in enumerate(labels.items(), 1):
            tk.Label(form_frame, text=text).grid(row=i, column=0, sticky=tk.W, pady=5)
            entry = tk.Entry(form_frame, width=30)
            entry.grid(row=i, column=1, pady=5)
            self.entries[key] = entry

        # Account Dropdown
        tk.Label(form_frame, text="Account:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.account_var = tk.StringVar()
        self.account_dropdown = ttk.Combobox(form_frame, textvariable=self.account_var, values=["School Fees", "Materials"], state="readonly")
        self.account_dropdown.grid(row=3, column=1, pady=5)

        # Academic Year/Term Dropdowns
        tk.Label(form_frame, text="Academic Year:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.year_var = tk.StringVar()
        self.year_dropdown = ttk.Combobox(form_frame, textvariable=self.year_var, values=["2023/2024", "2024/2025", "2025/2026"], state="readonly")
        self.year_dropdown.grid(row=4, column=1, pady=5)

        tk.Label(form_frame, text="Term:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.term_var = tk.StringVar()
        self.term_dropdown = ttk.Combobox(form_frame, textvariable=self.term_var, values=["First Term", "Second Term", "Third Term"], state="readonly")
        self.term_dropdown.grid(row=5, column=1, pady=5)

        self.submit_button = tk.Button(self, text="Submit", command=self.submit_form)
        self.submit_button.pack(pady=10)

    def load_students(self):
        self.students = get_student_names()
        self.student_dropdown['values'] = [f"{name} (ID: {sid})" for sid, name in self.students]

    def submit_form(self):
        student_info = self.student_var.get()
        amount_str = self.entries['amount'].get()
        account = self.account_var.get()
        payment_date = self.entries['payment_date'].get()
        academic_year = self.year_var.get()
        term = self.term_var.get()

        if not all([student_info, amount_str, account, payment_date, academic_year, term]):
            messagebox.showerror("Error", "All fields are required.")
            return

        try:
            amount = float(amount_str.replace(',', ''))
        except ValueError:
            messagebox.showerror("Error", "Invalid amount. Please enter a valid number.")
            return

        match = re.search(r'\(ID: (\d+)\)', student_info)
        if not match:
            messagebox.showerror("Error", "Invalid student selected.")
            return
        student_id = int(match.group(1))

        if add_payment(student_id, amount, account, payment_date, academic_year, term):
            messagebox.showinfo("Success", "Payment recorded successfully!")
            self.master.destroy() # Close window on success
        else:
            messagebox.showerror("Error", "Failed to record payment.")

if __name__ == '__main__':
    root = tk.Tk()
    app = PaymentView(master=root)
    app.mainloop()
