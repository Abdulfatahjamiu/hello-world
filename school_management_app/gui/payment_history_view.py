import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import os
import csv

# Add the parent directory to the path to import the controller
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.payment_controller import get_all_payments
from modules.payment_receipt import generate_payment_receipt

class PaymentHistoryView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Payment History")
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.load_payments()

    def create_widgets(self):
        self.columns = ("ID", "Student", "Amount", "Account", "Date", "Academic Year", "Term")
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.column("ID", width=30)

        self.tree.pack(fill="both", expand=True)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        self.refresh_button = tk.Button(button_frame, text="Refresh", command=self.load_payments)
        self.refresh_button.pack(side="left", padx=5)

        self.generate_receipt_button = tk.Button(button_frame, text="Generate Receipt", command=self.generate_receipt)
        self.generate_receipt_button.pack(side="left", padx=5)

        self.export_button = tk.Button(button_frame, text="Export to CSV", command=self.export_to_csv)
        self.export_button.pack(side="left", padx=5)

    def load_payments(self):
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Load new data
        self.payments = get_all_payments()
        for payment in self.payments:
            self.tree.insert("", "end", values=payment)

    def generate_receipt(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a payment from the list.")
            return

        item = self.tree.item(selected_item)
        payment_data = item['values']

        payment_id = payment_data[0]
        student_name = payment_data[1]
        amount = payment_data[2]
        account = payment_data[3]
        payment_date = payment_data[4]

        file_name = generate_payment_receipt(payment_id, student_name, amount, account, payment_date)

        if file_name:
            messagebox.showinfo("Success", f"Payment receipt generated successfully: {file_name}")
        else:
            messagebox.showerror("Error", "Failed to generate payment receipt.")

    def export_to_csv(self):
        if not self.payments:
            messagebox.showerror("Error", "No data to export.")
            return

        try:
            with open("payment_history_report.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self.columns)
                writer.writerows(self.payments)
            messagebox.showinfo("Success", "Report exported to payment_history_report.csv")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {e}")


if __name__ == '__main__':
    root = tk.Tk()
    app = PaymentHistoryView(master=root)
    app.mainloop()
