import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import os

# Add the parent directory to the path to import the controller
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.student_bus_controller import get_all_assignments, update_pickup_status, update_dropoff_status

class PickupDropoffView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Pickup and Drop-off")
        self.pack(fill="both", expand=True, padx=10, pady=10)
        self.create_widgets()
        self.load_assignments()

    def create_widgets(self):
        # Table to display assignments
        table_frame = tk.LabelFrame(self, text="Student Status", padx=10, pady=10)
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

        self.pickup_button = tk.Button(button_frame, text="Mark as Picked Up", command=self.mark_picked_up)
        self.pickup_button.pack(side="left", padx=5)

        self.dropoff_button = tk.Button(button_frame, text="Mark as Dropped Off", command=self.mark_dropped_off)
        self.dropoff_button.pack(side="left", padx=5)

    def load_assignments(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.assignments = get_all_assignments()
        for assignment in self.assignments:
            # We only need to display student name, route name, pickup status, dropoff status
            display_data = (assignment[2], assignment[3], assignment[6], assignment[7])
            self.tree.insert("", "end", values=display_data)

    def get_selected_assignment(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student from the list.")
            return None

        # Find the full assignment data corresponding to the selected treeview item
        selected_values = self.tree.item(selected_item)['values']
        for assignment in self.assignments:
            if assignment[2] == selected_values[0] and assignment[3] == selected_values[1]:
                return assignment
        return None

    def mark_picked_up(self):
        assignment = self.get_selected_assignment()
        if assignment:
            student_id = assignment[0]
            route_id = assignment[1]
            if update_pickup_status(student_id, route_id, "Picked Up"):
                self.load_assignments()
            else:
                messagebox.showerror("Error", "Failed to update pickup status.")

    def mark_dropped_off(self):
        assignment = self.get_selected_assignment()
        if assignment:
            student_id = assignment[0]
            route_id = assignment[1]
            if update_dropoff_status(student_id, route_id, "Dropped Off"):
                self.load_assignments()
            else:
                messagebox.showerror("Error", "Failed to update drop-off status.")


if __name__ == '__main__':
    root = tk.Tk()
    app = PickupDropoffView(master=root)
    app.mainloop()
