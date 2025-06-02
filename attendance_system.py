import tkinter as tk
from tkinter import messagebox, filedialog
from datetime import datetime
import csv
import re
import os
from PIL import Image, ImageTk

# File names
STUDENT_FILE = "students.txt"
ATTENDANCE_FILE = "attendance.txt"
CSV_EXPORT_FILE = "attendance_export.csv"
PHOTO_DIR = "student_photos"

# Ensure photo directory exists
os.makedirs(PHOTO_DIR, exist_ok=True)

# Admin credentials
ADMIN_USERNAME = "Dharshini V"
ADMIN_PASSWORD = "Cyber"

# Main Application Class
class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("📘 Smart Attendance System")
        self.root.geometry("600x700")  # Reduced size for better compactness
        self.root.configure(bg="#FA8072")  # Salmon background

        self.photo_path = None
        self.is_logged_in = False

        self.create_login_screen()

    # ----------------------- Login Screen ------------------------
    def create_login_screen(self):
        self.clear_screen()

        tk.Label(self.root, text="🔐 Admin Login", font=("Arial", 22, "bold"), fg="#000000", bg="#FA8072").pack(pady=30)

        tk.Label(self.root, text="Username:", font=("Arial", 14), fg="#000000", bg="#FA8072").pack(pady=5)
        self.login_user_entry = tk.Entry(self.root, font=("Arial", 14), width=25)
        self.login_user_entry.pack(pady=5)

        tk.Label(self.root, text="Password:", font=("Arial", 14), fg="#000000", bg="#FA8072").pack(pady=5)
        self.login_pass_entry = tk.Entry(self.root, font=("Arial", 14), width=25, show="*")
        self.login_pass_entry.pack(pady=5)

        login_frame = tk.Frame(self.root, bg="#FA8072")
        login_frame.pack(pady=20)
        
        tk.Button(login_frame, text="Login", width=10, font=("Arial", 12, "bold"), 
                 bg="#28a745", fg="white", command=self.verify_login).pack(side=tk.LEFT, padx=5)
        tk.Button(login_frame, text="Exit", width=10, font=("Arial", 12, "bold"), 
                 bg="#dc3545", fg="white", command=self.root.quit).pack(side=tk.LEFT, padx=5)

    def verify_login(self):
        username = self.login_user_entry.get().strip()
        password = self.login_pass_entry.get().strip()

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            self.is_logged_in = True
            self.create_home_screen()
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    # ----------------------- Home Screen ------------------------
    def create_home_screen(self):
        self.clear_screen()

        # Header with title
        header_frame = tk.Frame(self.root, bg="#FA8072")
        header_frame.pack(pady=20)

        tk.Label(header_frame, text="🎓 Student Attendance System", font=("Arial", 22, "bold"), fg="#000000", bg="#FA8072").pack()

        # Centered clock label below the heading
        self.clock_label = tk.Label(header_frame, font=("Arial", 16, "bold"), fg="#000000", bg="#FA8072")  # Changed text color to black
        self.clock_label.pack(pady=10)  # Centered below the heading
        self.update_clock()

        button_frame = tk.Frame(self.root, bg="#FA8072")
        button_frame.pack(pady=20)

        buttons = [
            ("➕ Add Student", self.create_add_student_screen),
            ("✅ Mark Attendance", self.create_mark_attendance_screen),
            ("📄 View Attendance", self.view_attendance),
            ("🔍 Search Attendance", self.create_search_screen),
            ("🧾 Summary Report", self.view_summary_report),
            ("📆 Filter by Date", self.create_filter_date_screen),
            ("🏫 Filter by Class", self.create_filter_class_screen),
            ("👥 View Students", self.view_students),
            ("📤 Export to CSV", self.export_to_csv),
            ("❌ Delete Student", self.create_delete_screen),
            ("🚪 Logout", self.logout),
            ("❎ Exit", self.root.quit)
        ]

        for (text, command) in buttons:
            tk.Button(button_frame, text=text, width=25, height=1, command=command,
                      bg="#DA4848", fg="white", font=("Arial", 12, "bold")).pack(pady=5, fill=tk.X)  # Changed button color to blue

    def update_clock(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.clock_label.config(text=now)
        self.root.after(1000, self.update_clock)

    def logout(self):
        self.is_logged_in = False
        self.create_login_screen()

    # ----------------------- Add Student Screen ------------------------
    def create_add_student_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="➕ Add Student", font=("Arial", 22, "bold"), bg="#FA8072", fg="#000000").pack(pady=20)

        self.name_entry = self.create_entry("Student Name")
        self.roll_entry = self.create_entry("Roll Number")
        self.class_entry = self.create_entry("Class")

        # Photo upload button and label
        photo_frame = tk.Frame(self.root, bg="#FA8072")
        photo_frame.pack(pady=10)

        tk.Label(photo_frame, text="Upload Photo:", font=("Arial", 12), bg="#FA8072", fg="#000000").pack(side="left")
        tk.Button(photo_frame, text="Choose File", command=self.upload_photo, bg="#4682B4", fg="white", font=("Arial", 10, "bold")).pack(side="left", padx=5)

        self.photo_label = tk.Label(self.root, bg="#FA8072")
        self.photo_label.pack(pady=10)

        button_frame = tk.Frame(self.root, bg="#FA8072")
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="💾 Save", width=10, command=self.add_student, 
                 bg="#28a745", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="🔙 Back", width=10, command=self.create_home_screen, 
                 bg="#dc3545", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5)

    def upload_photo(self):
        filetypes = [("Image files", "*.jpg *.jpeg *.png")]
        filepath = filedialog.askopenfilename(title="Choose student photo", filetypes=filetypes)
        if filepath:
            self.photo_path = filepath
            img = Image.open(filepath)
            img.thumbnail((150, 150))
            self.photo_img = ImageTk.PhotoImage(img)
            self.photo_label.config(image=self.photo_img)

    def create_entry(self, label_text):
        tk.Label(self.root, text=label_text, font=("Arial", 14), bg="#FA8072", fg="#000000").pack(pady=6)
        entry = tk.Entry(self.root, font=("Arial", 14), width=25)
        entry.pack(pady=6)
        return entry

    def validate_name(self, name):
        return bool(re.fullmatch(r"[A-Za-z ]+", name))

    def add_student(self):
        name = self.name_entry.get().strip()
        roll = self.roll_entry.get().strip()
        cls = self.class_entry.get().strip()

        if not name or not roll or not cls:
            messagebox.showerror("Error", "Please fill all fields.")
            return
        if not self.validate_name(name):
            messagebox.showerror("Invalid Name", "Name must contain only letters and spaces.")
            return
        # Check roll uniqueness
        students = self.read_students()
        for s in students:
            if s[1] == roll:
                messagebox.showerror("Duplicate Roll", f"Roll number {roll} already exists.")
                return

        # Save student data
        with open(STUDENT_FILE, "a") as f:
            f.write(f"{name},{roll},{cls}\n")

        # Save photo if uploaded
        if self.photo_path:
            ext = os.path.splitext(self.photo_path)[1]
            photo_save_path = os.path.join(PHOTO_DIR, f"{roll}{ext}")
            try:
                img = Image.open(self.photo_path)
                img.save(photo_save_path)
            except Exception as e:
                messagebox.showwarning("Warning", f"Failed to save photo: {e}")

        messagebox.showinfo("Success", "Student added successfully!")
        self.photo_path = None
        self.create_home_screen()

    def read_students(self):
        students = []
        try:
            with open(STUDENT_FILE, "r") as f:
                for line in f:
                    parts = line.strip().split(",")
                    if len(parts) >= 3:
                        students.append(parts)
        except FileNotFoundError:
            pass
        return students

    # ----------------------- Mark Attendance ------------------------
    def create_mark_attendance_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="✅ Mark Attendance", font=("Arial", 22, "bold"), bg="#FA8072", fg="#000000").pack(pady=20)

        self.att_roll_entry = self.create_entry("Roll Number")
        self.status_entry = self.create_entry("Status (Present/Absent)")

        button_frame = tk.Frame(self.root, bg="#FA8072")
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="💾 Save", width=10, command=self.mark_attendance, 
                 bg="#28a745", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="🔙 Back", width=10, command=self.create_home_screen, 
                 bg="#dc3545", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5)

    def mark_attendance(self):
        roll = self.att_roll_entry.get().strip()
        status = self.status_entry.get().strip().capitalize()
        date = datetime.now().strftime("%Y-%m-%d")

        if not roll or status not in ["Present", "Absent"]:
            messagebox.showerror("Error", "Enter valid roll and status (Present/Absent).")
            return

        # Verify roll exists
        students = self.read_students()
        if not any(s[1] == roll for s in students):
            messagebox.showerror("Error", f"Roll number {roll} not found in students list.")
            return

        updated = False
        records = []

        try:
            with open(ATTENDANCE_FILE, "r") as f:
                records = f.readlines()
        except FileNotFoundError:
            pass

        with open(ATTENDANCE_FILE, "w") as f:
            for record in records:
                r_roll, r_status, r_date = record.strip().split(",")
                if r_roll == roll and r_date == date:
                    f.write(f"{roll},{status},{date}\n")
                    updated = True
                else:
                    f.write(record)
            if not updated:
                f.write(f"{roll},{status},{date}\n")

        msg = "updated" if updated else "marked"
        messagebox.showinfo("Success", f"Attendance {msg} for roll {roll} on {date}.")
        self.create_home_screen()

    # ----------------------- View Attendance ------------------------
    def view_attendance(self):
        self.clear_screen()
        tk.Label(self.root, text="📄 Attendance Records", font=("Arial", 22, "bold"), bg="#FA8072", fg="#000000").pack(pady=20)
        
        # Reduce the height of the text area
        text_area = tk.Text(self.root, width=70, height=10, font=("Consolas", 12))  # Reduced height from 15 to 10
        text_area.pack(pady=10)

        try:
            with open(ATTENDANCE_FILE, "r") as f:
                content = f.read()
                text_area.insert(tk.END, content)
        except FileNotFoundError:
            messagebox.showerror("Error", "Attendance file not found!")

        button_frame = tk.Frame(self.root, bg="#FA8072")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="🔙 Back", command=self.create_home_screen, 
                 bg="#dc3545", fg="white", font=("Arial", 12, "bold")).pack()

    # ----------------------- Attendance Summary ------------------------
    def view_summary_report(self):
        self.clear_screen()
        tk.Label(self.root, text="🧾 Attendance Summary", font=("Arial", 22, "bold"), bg="#FA8072", fg="#000000").pack(pady=20)

        summary = {}
        try:
            with open(ATTENDANCE_FILE, "r") as f:
                for line in f:
                    roll, status, _ = line.strip().split(",")
                    if roll not in summary:
                        summary[roll] = {"Present": 0, "Absent": 0}
                    summary[roll][status] += 1

            text_area = tk.Text(self.root, width=65, height=10, font=("Consolas", 12))
            text_area.pack(pady=10)
            text_area.insert(tk.END, "Roll No\tPresent\tAbsent\n")
            text_area.insert(tk.END, "-------\t-------\t------\n")
            for roll, data in summary.items():
                text_area.insert(tk.END, f"{roll}\t{data['Present']}\t{data['Absent']}\n")
        except FileNotFoundError:
            messagebox.showerror("Error", "Attendance file not found!")

        button_frame = tk.Frame(self.root, bg="#FA8072")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="🔙 Back", command=self.create_home_screen, 
                 bg="#dc3545", fg="white", font=("Arial", 12, "bold")).pack()

    # ----------------------- Search Attendance ------------------------
    def create_search_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="🔍 Search Attendance by Roll Number", font=("Arial", 22, "bold"), bg="#FA8072", fg="#000000").pack(pady=20)
        self.search_roll_entry = self.create_entry("Roll Number")
        
        button_frame = tk.Frame(self.root, bg="#FA8072")
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="🔍 Search", width=10, command=self.search_attendance, 
                 bg="#28a745", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="🔙 Back", width=10, command=self.create_home_screen, 
                 bg="#dc3545", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5)

    def search_attendance(self):
        roll = self.search_roll_entry.get().strip()
        if not roll:
            messagebox.showerror("Error", "Please enter a roll number.")
            return
        results = []
        try:
            with open(ATTENDANCE_FILE, "r") as f:
                for line in f:
                    r_roll, status, date = line.strip().split(",")
                    if r_roll == roll:
                        results.append(f"{date} : {status}")
        except FileNotFoundError:
            messagebox.showerror("Error", "Attendance file not found!")
            return

        if results:
            result_text = "\n".join(results)
            messagebox.showinfo(f"Attendance for Roll {roll}", result_text)
        else:
            messagebox.showinfo("No Records", f"No attendance found for roll {roll}.")

    # ----------------------- Filter by Date ------------------------
    def create_filter_date_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="📆 Filter Attendance by Date", font=("Arial", 22, "bold"), bg="#FA8072", fg="#000000").pack(pady=20)

        self.filter_date_entry = self.create_entry("Date (YYYY-MM-DD)")

        button_frame = tk.Frame(self.root, bg="#FA8072")
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="🔍 Filter", width=10, command=self.filter_by_date, 
                 bg="#28a745", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="🔙 Back", width=10, command=self.create_home_screen, 
                 bg="#dc3545", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5)

    def filter_by_date(self):
        date = self.filter_date_entry.get().strip()
        if not re.match(r"\d{4}-\d{2}-\d{2}", date):
            messagebox.showerror("Error", "Enter a valid date in YYYY-MM-DD format.")
            return

        filtered = []
        try:
            with open(ATTENDANCE_FILE, "r") as f:
                for line in f:
                    roll, status, r_date = line.strip().split(",")
                    if r_date == date:
                        filtered.append(f"Roll: {roll} - Status: {status}")
        except FileNotFoundError:
            messagebox.showerror("Error", "Attendance file not found!")
            return

        if filtered:
            self.show_list_screen(f"Attendance on {date}", filtered)
        else:
            messagebox.showinfo("No Records", f"No attendance found on {date}.")

    # ----------------------- Filter by Class ------------------------
    def create_filter_class_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="🏫 Filter Students by Class", font=("Arial", 22, "bold"), bg="#FA8072", fg="#000000").pack(pady=20)

        students = self.read_students()
        classes = sorted(set(s[2] for s in students))

        if not classes:
            messagebox.showinfo("No Students", "No students data available.")
            self.create_home_screen()
            return

        tk.Label(self.root, text="Select Class:", font=("Arial", 14), bg="#FA8072", fg="#000000").pack(pady=6)
        self.class_var = tk.StringVar(self.root)
        self.class_var.set(classes[0])
        class_dropdown = tk.OptionMenu(self.root, self.class_var, *classes)
        class_dropdown.config(font=("Arial", 12))
        class_dropdown.pack(pady=10)

        button_frame = tk.Frame(self.root, bg="#FA8072")
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="Show Students", command=self.show_students_by_class, 
                 bg="#28a745", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="🔙 Back", command=self.create_home_screen, 
                 bg="#dc3545", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5)

    def show_students_by_class(self):
        selected_class = self.class_var.get()
        students = self.read_students()
        filtered_students = [f"{s[0]} (Roll: {s[1]})" for s in students if s[2] == selected_class]
        if filtered_students:
            self.show_list_screen(f"Students in Class {selected_class}", filtered_students)
        else:
            messagebox.showinfo("No Students", f"No students found in class {selected_class}.")

    # ----------------------- View Students ------------------------
    def view_students(self):
        students = self.read_students()
        if students:
            display_list = [f"Name: {s[0]}, Roll: {s[1]}, Class: {s[2]}" for s in students]
            self.show_list_screen("👥 Students List", display_list)
        else:
            messagebox.showinfo("No Students", "No students found.")

    # ----------------------- Delete Student ------------------------
    def create_delete_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="❌ Delete Student by Roll Number", font=("Arial", 22, "bold"), bg="#FA8072", fg="#000000").pack(pady=20)
        self.delete_roll_entry = self.create_entry("Roll Number")

        button_frame = tk.Frame(self.root, bg="#FA8072")
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="🗑️ Delete", width=10, command=self.delete_student, 
                 bg="#28a745", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="🔙 Back", width=10, command=self.create_home_screen, 
                 bg="#dc3545", fg="white", font=("Arial", 12, "bold")).grid(row=0, column=1, padx=5)

    def delete_student(self):
        roll = self.delete_roll_entry.get().strip()
        if not roll:
            messagebox.showerror("Error", "Please enter a roll number.")
            return
        students = self.read_students()
        new_students = [s for s in students if s[1] != roll]
        if len(new_students) == len(students):
            messagebox.showinfo("Not Found", f"No student found with roll {roll}.")
            return

        with open(STUDENT_FILE, "w") as f:
            for s in new_students:
                f.write(",".join(s) + "\n")

        # Also remove attendance records
        try:
            with open(ATTENDANCE_FILE, "r") as f:
                attendance = f.readlines()
            attendance = [a for a in attendance if not a.startswith(roll + ",")]
            with open(ATTENDANCE_FILE, "w") as f:
                f.writelines(attendance)
        except FileNotFoundError:
            pass

        # Remove photo if exists
        for ext in [".jpg", ".jpeg", ".png"]:
            photo_path = os.path.join(PHOTO_DIR, f"{roll}{ext}")
            if os.path.exists(photo_path):
                os.remove(photo_path)

        messagebox.showinfo("Deleted", f"Student with roll {roll} deleted.")
        self.create_home_screen()

    # ----------------------- Export to CSV ------------------------
    def export_to_csv(self):
        try:
            with open(ATTENDANCE_FILE, "r") as f_in, open(CSV_EXPORT_FILE, "w", newline="") as f_out:
                reader = csv.reader(f_in)
                writer = csv.writer(f_out)
                writer.writerow(["Roll Number", "Status", "Date"])
                for row in reader:
                    writer.writerow(row)
            messagebox.showinfo("Export Successful", f"Attendance data exported to {CSV_EXPORT_FILE}")
        except FileNotFoundError:
            messagebox.showerror("Error", "Attendance file not found!")

        button_frame = tk.Frame(self.root, bg="#FA8072")
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="🔙 Back", command=self.create_home_screen, 
                 bg="#dc3545", fg="white", font=("Arial", 12, "bold")).pack()

    # ----------------------- Utility ------------------------
    def show_list_screen(self, title, items):
        self.clear_screen()
        tk.Label(self.root, text=title, font=("Arial", 22, "bold"), bg="#FA8072", fg="#000000").pack(pady=20)

        # Reduce the height of the listbox
        listbox = tk.Listbox(self.root, width=70, height=10, font=("Arial", 12))  # Reduced height from 25 to 10
        listbox.pack(pady=10)
        for item in items:
            listbox.insert(tk.END, item)

        button_frame = tk.Frame(self.root, bg="#FA8072")
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="🔙 Back", command=self.create_home_screen, 
                 bg="#dc3545", fg="white", font=("Arial", 12, "bold")).pack()

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Run the app
if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()