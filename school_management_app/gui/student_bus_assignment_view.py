import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import os
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from core.student_bus_controller import assign_student_to_route, get_all_assignments, get_route_names
from core.student_controller import get_student_names
from core.transport_schedule import generate_transport_schedule

import csv


class StudentBusAssignmentView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Assign Student to Bus Route")
        self.pack(padx=20, pady=20)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        form_frame = tk.LabelFrame(self, text="Assign Student", padx=10, pady=10)
        form_frame.pack(fill="x", expand="yes", padx=10, pady=5)

        tk.Label(form_frame, text="Student:").grid(row=0, column=0, sticky=tk.W)
        self.student_var = tk.StringVar()
        self.student_dropdown = ttk.Combobox(form_frame, textvariable=self.student_var, width=28, state="readonly")
        self.student_dropdown.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Route:").grid(row=1, column=0, sticky=tk.W)
        self.route_var = tk.StringVar()
        self.route_dropdown = ttk.Combobox(form_frame, textvariable=self.route_var, width=28, state="readonly")
        self.route_dropdown.grid(row=1, column=1, pady=5)

        self.assign_button = tk.Button(form_frame, text="Assign", command=self.assign)
        self.assign_button.grid(row=2, column=0, columnspan=2, pady=10)

        table_frame = tk.LabelFrame(self, text="Current Assignments", padx=10, pady=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.columns = ("Student", "Route", "Bus Number", "Driver")
        self.tree = ttk.Treeview(table_frame, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        button_frame = tk.Frame(table_frame)
        button_frame.pack(pady=10)
        self.refresh_button = tk.Button(button_frame, text="Refresh", command=self.load_assignments)
        self.refresh_button.pack(side="left", padx=5)
        self.export_button = tk.Button(button_frame, text="Export to CSV", command=self.export_to_csv)
        self.export_button.pack(side="left", padx=5)
        self.generate_schedule_button = tk.Button(button_frame, text="Generate Schedule", command=self.generate_schedule)
        self.generate_schedule_button.pack(side="left", padx=5)

    def load_data(self):
        students = get_student_names()
        self.student_map = {f"{name} (ID: {sid})": sid for sid, name in students}
        self.student_dropdown['values'] = list(self.student_map.keys())

        routes = get_route_names()
        self.route_map = {f"{name} (ID: {rid})": rid for rid, name in routes}
        self.route_dropdown['values'] = list(self.route_map.keys())

        self.load_assignments()

    def load_assignments(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.assignments = get_all_assignments()
        for assignment in self.assignments:
            display_data = (assignment[2], assignment[3], assignment[4], assignment[5])
            self.tree.insert("", "end", values=display_data)

    def assign(self):
        student_info = self.student_var.get()
        route_info = self.route_var.get()
        if not all([student_info, route_info]):
            messagebox.showerror("Error", "All fields are required.")
            return

        student_id = self.student_map.get(student_info)
        route_id = self.route_map.get(route_info)

        if assign_student_to_route(student_id, route_id):
            messagebox.showinfo("Success", "Student assigned to route successfully!")
            self.load_assignments()
            self.student_var.set('')
            self.route_var.set('')
        else:
            messagebox.showerror("Error", "Failed to assign student to route.")

    def export_to_csv(self):
        if not hasattr(self, 'assignments') or not self.assignments:
            messagebox.showerror("Error", "No data to export.")
            return
        try:
            with open("bus_assignments_report.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self.columns)
                display_assignments = [ (a[2], a[3], a[4], a[5]) for a in self.assignments]
                writer.writerows(display_assignments)
            messagebox.showinfo("Success", "Report exported to bus_assignments_report.csv")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {e}")
            
    def generate_schedule(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an assignment from the list.")
            return

        item = self.tree.item(selected_item)
        assignment_data = item['values']

        student_name = assignment_data[0]
        route_name = assignment_data[1]
        bus_number = assignment_data[2]
        driver_name = assignment_data[3]

        file_name = generate_transport_schedule(student_name, route_name, bus_number, driver_name)

        if file_name:
            messagebox.showinfo("Success", f"Transport schedule generated successfully: {file_name}")
        else:
            messagebox.showerror("Error", "Failed to generate transport schedule.")

if __name__ == '__main__':
    root = tk.Tk()
    app = StudentBusAssignmentView(master=root)
    app.mainloop()
