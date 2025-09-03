import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import sys
import os

# Add the parent directory to the path to import the controller
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.student_controller import get_student_by_id
from core.id_card_generator import generate_id_card

class StudentProfileView(tk.Frame):
    def __init__(self, master=None, student_id=None):
        super().__init__(master)
        self.master = master
        self.master.title("Student Profile")
        self.pack(padx=20, pady=20)
        self.student_id = student_id
        self.create_widgets()
        self.load_student_data()

    def create_widgets(self):
        self.photo_label = tk.Label(self)
        self.photo_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.details_frame = tk.Frame(self)
        self.details_frame.grid(row=1, column=0, columnspan=2)

        self.labels = {}
        self.values = {}

        self.generate_card_button = tk.Button(self, text="Generate ID Card", command=self.generate_card)
        self.generate_card_button.grid(row=2, column=0, columnspan=2, pady=10)

    def generate_card(self):
        if not self.student_data:
            messagebox.showerror("Error", "Student data not loaded.")
            return

        (sid, name, dob, addr1, city, state, zip_code, s_class, gender, med_info, photo_path, parent_id, reg_date) = self.student_data

        file_name = generate_id_card(name, sid, s_class, photo_path)
        if file_name:
            messagebox.showinfo("Success", f"ID Card generated successfully: {file_name}")
        else:
            messagebox.showerror("Error", "Failed to generate ID Card.")

    def load_student_data(self):
        self.student_data = get_student_by_id(self.student_id)
        if not self.student_data:
            return

        # Unpack student data (assuming a specific order)
        (sid, name, dob, addr1, city, state, zip_code, s_class, gender, med_info, photo_path, parent_id, reg_date) = self.student_data

        # Display Photo
        if photo_path and os.path.exists(os.path.join('..', photo_path)):
            try:
                img = Image.open(os.path.join('..', photo_path))
                img.thumbnail((150, 150))
                self.photo_image = ImageTk.PhotoImage(img)
                self.photo_label.config(image=self.photo_image)
            except Exception as e:
                print(f"Error loading image: {e}")
                self.photo_label.config(text="Image not found")
        else:
            self.photo_label.config(text="No Photo")

        # Display Details
        details = {
            "Name": name,
            "Date of Birth": dob,
            "Address": f"{addr1}, {city}, {state} {zip_code}",
            "Class": s_class,
            "Gender": gender,
            "Medical Info": med_info,
            "Registration Date": reg_date,
        }

        row = 0
        for label, value in details.items():
            if label in self.labels:
                self.values[label].config(text=value)
            else:
                self.labels[label] = tk.Label(self.details_frame, text=f"{label}:", font=("Arial", 10, "bold"))
                self.labels[label].grid(row=row, column=0, sticky=tk.W, pady=2)
                self.values[label] = tk.Label(self.details_frame, text=value, wraplength=300)
                self.values[label].grid(row=row, column=1, sticky=tk.W, pady=2)
            row += 1

if __name__ == '__main__':
    # This is for testing purposes. You would pass a real student_id.
    test_student_id = 1
    root = tk.Tk()
    app = StudentProfileView(master=root, student_id=test_student_id)
    app.mainloop()
