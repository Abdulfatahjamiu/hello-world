import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import os
import csv

# Add the parent directory to the path to import the controller
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.driver_controller import add_driver, get_all_drivers

class DriverView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Manage Drivers")
        self.pack(padx=20, pady=20)
        self.create_widgets()
        self.load_drivers()

    def create_widgets(self):
        # Form to add a new driver
        form_frame = tk.LabelFrame(self, text="Add New Driver", padx=10, pady=10)
        form_frame.pack(fill="x", expand="yes", padx=10, pady=5)

        self.name_label = tk.Label(form_frame, text="Name:")
        self.name_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = tk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1)

        self.phone_label = tk.Label(form_frame, text="Phone Number:")
        self.phone_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.phone_entry = tk.Entry(form_frame, width=30)
        self.phone_entry.grid(row=1, column=1)

        self.license_label = tk.Label(form_frame, text="License Number:")
        self.license_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.license_entry = tk.Entry(form_frame, width=30)
        self.license_entry.grid(row=2, column=1)

        self.add_button = tk.Button(form_frame, text="Add Driver", command=self.add_new_driver)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # Table to display drivers
        table_frame = tk.LabelFrame(self, text="Driver List", padx=10, pady=10)
        table_frame.pack(fill="both", expand="yes", padx=10, pady=5)

        self.columns = ("ID", "Name", "Phone Number", "License Number")
        self.tree = ttk.Treeview(table_frame, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        button_frame = tk.Frame(table_frame)
        button_frame.pack(pady=10)

        self.refresh_button = tk.Button(button_frame, text="Refresh", command=self.load_drivers)
        self.refresh_button.pack(side="left", padx=5)

        self.export_button = tk.Button(button_frame, text="Export to CSV", command=self.export_to_csv)
        self.export_button.pack(side="left", padx=5)

    def load_drivers(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.drivers = get_all_drivers()
        for driver in self.drivers:
            self.tree.insert("", "end", values=driver)

    def add_new_driver(self):
        name = self.name_entry.get()
        phone = self.phone_entry.get()
        license_num = self.license_entry.get()
        if not name or not phone or not license_num:
            messagebox.showerror("Error", "All fields are required.")
            return
        if add_driver(name, phone, license_num):
            messagebox.showinfo("Success", "Driver added successfully!")
            self.load_drivers()
            self.name_entry.delete(0, tk.END)
            self.phone_entry.delete(0, tk.END)
            self.license_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Failed to add driver.")

    def export_to_csv(self):
        if not self.drivers:
            messagebox.showerror("Error", "No data to export.")
            return

        try:
            with open("drivers_report.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self.columns)
                writer.writerows(self.drivers)
            messagebox.showinfo("Success", "Report exported to drivers_report.csv")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = DriverView(master=root)
    app.mainloop()
