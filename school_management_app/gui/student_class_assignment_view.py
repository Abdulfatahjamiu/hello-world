import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import os
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from core.student_class_assignment_controller import assign_student_to_class, get_class_assignments
from core.student_controller import get_student_names
from core.academic_calendar_controller import get_all_terms
from core.class_management_controller import get_all_sections

class StudentClassAssignmentView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Assign Student to Class Section")
        self.pack(padx=20, pady=20)
        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        form_frame = tk.LabelFrame(self, text="Assign Student", padx=10, pady=10)
        form_frame.pack(fill="x", expand="yes", padx=10, pady=5)

        tk.Label(form_frame, text="Student:").grid(row=0, column=0, sticky=tk.W)
        self.student_var = tk.StringVar()
        self.student_dropdown = ttk.Combobox(form_frame, textvariable=self.student_var, state="readonly")
        self.student_dropdown.grid(row=0, column=1, pady=5)

        tk.Label(form_frame, text="Term:").grid(row=1, column=0, sticky=tk.W)
        self.term_var = tk.StringVar()
        self.term_dropdown = ttk.Combobox(form_frame, textvariable=self.term_var, state="readonly")
        self.term_dropdown.grid(row=1, column=1, pady=5)

        tk.Label(form_frame, text="Class Section:").grid(row=2, column=0, sticky=tk.W)
        self.section_var = tk.StringVar()
        self.section_dropdown = ttk.Combobox(form_frame, textvariable=self.section_var, state="readonly")
        self.section_dropdown.grid(row=2, column=1, pady=5)

        self.assign_button = tk.Button(form_frame, text="Assign", command=self.assign)
        self.assign_button.grid(row=3, column=1, sticky=tk.E, pady=10)

        table_frame = tk.LabelFrame(self, text="Current Assignments", padx=10, pady=10)
        table_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.columns = ("Student", "Class", "Section", "Term", "Year")
        self.tree = ttk.Treeview(table_frame, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col)
        self.tree.pack(fill="both", expand=True)

    def load_data(self):
        self.students = get_student_names()
        self.student_dropdown['values'] = [f"{name} (ID: {sid})" for sid, name in self.students]
        self.terms = get_all_terms()
        self.term_dropdown['values'] = [f"{name} {year} (ID: {tid})" for tid, name, year in self.terms]
        self.sections = get_all_sections()
        self.section_dropdown['values'] = [f"{class_name} - {sec_name} (ID: {sid})" for sid, sec_name, class_name in self.sections]
        self.load_assignments()

    def load_assignments(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        assignments = get_class_assignments()
        for assignment in assignments:
            self.tree.insert("", "end", values=assignment)

    def assign(self):
        student_info = self.student_var.get()
        term_info = self.term_var.get()
        section_info = self.section_var.get()

        if not all([student_info, term_info, section_info]):
            messagebox.showerror("Error", "All fields are required.")
            return

        student_id = int(re.search(r'\(ID: (\d+)\)', student_info).group(1))
        term_id = int(re.search(r'\(ID: (\d+)\)', term_info).group(1))
        section_id = int(re.search(r'\(ID: (\d+)\)', section_info).group(1))

        result = assign_student_to_class(student_id, section_id, term_id)
        if result is True:
            messagebox.showinfo("Success", "Student assigned to class successfully!")
            self.load_assignments()
        else:
            messagebox.showerror("Error", result)

if __name__ == '__main__':
    root = tk.Tk()
    app = StudentClassAssignmentView(master=root)
    app.mainloop()
