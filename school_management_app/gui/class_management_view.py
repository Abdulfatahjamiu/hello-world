import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sys
import os

# Add the parent directory to the path to import the controller
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.class_management_controller import add_class, get_all_classes, add_section, get_sections_by_class

class ClassManagementView(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.title("Class and Section Management")
        self.pack(padx=20, pady=20)
        self.create_widgets()
        self.load_classes()

    def create_widgets(self):
        # Frame for adding a new class
        class_frame = tk.LabelFrame(self, text="Add New Class", padx=10, pady=10)
        class_frame.pack(fill="x", expand="yes", padx=10, pady=5)

        self.class_label = tk.Label(class_frame, text="Class Name (e.g., Grade 1):")
        self.class_label.pack(side="left")
        self.class_entry = tk.Entry(class_frame, width=20)
        self.class_entry.pack(side="left", padx=5)
        self.add_class_button = tk.Button(class_frame, text="Add Class", command=self.add_new_class)
        self.add_class_button.pack(side="left", padx=5)

        # Frame for managing sections
        section_frame = tk.LabelFrame(self, text="Manage Sections", padx=10, pady=10)
        section_frame.pack(fill="x", expand="yes", padx=10, pady=5)

        self.class_select_label = tk.Label(section_frame, text="Select Class:")
        self.class_select_label.grid(row=0, column=0, sticky=tk.W)
        self.class_var = tk.StringVar()
        self.class_dropdown = ttk.Combobox(section_frame, textvariable=self.class_var, state="readonly")
        self.class_dropdown.grid(row=0, column=1, pady=5)
        self.class_dropdown.bind("<<ComboboxSelected>>", self.load_sections_for_selected_class)

        self.section_name_label = tk.Label(section_frame, text="Section Name (e.g., A):")
        self.section_name_label.grid(row=1, column=0, sticky=tk.W)
        self.section_name_entry = tk.Entry(section_frame)
        self.section_name_entry.grid(row=1, column=1, pady=2)

        self.add_section_button = tk.Button(section_frame, text="Add Section", command=self.add_new_section)
        self.add_section_button.grid(row=2, column=1, sticky=tk.E, pady=10)

        # Table to display sections
        self.section_tree = ttk.Treeview(section_frame, columns=("ID", "Name"), show="headings")
        self.section_tree.heading("ID", text="ID")
        self.section_tree.heading("Name", text="Section Name")
        self.section_tree.grid(row=3, column=0, columnspan=2, sticky="nsew")

    def load_classes(self):
        self.classes = get_all_classes()
        self.class_dropdown['values'] = [c[1] for c in self.classes]
        if self.classes:
            self.class_var.set(self.classes[0][1])
            self.load_sections_for_selected_class()

    def add_new_class(self):
        name = self.class_entry.get()
        if not name:
            messagebox.showerror("Error", "Class name cannot be empty.")
            return
        result = add_class(name)
        if result is True:
            messagebox.showinfo("Success", "Class added successfully!")
            self.class_entry.delete(0, tk.END)
            self.load_classes()
        elif result == "Class already exists":
            messagebox.showerror("Error", "This class already exists.")
        else:
            messagebox.showerror("Error", "Failed to add class.")

    def load_sections_for_selected_class(self, event=None):
        selected_class_str = self.class_var.get()
        class_id = None
        for c in self.classes:
            if c[1] == selected_class_str:
                class_id = c[0]
                break

        for row in self.section_tree.get_children():
            self.section_tree.delete(row)

        if class_id:
            sections = get_sections_by_class(class_id)
            for section in sections:
                self.section_tree.insert("", "end", values=section)

    def add_new_section(self):
        class_str = self.class_var.get()
        name = self.section_name_entry.get()

        if not all([class_str, name]):
            messagebox.showerror("Error", "Both class and section name are required.")
            return

        class_id = None
        for c in self.classes:
            if c[1] == class_str:
                class_id = c[0]
                break

        if add_section(name, class_id):
            messagebox.showinfo("Success", "Section added successfully!")
            self.section_name_entry.delete(0, tk.END)
            self.load_sections_for_selected_class()
        else:
            messagebox.showerror("Error", "Failed to add section.")

if __name__ == '__main__':
    root = tk.Tk()
    app = ClassManagementView(master=root)
    app.mainloop()
