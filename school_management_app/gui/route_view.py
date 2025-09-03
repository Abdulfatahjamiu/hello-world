import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import os
import re
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from core.route_controller import add_route, get_all_routes, get_bus_numbers, get_driver_names

class RouteView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Manage Routes")
        self.pack(padx=20, pady=20)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        form_frame = tk.LabelFrame(self, text="Add New Route", padx=10, pady=10)
        form_frame.pack(fill="x", expand="yes", padx=10, pady=5)

        tk.Label(form_frame, text="Route Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = tk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1)

        tk.Label(form_frame, text="Bus:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.bus_var = tk.StringVar()
        self.bus_dropdown = ttk.Combobox(form_frame, textvariable=self.bus_var, state="readonly")
        self.bus_dropdown.grid(row=1, column=1)

        tk.Label(form_frame, text="Driver:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.driver_var = tk.StringVar()
        self.driver_dropdown = ttk.Combobox(form_frame, textvariable=self.driver_var, state="readonly")
        self.driver_dropdown.grid(row=2, column=1)

        self.add_button = tk.Button(form_frame, text="Add Route", command=self.add_new_route)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        table_frame = tk.LabelFrame(self, text="Route List", padx=10, pady=10)
        table_frame.pack(fill="both", expand="yes", padx=10, pady=5)

        self.columns = ("ID", "Name", "Bus Number", "Driver Name")
        self.tree = ttk.Treeview(table_frame, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        button_frame = tk.Frame(table_frame)
        button_frame.pack(pady=10)
        self.refresh_button = tk.Button(button_frame, text="Refresh", command=self.load_routes)
        self.refresh_button.pack(side="left", padx=5)
        self.export_button = tk.Button(button_frame, text="Export to CSV", command=self.export_to_csv)
        self.export_button.pack(side="left", padx=5)

    def load_data(self):
        self.buses = get_bus_numbers()
        self.bus_dropdown['values'] = [f"{bus_num} (ID: {bid})" for bid, bus_num in self.buses]
        self.drivers = get_driver_names()
        self.driver_dropdown['values'] = [f"{name} (ID: {did})" for did, name in self.drivers]
        self.load_routes()

    def load_routes(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.routes = get_all_routes()
        for route in self.routes:
            self.tree.insert("", "end", values=route)

    def add_new_route(self):
        name = self.name_entry.get()
        bus_info = self.bus_var.get()
        driver_info = self.driver_var.get()
        if not all([name, bus_info, driver_info]):
            messagebox.showerror("Error", "All fields are required.")
            return

        bus_id = int(re.search(r'\(ID: (\d+)\)', bus_info).group(1))
        driver_id = int(re.search(r'\(ID: (\d+)\)', driver_info).group(1))

        if add_route(name, bus_id, driver_id):
            messagebox.showinfo("Success", "Route added successfully!")
            self.load_routes()
            self.name_entry.delete(0, tk.END)
            self.bus_var.set('')
            self.driver_var.set('')
        else:
            messagebox.showerror("Error", "Failed to add route.")

    def export_to_csv(self):
        if not hasattr(self, 'routes') or not self.routes:
            messagebox.showerror("Error", "No data to export.")
            return
        try:
            with open("routes_report.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self.columns)
                writer.writerows(self.routes)
            messagebox.showinfo("Success", "Report exported to routes_report.csv")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = RouteView(master=root)
    app.mainloop()
