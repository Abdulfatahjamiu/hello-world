import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import os
import csv

# Add the parent directory to the path to import the controller
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
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
            if col == "Address" or col == "Medical Info":
                self.tree.column(col, width=200)
            else:
                self.tree.column(col, width=100)
        self.tree.column("ID", width=30)

        self.tree.pack(fill="both", expand=True)

        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        self.refresh_button = tk.Button(button_frame, text="Refresh", command=self.load_students)
        self.refresh_button.pack(side="left", padx=5)

        self.generate_letter_button = tk.Button(button_frame, text="Generate Admission Letter", command=self.generate_letter)
        self.generate_letter_button.pack(side="left", padx=5)

        self.export_button = tk.Button(button_frame, text="Export to CSV", command=self.export_to_csv)
        self.export_button.pack(side="left", padx=5)

        self.view_profile_button = tk.Button(button_frame, text="View Profile", command=self.open_profile)
        self.view_profile_button.pack(side="left", padx=5)

    def open_profile(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student from the list.")
            return

        item = self.tree.item(selected_item)
        student_id = item['values'][0] # The first value is the ID

        new_window = tk.Toplevel(self.master)
        StudentProfileView(new_window, student_id=student_id)

    def load_students(self):
        # Clear existing data
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Load new data
        self.students = get_all_students()
        for student in self.students:
            self.tree.insert("", "end", values=student)

    def generate_letter(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a student from the list.")
            return

        item = self.tree.item(selected_item)
        student_data = item['values']

        student_name = student_data[1]
        class_name = student_data[4]
        gender = student_data[5]
        parent_name = student_data[7]
        reg_date = student_data[8].split(" ")[0] # Get only the date part

        file_name = generate_admission_letter(student_name, class_name, reg_date, parent_name, gender)

        if file_name:
            messagebox.showinfo("Success", f"Admission letter generated successfully: {file_name}")
        else:
            messagebox.showerror("Error", "Failed to generate admission letter.")

    def export_to_csv(self):
        if not self.students:
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
