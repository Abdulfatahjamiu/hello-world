import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import os
import csv

# Add the parent directory to the path to import the controller
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.preregistration_controller import get_all_parents

class ParentListView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Preregistered Parents")
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.load_parents()

    def create_widgets(self):
        self.columns = ("ID", "Name", "Phone", "Email", "Child Name", "Child Age", "Enquiry Date", "Notes", "Follow-up Date", "Next of Kin", "Next of Kin Phone")
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)

        self.tree.pack(fill="both", expand=True)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        self.refresh_button = tk.Button(button_frame, text="Refresh", command=self.load_parents)
        self.refresh_button.pack(side="left", padx=5)

        self.export_button = tk.Button(button_frame, text="Export to CSV", command=self.export_to_csv)
        self.export_button.pack(side="left", padx=5)

    def load_parents(self):
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Load new data
        self.parents = get_all_parents()
        for parent in self.parents:
            self.tree.insert("", "end", values=parent)

    def export_to_csv(self):
        if not self.parents:
            messagebox.showerror("Error", "No data to export.")
            return

        try:
            with open("parents_report.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self.columns)
                writer.writerows(self.parents)
            messagebox.showinfo("Success", "Report exported to parents_report.csv")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {e}")


if __name__ == '__main__':
    root = tk.Tk()
    app = ParentListView(master=root)
    app.mainloop()
