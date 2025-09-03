import tkinter as tk
from tkinter import messagebox
import sys
import os

# Add the parent directory to the path to import the controller
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.preregistration_controller import add_parent

class PreregistrationView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Parent Preregistration")
        self.pack(padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        # Name
        self.name_label = tk.Label(self, text="Name:")
        self.name_label.grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_entry = tk.Entry(self, width=30)
        self.name_entry.grid(row=0, column=1)

        # Phone Number
        self.phone_label = tk.Label(self, text="Phone Number:")
        self.phone_label.grid(row=1, column=0, sticky=tk.W, pady=5)
        self.phone_entry = tk.Entry(self, width=30)
        self.phone_entry.grid(row=1, column=1)

        # Email
        self.email_label = tk.Label(self, text="Email:")
        self.email_label.grid(row=2, column=0, sticky=tk.W, pady=5)
        self.email_entry = tk.Entry(self, width=30)
        self.email_entry.grid(row=2, column=1)

        # Child's Name
        self.child_name_label = tk.Label(self, text="Child's Name:")
        self.child_name_label.grid(row=3, column=0, sticky=tk.W, pady=5)
        self.child_name_entry = tk.Entry(self, width=30)
        self.child_name_entry.grid(row=3, column=1)

        # Child's Age
        self.child_age_label = tk.Label(self, text="Child's Age:")
        self.child_age_label.grid(row=4, column=0, sticky=tk.W, pady=5)
        self.child_age_entry = tk.Entry(self, width=30)
        self.child_age_entry.grid(row=4, column=1)

        # Notes
        self.notes_label = tk.Label(self, text="Notes:")
        self.notes_label.grid(row=5, column=0, sticky=tk.W, pady=5)
        self.notes_entry = tk.Entry(self, width=30)
        self.notes_entry.grid(row=5, column=1)

        # Follow-up Date
        self.follow_up_date_label = tk.Label(self, text="Follow-up Date (YYYY-MM-DD):")
        self.follow_up_date_label.grid(row=6, column=0, sticky=tk.W, pady=5)
        self.follow_up_date_entry = tk.Entry(self, width=30)
        self.follow_up_date_entry.grid(row=6, column=1)

        # Next of Kin Name
        self.next_of_kin_name_label = tk.Label(self, text="Next of Kin Name:")
        self.next_of_kin_name_label.grid(row=7, column=0, sticky=tk.W, pady=5)
        self.next_of_kin_name_entry = tk.Entry(self, width=30)
        self.next_of_kin_name_entry.grid(row=7, column=1)

        # Next of Kin Phone
        self.next_of_kin_phone_label = tk.Label(self, text="Next of Kin Phone:")
        self.next_of_kin_phone_label.grid(row=8, column=0, sticky=tk.W, pady=5)
        self.next_of_kin_phone_entry = tk.Entry(self, width=30)
        self.next_of_kin_phone_entry.grid(row=8, column=1)

        # Submit Button
        self.submit_button = tk.Button(self, text="Submit", command=self.submit_form)
        self.submit_button.grid(row=9, column=0, columnspan=2, pady=10)

    def submit_form(self):
        name = self.name_entry.get()
        phone_number = self.phone_entry.get()
        email = self.email_entry.get()
        child_name = self.child_name_entry.get()
        child_age = self.child_age_entry.get()
        notes = self.notes_entry.get()
        follow_up_date = self.follow_up_date_entry.get()
        next_of_kin_name = self.next_of_kin_name_entry.get()
        next_of_kin_phone = self.next_of_kin_phone_entry.get()

        if not name or not phone_number:
            messagebox.showerror("Error", "Name and Phone Number are required.")
            return

        if add_parent(name, phone_number, email, child_name, child_age, notes, follow_up_date, next_of_kin_name, next_of_kin_phone):
            messagebox.showinfo("Success", "Parent preregistered successfully!")
            self.clear_form()
        else:
            messagebox.showerror("Error", "Failed to preregister parent.")

    def clear_form(self):
        self.name_entry.delete(0, tk.END)
        self.phone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.child_name_entry.delete(0, tk.END)
        self.child_age_entry.delete(0, tk.END)
        self.notes_entry.delete(0, tk.END)
        self.follow_up_date_entry.delete(0, tk.END)
        self.next_of_kin_name_entry.delete(0, tk.END)
        self.next_of_kin_phone_entry.delete(0, tk.END)

if __name__ == '__main__':
    root = tk.Tk()
    app = PreregistrationView(master=root)
    app.mainloop()
