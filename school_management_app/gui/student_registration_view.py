import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import os
import re

# Add the parent directory to the path to import the controller
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from modules.preregistration_controller import get_parent_names
from modules.student_controller import add_student

class StudentRegistrationView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Student Registration")
        self.pack(padx=20, pady=20)
        self.create_widgets()
        self.load_parents()

    def create_widgets(self):
        # Name
        self.name_label = tk.Label(self, text="Name:")
        self.name_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = tk.Entry(self, width=30)
        self.name_entry.grid(row=0, column=1)

        # Date of Birth
        self.dob_label = tk.Label(self, text="Date of Birth (YYYY-MM-DD):")
        self.dob_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.dob_entry = tk.Entry(self, width=30)
        self.dob_entry.grid(row=1, column=1)

        # Address
        self.address1_label = tk.Label(self, text="Address Line 1:")
        self.address1_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.address1_entry = tk.Entry(self, width=30)
        self.address1_entry.grid(row=2, column=1)

        self.city_label = tk.Label(self, text="City:")
        self.city_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        self.city_entry = tk.Entry(self, width=30)
        self.city_entry.grid(row=3, column=1)

        self.state_label = tk.Label(self, text="State:")
        self.state_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        self.state_entry = tk.Entry(self, width=30)
        self.state_entry.grid(row=4, column=1)

        self.zip_label = tk.Label(self, text="Zip Code:")
        self.zip_label.grid(row=5, column=0, sticky=tk.W, pady=5)
        self.zip_entry = tk.Entry(self, width=30)
        self.zip_entry.grid(row=5, column=1)

        # Class
        self.class_label = tk.Label(self, text="Class:")
        self.class_label.grid(row=6, column=0, sticky=tk.W, pady=5)
        self.class_entry = tk.Entry(self, width=30)
        self.class_entry.grid(row=6, column=1)

        # Gender
        self.gender_label = tk.Label(self, text="Gender:")
        self.gender_label.grid(row=7, column=0, sticky=tk.W, pady=5)
        self.gender_var = tk.StringVar()
        self.gender_dropdown = ttk.Combobox(self, textvariable=self.gender_var, values=["Male", "Female", "Other"], width=28, state="readonly")
        self.gender_dropdown.grid(row=7, column=1)

        # Medical Information
        self.medical_info_label = tk.Label(self, text="Medical Information:")
        self.medical_info_label.grid(row=8, column=0, sticky=tk.W, pady=5)
        self.medical_info_entry = tk.Entry(self, width=30)
        self.medical_info_entry.grid(row=8, column=1)

        # Photo
        self.photo_label = tk.Label(self, text="Student Photo:")
        self.photo_label.grid(row=9, column=0, sticky=tk.W, pady=5)
        self.photo_path_var = tk.StringVar()
        self.photo_path_label = tk.Label(self, textvariable=self.photo_path_var, wraplength=200)
        self.photo_path_label.grid(row=9, column=1, sticky=tk.W)
        self.upload_button = tk.Button(self, text="Upload Photo", command=self.upload_photo)
        self.upload_button.grid(row=9, column=2)


        # Parent
        self.parent_label = tk.Label(self, text="Parent:")
        self.parent_label.grid(row=10, column=0, sticky=tk.W, pady=5)
        self.parent_var = tk.StringVar()
        self.parent_dropdown = ttk.Combobox(self, textvariable=self.parent_var, width=28, state="readonly")
        self.parent_dropdown.grid(row=10, column=1)

        # Submit Button
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_form)
        self.submit_button.grid(row=11, column=0, columnspan=2, pady=10)

    def load_parents(self):
        self.parents = get_parent_names()
        self.parent_dropdown['values'] = [f"{name} (ID: {pid})" for pid, name in self.parents]

    def upload_photo(self):
        from tkinter import filedialog
        filepath = filedialog.askopenfilename(
            title="Select Student Photo",
            filetypes=(("Image files", "*.jpg *.jpeg *.png *.gif"), ("All files", "*.*"))
        )
        if filepath:
            self.photo_path_var.set(filepath)

    def submit_form(self):
        name = self.name_entry.get()
        dob = self.dob_entry.get()
        address1 = self.address1_entry.get()
        city = self.city_entry.get()
        state = self.state_entry.get()
        zip_code = self.zip_entry.get()
        class_name = self.class_entry.get()
        gender = self.gender_var.get()
        medical_info = self.medical_info_entry.get()
        photo_path = self.photo_path_var.get()
        parent_info = self.parent_var.get()

        if not all([name, dob, address1, city, state, zip_code, class_name, gender, parent_info]):
            messagebox.showerror("Error", "All fields except Medical Info and Photo are required.")
            return

        # Extract parent ID from the selected string
        match = re.search(r'\(ID: (\d+)\)', parent_info)
        if not match:
            messagebox.showerror("Error", "Invalid parent selected.")
            return
        parent_id = int(match.group(1))

        if add_student(name, dob, address1, city, state, zip_code, class_name, gender, medical_info, photo_path, parent_id):
            messagebox.showinfo("Success", "Student registered successfully!")
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to register student.")

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.dob_entry.delete(0, tk.END)
        self.address1_entry.delete(0, tk.END)
        self.city_entry.delete(0, tk.END)
        self.state_entry.delete(0, tk.END)
        self.zip_entry.delete(0, tk.END)
        self.class_entry.delete(0, tk.END)
        self.gender_var.set('')
        self.medical_info_entry.delete(0, tk.END)
        self.photo_path_var.set('')
        self.parent_var.set('')


if __name__ == '__main__':
    root = tk.Tk()
    app = StudentRegistrationView(master=root)
    app.mainloop()
