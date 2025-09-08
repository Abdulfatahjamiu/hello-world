import tkinter as tk
from tkinter import messagebox
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from core.preregistration_controller import add_parent

class PreregistrationView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Parent Preregistration")
        self.pack(padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        # Using a frame for better layout management
        form_frame = tk.Frame(self)
        form_frame.pack()

        # Grid layout for labels and entries
        labels = ["Name:", "Phone Number:", "Email:", "Child's Name:", "Child's Age:", "Notes:", "Follow-up Date (YYYY-MM-DD):", "Next of Kin Name:", "Next of Kin Phone:"]
        self.entries = {}

        for i, label_text in enumerate(labels):
            label = tk.Label(form_frame, text=label_text)
            label.grid(row=i, column=0, sticky=tk.W, pady=5, padx=5)
            entry = tk.Entry(form_frame, width=40)
            entry.grid(row=i, column=1, pady=5, padx=5)
            self.entries[label_text] = entry

        # Submit Button
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_form)
        self.submit_button.pack(pady=10)

    def submit_form(self):
        data = {key.replace(":", "").replace(" (YYYY-MM-DD)", "").replace("'s", "").replace(" ", "_").lower(): entry.get() for key, entry in self.entries.items()}

        if not data['name'] or not data['phone_number']:
            messagebox.showerror("Error", "Name and Phone Number are required.")
            return

        if add_parent(
            data['name'], data['phone_number'], data['email'],
            data['child_name'], data['child_age'], data['notes'],
            data['follow-up_date'], data['next_of_kin_name'], data['next_of_kin_phone']
        ):
            messagebox.showinfo("Success", "Parent preregistered successfully!")
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to preregister parent.")

    def clear_form(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

if __name__ == '__main__':
    root = tk.Tk()
    app = PreregistrationView(master=root)
    app.mainloop()
