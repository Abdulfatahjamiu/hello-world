import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import os
import csv

# Add the parent directory to the path to import the controller
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.bus_controller import add_bus, get_all_buses

class BusView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Manage Buses")
        self.pack(padx=20, pady=20)
        self.create_widgets()
        self.load_buses()

    def create_widgets(self):
        # Form to add a new bus
        form_frame = tk.LabelFrame(self, text="Add New Bus", padx=10, pady=10)
        form_frame.pack(fill="x", expand="yes", padx=10, pady=5)

        self.bus_number_label = tk.Label(form_frame, text="Bus Number:")
        self.bus_number_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.bus_number_entry = tk.Entry(form_frame, width=30)
        self.bus_number_entry.grid(row=0, column=1)

        self.capacity_label = tk.Label(form_frame, text="Capacity:")
        self.capacity_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.capacity_entry = tk.Entry(form_frame, width=30)
        self.capacity_entry.grid(row=1, column=1)

        self.add_button = tk.Button(form_frame, text="Add Bus", command=self.add_new_bus)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Table to display buses
        table_frame = tk.LabelFrame(self, text="Bus List", padx=10, pady=10)
        table_frame.pack(fill="both", expand="yes", padx=10, pady=5)

        self.columns = ("ID", "Bus Number", "Capacity")
        self.tree = ttk.Treeview(table_frame, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        button_frame = tk.Frame(table_frame)
        button_frame.pack(pady=10)

        self.refresh_button = tk.Button(button_frame, text="Refresh", command=self.load_buses)
        self.refresh_button.pack(side="left", padx=5)

        self.export_button = tk.Button(button_frame, text="Export to CSV", command=self.export_to_csv)
        self.export_button.pack(side="left", padx=5)

    def load_buses(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.buses = get_all_buses()
        for bus in self.buses:
            self.tree.insert("", "end", values=bus)

    def add_new_bus(self):
        bus_number = self.bus_number_entry.get()
        capacity = self.capacity_entry.get()
        if not bus_number or not capacity:
            messagebox.showerror("Error", "All fields are required.")
            return
        if add_bus(bus_number, int(capacity)):
            messagebox.showinfo("Success", "Bus added successfully!")
            self.load_buses()
            self.bus_number_entry.delete(0, tk.END)
            self.capacity_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Failed to add bus.")

    def export_to_csv(self):
        if not self.buses:
            messagebox.showerror("Error", "No data to export.")
            return

        try:
            with open("buses_report.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self.columns)
                writer.writerows(self.buses)
            messagebox.showinfo("Success", "Report exported to buses_report.csv")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = BusView(master=root)
    app.mainloop()
