import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import os
import csv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from core.student_controller import get_all_students
from core.admission_letter import generate_admission_letter
from .student_profile_view import StudentProfileView

class StudentListView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Registered Students")
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.load_students()

    def create_widgets(self):
        self.columns = ("ID", "Name", "DOB", "Address", "Class", "Gender", "Medical Info", "Parent", "Reg. Date")
        self.tree = ttk.Treeview(self, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
            width = 200 if col in ["Address", "Medical Info"] else 100
            self.tree.column(col, width=width)
        self.tree.column("ID", width=40)
        self.tree.pack(fill="both", expand=True)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)
        self.refresh_button = tk.Button(button_frame, text="Refresh", command=self.load_students)
        self.refresh_button.pack(side="left", padx=5)
        self.view_profile_button = tk.Button(button_frame, text="View Profile", command=self.open_profile)
        self.view_profile_button.pack(side="left", padx=5)
        self.export_button = tk.Button(button_frame, text="Export to CSV", command=self.export_to_csv)
        self.export_button.pack(side="left", padx=5)

    def load_students(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.students = get_all_students()
        for student in self.students:
            # Combine address fields for display
            address = f"{student[3]}, {student[4]}, {student[5]} {student[6]}"
            display_student = student[:3] + (address,) + student[7:]
            self.tree.insert("", "end", values=display_student)

    def open_profile(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student.")
            return
        student_id = self.tree.item(selected_item)['values'][0]
        new_window = tk.Toplevel(self.master)
        StudentProfileView(new_window, student_id=student_id)

    def export_to_csv(self):
        if not hasattr(self, 'students') or not self.students:
            messagebox.showerror("Error", "No data to export.")
            return
        try:
            with open("students_report.csv", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(self.columns)
                writer.writerows(self.students)
            messagebox.showinfo("Success", "Report exported to students_report.csv")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export report: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = StudentListView(master=root)
    app.mainloop()
