import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog
import sys
import os
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from core.preregistration_controller import get_parent_names
from core.student_controller import add_student

class StudentRegistrationView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Student Registration")
        self.pack(padx=20, pady=20)
        self.create_widgets()
        self.load_parents()

    def create_widgets(self):
        form_frame = tk.Frame(self)
        form_frame.pack()

        self.entries = {}
        labels = {
            "name": "Name:", "dob": "Date of Birth (YYYY-MM-DD):", "address1": "Address Line 1:",
            "city": "City:", "state": "State:", "zip_code": "Zip Code:", "class": "Class:",
            "medical_info": "Medical Information:"
        }

        row = 0
        for key, text in labels.items():
            label = tk.Label(form_frame, text=text)
            label.grid(row=row, column=0, sticky=tk.W, pady=5, padx=5)
            entry = tk.Entry(form_frame, width=40)
            entry.grid(row=row, column=1, pady=5, padx=5)
            self.entries[key] = entry
            row += 1

        # Gender Dropdown
        label = tk.Label(form_frame, text="Gender:")
        label.grid(row=row, column=0, sticky=tk.W, pady=5, padx=5)
        self.gender_var = tk.StringVar()
        self.gender_dropdown = ttk.Combobox(form_frame, textvariable=self.gender_var, values=["Male", "Female", "Other"], state="readonly")
        self.gender_dropdown.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        # Parent Dropdown
        label = tk.Label(form_frame, text="Parent:")
        label.grid(row=row, column=0, sticky=tk.W, pady=5, padx=5)
        self.parent_var = tk.StringVar()
        self.parent_dropdown = ttk.Combobox(form_frame, textvariable=self.parent_var, state="readonly")
        self.parent_dropdown.grid(row=row, column=1, pady=5, padx=5)
        row += 1

        # Photo Upload
        label = tk.Label(form_frame, text="Student Photo:")
        label.grid(row=row, column=0, sticky=tk.W, pady=5, padx=5)
        self.photo_path_var = tk.StringVar()
        self.photo_path_label = tk.Label(form_frame, textvariable=self.photo_path_var, wraplength=250)
        self.photo_path_label.grid(row=row, column=1, sticky=tk.W)
        self.upload_button = tk.Button(form_frame, text="Upload", command=self.upload_photo)
        self.upload_button.grid(row=row, column=2)
        row += 1

        self.submit_button = tk.Button(self, text="Submit", command=self.submit_form)
        self.submit_button.pack(pady=10)

    def load_parents(self):
        parents = get_parent_names()
        self.parent_map = {f"{name} (ID: {pid})": pid for pid, name in parents}
        self.parent_dropdown['values'] = list(self.parent_map.keys())

    def upload_photo(self):
        filepath = filedialog.askopenfilename(title="Select Student Photo", filetypes=(("Image files", "*.jpg *.jpeg *.png"), ("All files", "*.*")))
        if filepath:
            self.photo_path_var.set(filepath)

    def submit_form(self):
        data = {key: entry.get() for key, entry in self.entries.items()}
        data['gender'] = self.gender_var.get()
        data['photo_path'] = self.photo_path_var.get()
        parent_info = self.parent_var.get()

        if not all([data['name'], data['dob'], data['address1'], data['city'], data['state'], data['zip_code'], data['class'], data['gender'], parent_info]):
            messagebox.showerror("Error", "All fields except Medical Info and Photo are required.")
            return

        parent_id = self.parent_map.get(parent_info)
        if not parent_id:
            messagebox.showerror("Error", "Invalid parent selected.")
            return

        if add_student(data['name'], data['dob'], data['address1'], data['city'], data['state'], data['zip_code'], data['class'], data['gender'], data['medical_info'], data['photo_path'], parent_id):
            messagebox.showinfo("Success", "Student registered successfully!")
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to register student.")

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.gender_var.set('')
        self.parent_var.set('')
        self.photo_path_var.set('')

if __name__ == '__main__':
    root = tk.Tk()
    app = StudentRegistrationView(master=root)
    app.mainloop()
