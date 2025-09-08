import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from core.student_bus_controller import get_all_assignments, update_pickup_status, update_dropoff_status

class PickupDropoffView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Pickup and Drop-off Log")
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.create_widgets()
        self.load_assignments()

    def create_widgets(self):
        table_frame = tk.LabelFrame(self, text="Student Bus Status", padx=10, pady=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.columns = ("Student", "Route", "Pickup Status", "Drop-off Status")
        self.tree = ttk.Treeview(table_frame, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        self.refresh_button = tk.Button(button_frame, text="Refresh", command=self.load_assignments)
        self.refresh_button.pack(side="left", padx=5)
        self.pickup_button = tk.Button(button_frame, text="Mark Picked Up", command=self.mark_picked_up)
        self.pickup_button.pack(side="left", padx=5)
        self.dropoff_button = tk.Button(button_frame, text="Mark Dropped Off", command=self.mark_dropped_off)
        self.dropoff_button.pack(side="left", padx=5)

    def load_assignments(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.assignments = get_all_assignments()
        for assignment in self.assignments:
            display_data = (assignment[2], assignment[3], assignment[6] or "Pending", assignment[7] or "Pending")
            self.tree.insert("", "end", values=display_data, iid=assignment[0]) # Use student ID as iid

    def get_selected_assignment(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student from the list.")
            return None

        student_id = int(selected_item[0])
        for assignment in self.assignments:
            if assignment[0] == student_id:
                return assignment
        return None

    def mark_picked_up(self):
        assignment = self.get_selected_assignment()
        if assignment:
            student_id, route_id = assignment[0], assignment[1]
            if update_pickup_status(student_id, route_id, "Picked Up"):
                self.load_assignments()
            else:
                messagebox.showerror("Error", "Failed to update pickup status.")

    def mark_dropped_off(self):
        assignment = self.get_selected_assignment()
        if assignment:
            student_id, route_id = assignment[0], assignment[1]
            if update_dropoff_status(student_id, route_id, "Dropped Off"):
                self.load_assignments()
            else:
                messagebox.showerror("Error", "Failed to update drop-off status.")

if __name__ == '__main__':
    root = tk.Tk()
    app = PickupDropoffView(master=root)
    app.mainloop()
