import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import os

# Add the parent directory to the path to import the controller
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.academic_calendar_controller import add_academic_year, get_all_academic_years, add_term, get_terms_by_year

class AcademicCalendarView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Academic Calendar Management")
        self.pack(padx=20, pady=20)
        self.create_widgets()
        self.load_years()

    def create_widgets(self):
        # Frame for adding academic year
        year_frame = tk.LabelFrame(self, text="Add Academic Year", padx=10, pady=10)
        year_frame.pack(fill="x", expand="yes", padx=10, pady=5)

        self.year_label = tk.Label(year_frame, text="Year (e.g., 2024/2025):")
        self.year_label.pack(side="left")
        self.year_entry = tk.Entry(year_frame, width=20)
        self.year_entry.pack(side="left", padx=5)
        self.add_year_button = tk.Button(year_frame, text="Add Year", command=self.add_year)
        self.add_year_button.pack(side="left", padx=5)

        # Frame for managing terms
        term_frame = tk.LabelFrame(self, text="Manage Terms", padx=10, pady=10)
        term_frame.pack(fill="x", expand="yes", padx=10, pady=5)

        self.year_select_label = tk.Label(term_frame, text="Select Year:")
        self.year_select_label.grid(row=0, column=0, sticky=tk.W)
        self.year_var = tk.StringVar()
        self.year_dropdown = ttk.Combobox(term_frame, textvariable=self.year_var, state="readonly")
        self.year_dropdown.grid(row=0, column=1, pady=5)
        self.year_dropdown.bind("<<ComboboxSelected>>", self.load_terms_for_selected_year)

        self.term_name_label = tk.Label(term_frame, text="Term Name:")
        self.term_name_label.grid(row=1, column=0, sticky=tk.W)
        self.term_name_entry = tk.Entry(term_frame)
        self.term_name_entry.grid(row=1, column=1, pady=2)

        self.start_date_label = tk.Label(term_frame, text="Start Date (YYYY-MM-DD):")
        self.start_date_label.grid(row=2, column=0, sticky=tk.W)
        self.start_date_entry = tk.Entry(term_frame)
        self.start_date_entry.grid(row=2, column=1, pady=2)

        self.end_date_label = tk.Label(term_frame, text="End Date (YYYY-MM-DD):")
        self.end_date_label.grid(row=3, column=0, sticky=tk.W)
        self.end_date_entry = tk.Entry(term_frame)
        self.end_date_entry.grid(row=3, column=1, pady=2)

        self.add_term_button = tk.Button(term_frame, text="Add Term", command=self.add_new_term)
        self.add_term_button.grid(row=4, column=1, sticky=tk.E, pady=10)

        # Table to display terms
        self.term_tree = ttk.Treeview(term_frame, columns=("ID", "Name", "Start Date", "End Date"), show="headings")
        self.term_tree.heading("ID", text="ID")
        self.term_tree.heading("Name", text="Term Name")
        self.term_tree.heading("Start Date", text="Start Date")
        self.term_tree.heading("End Date", text="End Date")
        self.term_tree.grid(row=5, column=0, columnspan=2, sticky="nsew")

    def load_years(self):
        self.years = get_all_academic_years()
        self.year_dropdown['values'] = [year[1] for year in self.years]
        if self.years:
            self.year_var.set(self.years[0][1])
            self.load_terms_for_selected_year()

    def add_year(self):
        year = self.year_entry.get()
        if not year:
            messagebox.showerror("Error", "Year field cannot be empty.")
            return
        result = add_academic_year(year)
        if result is True:
            messagebox.showinfo("Success", "Academic year added successfully!")
            self.year_entry.delete(0, tk.END)
            self.load_years()
        elif result == "Year already exists":
            messagebox.showerror("Error", "This academic year already exists.")
        else:
            messagebox.showerror("Error", "Failed to add academic year.")

    def load_terms_for_selected_year(self, event=None):
        selected_year_str = self.year_var.get()
        year_id = None
        for year in self.years:
            if year[1] == selected_year_str:
                year_id = year[0]
                break

        for row in self.term_tree.get_children():
            self.term_tree.delete(row)

        if year_id:
            terms = get_terms_by_year(year_id)
            for term in terms:
                self.term_tree.insert("", "end", values=term)

    def add_new_term(self):
        year_str = self.year_var.get()
        name = self.term_name_entry.get()
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()

        if not all([year_str, name, start_date, end_date]):
            messagebox.showerror("Error", "All term fields are required.")
            return

        year_id = None
        for year in self.years:
            if year[1] == year_str:
                year_id = year[0]
                break

        if add_term(name, year_id, start_date, end_date):
            messagebox.showinfo("Success", "Term added successfully!")
            self.term_name_entry.delete(0, tk.END)
            self.start_date_entry.delete(0, tk.END)
            self.end_date_entry.delete(0, tk.END)
            self.load_terms_for_selected_year()
        else:
            messagebox.showerror("Error", "Failed to add term.")

if __name__ == '__main__':
    root = tk.Tk()
    app = AcademicCalendarView(master=root)
    app.mainloop()
