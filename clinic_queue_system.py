"""
==========================================================================
 PROJECT     : Community Clinic Queue Management System
 COURSE      : PROG103 - Principles of Structured Programming
 INSTITUTION : Limkokwing University of Creative Technology, Sierra Leone
 SDG ALIGNED : SDG 3 - Good Health and Well-Being
 DESCRIPTION : A GUI-based structured Python application that helps small
               community clinics in Sierra Leone manage patient queues in
               an organized, fair, and transparent way. Patients register
               with basic details and a priority level (Emergency, Elderly/
               Pregnant, Normal). The system automatically assigns a queue
               number, sorts patients by priority, and lets clinic staff
               call the next patient, view the full queue, and remove
               attended patients.
 AUTHOR      : [Your Name Here]
 LICENSE     : MIT License (see LICENSE file)
==========================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# --------------------------------------------------------------------
# GLOBAL CONSTANTS
# --------------------------------------------------------------------
PRIORITY_LEVELS = ["Emergency", "Elderly/Pregnant", "Normal"]

# Lower number = higher priority (used for sorting the queue)
PRIORITY_WEIGHT = {
    "Emergency": 1,
    "Elderly/Pregnant": 2,
    "Normal": 3
}

APP_BG = "#f4f6f8"
HEADER_BG = "#1B4F72"
HEADER_FG = "#FFFFFF"
BUTTON_BG = "#1B4F72"
BUTTON_FG = "#FFFFFF"


# --------------------------------------------------------------------
# DATA STRUCTURE
# --------------------------------------------------------------------
# Each patient is stored as a dictionary (a record) inside a list.
# This list acts as our in-memory "database" for the session.
patient_queue = []      # list of dicts -> the active queue
queue_counter = 0       # running counter -> used to generate queue numbers
served_count = 0        # tracks how many patients have been attended to


# --------------------------------------------------------------------
# FUNCTION 1: VALIDATION (processing module helper)
# --------------------------------------------------------------------
def validate_input(name, age_str):
    """
    Validates patient name and age input.
    Returns a tuple (is_valid: bool, message_or_age).
    Demonstrates: decision structures, string methods, type conversion.
    """
    name = name.strip()

    if name == "":
        return False, "Patient name cannot be empty."

    if not all(ch.isalpha() or ch.isspace() for ch in name):
        return False, "Patient name should contain letters only."

    if age_str.strip() == "":
        return False, "Age cannot be empty."

    if not age_str.strip().isdigit():
        return False, "Age must be a whole number."

    age = int(age_str.strip())

    if age <= 0 or age > 120:
        return False, "Please enter a realistic age (1-120)."

    return True, age


# --------------------------------------------------------------------
# FUNCTION 2: ADD PATIENT TO QUEUE (processing module)
# --------------------------------------------------------------------
def add_patient(name, age, priority, reason):
    """
    Adds a new patient record to the patient_queue list and assigns
    a unique queue number. Then re-sorts the queue by priority.
    Demonstrates: functions, dictionaries, list operations, loops (via sort).
    """
    global queue_counter
    queue_counter += 1

    record = {
        "queue_no": queue_counter,
        "name": name.strip().title(),
        "age": age,
        "priority": priority,
        "reason": reason.strip() if reason.strip() != "" else "Not specified",
        "time_registered": datetime.now().strftime("%H:%M:%S")
    }

    patient_queue.append(record)
    sort_queue()
    return record


# --------------------------------------------------------------------
# FUNCTION 3: SORT QUEUE (processing module)
# --------------------------------------------------------------------
def sort_queue():
    """
    Sorts the patient_queue list in place using priority weight first,
    then by queue number (first-come-first-served within same priority).
    Demonstrates: iteration/loops concept via sorting, decision logic
    encapsulated in the key function.
    """
    patient_queue.sort(key=lambda p: (PRIORITY_WEIGHT[p["priority"]], p["queue_no"]))


# --------------------------------------------------------------------
# FUNCTION 4: CALL NEXT PATIENT (processing module)
# --------------------------------------------------------------------
def call_next_patient():
    """
    Removes and returns the patient at the front of the sorted queue.
    Demonstrates: decision structures (if/else), list mutation.
    """
    global served_count

    if len(patient_queue) == 0:
        return None

    next_patient = patient_queue.pop(0)
    served_count += 1
    return next_patient


# --------------------------------------------------------------------
# FUNCTION 5: QUEUE SUMMARY / STATISTICS (output module helper)
# --------------------------------------------------------------------
def get_queue_summary():
    """
    Loops through the current queue and counts patients per priority
    level. Returns a formatted summary string.
    Demonstrates: loops, decision structures, string formatting.
    """
    counts = {"Emergency": 0, "Elderly/Pregnant": 0, "Normal": 0}

    for patient in patient_queue:
        counts[patient["priority"]] += 1

    summary = (
        f"Waiting: {len(patient_queue)}   |   "
        f"Emergency: {counts['Emergency']}   "
        f"Elderly/Pregnant: {counts['Elderly/Pregnant']}   "
        f"Normal: {counts['Normal']}   |   "
        f"Served Today: {served_count}"
    )
    return summary


# ======================================================================
# GUI APPLICATION CLASS
# ======================================================================
class ClinicQueueApp:
    """
    Main GUI class. Wraps all widgets and connects them to the
    backend logic functions defined above (separation of GUI and logic).
    """

    def __init__(self, root):
        self.root = root
        self.root.title("Community Clinic Queue Management System")
        self.root.geometry("900x600")
        self.root.configure(bg=APP_BG)
        self.root.resizable(False, False)

        self.build_header()
        self.build_input_section()
        self.build_button_section()
        self.build_output_section()
        self.refresh_queue_display()

    # ------------------------------------------------------------
    # HEADER
    # ------------------------------------------------------------
    def build_header(self):
        header = tk.Frame(self.root, bg=HEADER_BG, height=70)
        header.pack(fill="x")

        title = tk.Label(
            header,
            text="Community Clinic Queue Management System",
            bg=HEADER_BG, fg=HEADER_FG,
            font=("Tahoma", 16, "bold")
        )
        title.pack(pady=10)

        subtitle = tk.Label(
            header,
            text="SDG 3: Good Health and Well-Being  |  Sierra Leone",
            bg=HEADER_BG, fg=HEADER_FG,
            font=("Tahoma", 9)
        )
        subtitle.pack()

    # ------------------------------------------------------------
    # INPUT MODULE (GUI)
    # ------------------------------------------------------------
    def build_input_section(self):
        frame = tk.LabelFrame(
            self.root, text="Patient Registration",
            bg=APP_BG, font=("Tahoma", 10, "bold"), padx=10, pady=10
        )
        frame.place(x=20, y=85, width=420, height=300)

        # Name
        tk.Label(frame, text="Full Name:", bg=APP_BG, font=("Tahoma", 10)).grid(
            row=0, column=0, sticky="w", pady=8)
        self.name_entry = tk.Entry(frame, width=28, font=("Tahoma", 10))
        self.name_entry.grid(row=0, column=1, pady=8)

        # Age
        tk.Label(frame, text="Age:", bg=APP_BG, font=("Tahoma", 10)).grid(
            row=1, column=0, sticky="w", pady=8)
        self.age_entry = tk.Entry(frame, width=28, font=("Tahoma", 10))
        self.age_entry.grid(row=1, column=1, pady=8)

        # Priority
        tk.Label(frame, text="Priority Level:", bg=APP_BG, font=("Tahoma", 10)).grid(
            row=2, column=0, sticky="w", pady=8)
        self.priority_var = tk.StringVar(value=PRIORITY_LEVELS[2])
        priority_menu = ttk.Combobox(
            frame, textvariable=self.priority_var,
            values=PRIORITY_LEVELS, state="readonly", width=25
        )
        priority_menu.grid(row=2, column=1, pady=8)

        # Reason
        tk.Label(frame, text="Reason for Visit:", bg=APP_BG, font=("Tahoma", 10)).grid(
            row=3, column=0, sticky="nw", pady=8)
        self.reason_entry = tk.Text(frame, width=28, height=5, font=("Tahoma", 10))
        self.reason_entry.grid(row=3, column=1, pady=8)

    # ------------------------------------------------------------
    # BUTTON SECTION
    # ------------------------------------------------------------
    def build_button_section(self):
        frame = tk.Frame(self.root, bg=APP_BG)
        frame.place(x=20, y=395, width=420, height=180)

        btn_style = {"font": ("Tahoma", 10, "bold"), "bg": BUTTON_BG,
                     "fg": BUTTON_FG, "width": 18, "height": 1}

        tk.Button(frame, text="Add to Queue", command=self.handle_add_patient,
                  **btn_style).grid(row=0, column=0, padx=5, pady=8)

        tk.Button(frame, text="Call Next Patient", command=self.handle_call_next,
                  **btn_style).grid(row=0, column=1, padx=5, pady=8)

        tk.Button(frame, text="Clear Form", command=self.clear_form,
                  **btn_style).grid(row=1, column=0, padx=5, pady=8)

        tk.Button(frame, text="Exit", command=self.handle_exit,
                  **btn_style).grid(row=1, column=1, padx=5, pady=8)

        self.now_serving_label = tk.Label(
            frame, text="Now Serving: -", bg=APP_BG,
            font=("Tahoma", 12, "bold"), fg="#1B4F72"
        )
        self.now_serving_label.grid(row=2, column=0, columnspan=2, pady=15)

    # ------------------------------------------------------------
    # OUTPUT MODULE (GUI)
    # ------------------------------------------------------------
    def build_output_section(self):
        frame = tk.LabelFrame(
            self.root, text="Current Queue (sorted by priority)",
            bg=APP_BG, font=("Tahoma", 10, "bold"), padx=10, pady=10
        )
        frame.place(x=460, y=85, width=420, height=420)

        columns = ("queue_no", "name", "age", "priority", "time")
        self.tree = ttk.Treeview(frame, columns=columns, show="headings", height=15)

        self.tree.heading("queue_no", text="No.")
        self.tree.heading("name", text="Name")
        self.tree.heading("age", text="Age")
        self.tree.heading("priority", text="Priority")
        self.tree.heading("time", text="Registered")

        self.tree.column("queue_no", width=35, anchor="center")
        self.tree.column("name", width=130)
        self.tree.column("age", width=40, anchor="center")
        self.tree.column("priority", width=110, anchor="center")
        self.tree.column("time", width=80, anchor="center")

        self.tree.pack(fill="both", expand=True)

        self.summary_label = tk.Label(
            self.root, text="", bg=APP_BG, font=("Tahoma", 9), fg="#333333"
        )
        self.summary_label.place(x=20, y=565)

    # ------------------------------------------------------------
    # EVENT HANDLERS (connect GUI to backend logic)
    # ------------------------------------------------------------
    def handle_add_patient(self):
        name = self.name_entry.get()
        age_str = self.age_entry.get()
        priority = self.priority_var.get()
        reason = self.reason_entry.get("1.0", "end")

        is_valid, result = validate_input(name, age_str)

        if not is_valid:
            messagebox.showerror("Invalid Input", result)
            return

        age = result
        record = add_patient(name, age, priority, reason)
        messagebox.showinfo(
            "Patient Added",
            f"{record['name']} added to queue.\nQueue Number: {record['queue_no']}"
        )
        self.clear_form()
        self.refresh_queue_display()

    def handle_call_next(self):
        next_patient = call_next_patient()

        if next_patient is None:
            messagebox.showwarning("Queue Empty", "There are no patients waiting.")
            self.now_serving_label.config(text="Now Serving: -")
        else:
            self.now_serving_label.config(
                text=f"Now Serving: #{next_patient['queue_no']} "
                     f"{next_patient['name']} ({next_patient['priority']})"
            )
            messagebox.showinfo(
                "Next Patient",
                f"Please call:\n\n{next_patient['name']}\n"
                f"Age: {next_patient['age']}\n"
                f"Priority: {next_patient['priority']}\n"
                f"Reason: {next_patient['reason']}"
            )

        self.refresh_queue_display()

    def clear_form(self):
        self.name_entry.delete(0, "end")
        self.age_entry.delete(0, "end")
        self.reason_entry.delete("1.0", "end")
        self.priority_var.set(PRIORITY_LEVELS[2])

    def handle_exit(self):
        confirm = messagebox.askyesno("Exit", "Are you sure you want to exit?")
        if confirm:
            self.root.destroy()

    # ------------------------------------------------------------
    # REFRESH OUTPUT (Output Module display logic)
    # ------------------------------------------------------------
    def refresh_queue_display(self):
        # Clear current rows
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Repopulate using a loop over the structured patient_queue list
        for patient in patient_queue:
            self.tree.insert("", "end", values=(
                patient["queue_no"],
                patient["name"],
                patient["age"],
                patient["priority"],
                patient["time_registered"]
            ))

        self.summary_label.config(text=get_queue_summary())


# ======================================================================
# PROGRAM ENTRY POINT
# ======================================================================
def main():
    """
    Main function - entry point of the structured program.
    Keeping this separate from the class definition follows
    structured programming practice (clear program flow).
    """
    root = tk.Tk()
    app = ClinicQueueApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
