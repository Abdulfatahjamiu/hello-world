import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import os
import re

# Add the parent directory to the path to import the controller
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.student_controller import get_student_names
from modules.payment_controller import add_payment

class PaymentView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Record Payment")
        self.pack(padx=20, pady=20)
        self.create_widgets()
        self.load_students()

    def create_widgets(self):
        # Student
        self.student_label = tk.Label(self, text="Student:")
        self.student_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.student_var = tk.StringVar()
        self.student_dropdown = ttk.Combobox(self, textvariable=self.student_var, width=28, state="readonly")
        self.student_dropdown.grid(row=0, column=1)

        # Amount
        self.amount_label = tk.Label(self, text="Amount:")
        self.amount_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.amount_entry = tk.Entry(self, width=30)
        self.amount_entry.grid(row=1, column=1)

        # Account
        self.account_label = tk.Label(self, text="Account:")
        self.account_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.account_var = tk.StringVar()
        self.account_dropdown = ttk.Combobox(self, textvariable=self.account_var, values=["School Fees", "Materials"], width=28, state="readonly")
        self.account_dropdown.grid(row=2, column=1)

        # Payment Date
        self.date_label = tk.Label(self, text="Payment Date (YYYY-MM-DD):")
        self.date_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        self.date_entry = tk.Entry(self, width=30)
        self.date_entry.grid(row=3, column=1)

        # Academic Year
        self.year_label = tk.Label(self, text="Academic Year:")
        self.year_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        self.year_var = tk.StringVar()
        self.year_dropdown = ttk.Combobox(self, textvariable=self.year_var, values=["2023/2024", "2024/2025", "2025/2026"], width=28, state="readonly")
        self.year_dropdown.grid(row=4, column=1)

        # Term
        self.term_label = tk.Label(self, text="Term:")
        self.term_label.grid(row=5, column=0, sticky=tk.W, pady=5)
        self.term_var = tk.StringVar()
        self.term_dropdown = ttk.Combobox(self, textvariable=self.term_var, values=["First Term", "Second Term", "Third Term"], width=28, state="readonly")
        self.term_dropdown.grid(row=5, column=1)

        # Submit Button
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_form)
        self.submit_button.grid(row=6, column=0, columnspan=2, pady=10)

    def load_students(self):
        students = get_student_names()
        self.student_dropdown['values'] = [f"{name} (ID: {sid})" for sid, name in students]

    def submit_form(self):
        student_info = self.student_var.get()
        amount = self.amount_entry.get()
        account = self.account_var.get()
        payment_date = self.date_entry.get()
        academic_year = self.year_var.get()
        term = self.term_var.get()

        if not all([student_info, amount, account, payment_date, academic_year, term]):
            messagebox.showerror("Error", "All fields are required.")
            return

        # Extract student ID from the selected string
        match = re.search(r'\(ID: (\d+)\)', student_info)
        if not match:
            messagebox.showerror("Error", "Invalid student selected.")
            return
        student_id = int(match.group(1))

        if add_payment(student_id, float(amount), account, payment_date, academic_year, term):
            messagebox.showinfo("Success", "Payment recorded successfully!")
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to record payment.")

    def clear_form(self):
        self.student_var.set('')
        self.amount_entry.delete(0, tk.END)
        self.account_var.set('')
        self.date_entry.delete(0, tk.END)
        self.year_var.set('')
        self.term_var.set('')


if __name__ == '__main__':
    root = tk.Tk()
    app = PaymentView(master=root)
    app.mainloop()
