# warden_dashboard.py

import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import calendar
from tkinter import ttk
from db_helper import get_db_connection


# --- Warden Dashboard ---
warden_themes = {
    "light": {"bg": "#FFF8DC", "fg": "#2c3e50", "btn_bg": "skyblue", "btn_fg": "black"},
    "dark": {"bg": "#1e1900", "fg": "#FFD700", "btn_bg": "#3e3800", "btn_fg": "#FFD700"}
}
current_theme = "light"

def open_warden_dashboard(username):
    global current_theme
    conn = get_db_connection()
    cursor = conn.cursor()
    win = tk.Tk()
    win.title("Warden Dashboard")
    from gui_helper import center_window, apply_button_style, apply_label_style
    center_window(win, 600, 620)
    win.config(bg=warden_themes[current_theme]["bg"])

    # UI Widgets
    greeting = f"Welcome, Warden {username}!"
    header_lbl = tk.Label(win, text=greeting, bg=win["bg"])
    header_lbl.pack(pady=15)
    apply_label_style(header_lbl, font_size=16, bold=True, color=warden_themes[current_theme]["fg"])

    cal_label = tk.Label(win, text=calendar.month_name[datetime.now().month], bg=win["bg"])
    cal_label.pack()
    apply_label_style(cal_label, font_size=14, bold=True, color=warden_themes[current_theme]["fg"])

    created_buttons = []

    def toggle_theme():
        global current_theme
        current_theme = "dark" if current_theme == "light" else "light"
        theme = warden_themes[current_theme]
        win.config(bg=theme["bg"])
        header_lbl.config(bg=theme["bg"], fg=theme["fg"])
        cal_label.config(bg=theme["bg"], fg=theme["fg"])
        for text, b in zip([t for t, _ in btns], created_buttons):
            hover_color = "#292400" if current_theme == "dark" else "#87ceeb"
            if "Theme" in text:
                apply_button_style(b, bg_color="#5bc0de", hover_bg="#31b0d5")
            elif "Logout" in text:
                apply_button_style(b, bg_color="#ff6666", hover_bg="#ff4d4d")
            else:
                apply_button_style(b, bg_color=theme["btn_bg"], fg_color=theme["btn_fg"], hover_bg=hover_color)

    btns = [
        ("View Attendance", view_attendance),
        ("📤 Approve Out Passes", approve_outpass),
        ("📋 View Hostellers", view_hostellers),
        ("📅 Attendance Overview", view_attendance_summary),
        ("🎂 Birthday Alerts", show_birthday_alerts),
        ("🔍 Filter Hostellers", filter_hostellers),
        ("🎨 Switch Theme", toggle_theme),
        ("🚪 Logout", win.destroy)
    ]
    for text, cmd in btns:
        btn = tk.Button(win, text=text, command=cmd)
        btn.pack(pady=8)
        hover_color = "#292400" if current_theme == "dark" else "#87ceeb"
        if "Theme" in text:
            apply_button_style(btn, bg_color="#5bc0de", hover_bg="#31b0d5")
        elif "Logout" in text:
            apply_button_style(btn, bg_color="#ff6666", hover_bg="#ff4d4d")
        else:
            apply_button_style(btn, bg_color=warden_themes[current_theme]["btn_bg"], fg_color=warden_themes[current_theme]["btn_fg"], hover_bg=hover_color)
        created_buttons.append(btn)

    win.mainloop()

# --- Warden Functional Placeholders ---
def view_attendance():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        query = """
            SELECT u.username, u.first_name, u.last_name, a.date, a.status
            FROM attendance a
            JOIN users u ON a.username = u.username
            ORDER BY a.date DESC
        """
        cursor.execute(query)
        records = cursor.fetchall()

        if not records:
            messagebox.showinfo("Attendance", "No attendance records found.")
            return

        att_win = tk.Toplevel()
        att_win.title("Attendance Records")
        att_win.geometry("700x400")
        att_win.config(bg="white")

        tk.Label(att_win, text="Attendance Records", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        frame = tk.Frame(att_win, bg="white")
        frame.pack(fill="both", expand=True)

        headings = ["Username", "First Name", "Last Name", "Date", "Status"]
        for idx, heading in enumerate(headings):
            tk.Label(frame, text=heading, font=("Arial", 10, "bold"), bg="lightgray", width=15, borderwidth=1, relief="solid").grid(row=0, column=idx)

        for row_idx, row in enumerate(records, start=1):
            for col_idx, value in enumerate(row):
                tk.Label(frame, text=value, font=("Arial", 10), bg="white", width=15, borderwidth=1, relief="solid").grid(row=row_idx, column=col_idx)

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching attendance records:\n{err}")

def approve_outpass():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to get pending outpass requests
        query = """
            SELECT o.request_id, u.first_name, u.last_name, o.request_date, o.start_date, o.end_date, o.reason
            FROM outpass_requests o
            JOIN users u ON o.user_id = u.user_id
            WHERE o.status = 'Pending'
        """
        cursor.execute(query)
        records = cursor.fetchall()

        if not records:
            messagebox.showinfo("Approve Outpass", "No pending outpasses found.")
            return

        # Create a new window to display pending outpasses
        outpass_win = tk.Toplevel()
        outpass_win.title("Approve Outpass Requests")
        outpass_win.geometry("900x400")
        outpass_win.config(bg="white")

        tk.Label(outpass_win, text="Pending Outpass Requests", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        frame = tk.Frame(outpass_win, bg="white")
        frame.pack(fill="both", expand=True)

        # Create headings
        headings = ["Request ID", "First Name", "Last Name", "Request Date", "Start Date", "End Date", "Reason", "Action"]
        for idx, heading in enumerate(headings):
            tk.Label(frame, text=heading, font=("Arial", 10, "bold"), bg="lightgray", width=15, borderwidth=1, relief="solid").grid(row=0, column=idx)

        # Display pending outpasses
        for row_idx, row in enumerate(records, start=1):
            for col_idx, value in enumerate(row[:-1]):  # All columns except the last "Reason" column
                # Handle NULL in request_date by showing "Not Set" or any placeholder
                display_value = value if value is not None else "Not Set"
                tk.Label(frame, text=display_value, font=("Arial", 10), bg="white", width=15, borderwidth=1, relief="solid").grid(row=row_idx, column=col_idx)
            
            # Reason column
            tk.Label(frame, text=row[6], font=("Arial", 10), bg="white", width=15, borderwidth=1, relief="solid").grid(row=row_idx, column=6)

            # Add approve/reject buttons
            approve_btn = tk.Button(frame, text="Approve", command=lambda id=row[0]: update_outpass_status(id, 'Approved', outpass_win))
            reject_btn = tk.Button(frame, text="Reject", command=lambda id=row[0]: update_outpass_status(id, 'Rejected', outpass_win))
            approve_btn.grid(row=row_idx, column=7, padx=5)
            reject_btn.grid(row=row_idx, column=8, padx=5)

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching outpass records:\n{err}")

def update_outpass_status(outpass_id, status, window):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Update the outpass status (approve/reject)
        update_query = """
            UPDATE outpass_requests
            SET status = %s, request_date = IFNULL(request_date, NOW())  -- Set request_date if it's NULL
            WHERE request_id = %s
        """
        cursor.execute(update_query, (status, outpass_id))
        conn.commit()

        messagebox.showinfo("Outpass Status", f"Outpass has been {status.lower()}.")

        # Close the window after updating the status
        window.destroy()

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error updating outpass status:\n{err}")

def view_hostellers():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to fetch all hostellers
        query = """
            SELECT user_id, first_name, last_name, email, phone_number, year_of_study, department, hostel_name, room_number
            FROM users
            WHERE role = 'hosteller';
        """
        cursor.execute(query)
        hostellers = cursor.fetchall()

        if not hostellers:
            messagebox.showinfo("View Hostellers", "No hostellers found.")
            return

        # Create a new window to display hostellers
        hosteller_win = tk.Toplevel()
        hosteller_win.title("List of Hostellers")
        hosteller_win.geometry("800x400")
        hosteller_win.config(bg="white")

        tk.Label(hosteller_win, text="List of Hostellers", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        frame = tk.Frame(hosteller_win, bg="white")
        frame.pack(fill="both", expand=True)

        # Create headings for the table
        headings = ["User ID", "First Name", "Last Name", "Email", "Phone", "Year of Study", "Department", "Hostel Name", "Room Number"]
        for idx, heading in enumerate(headings):
            tk.Label(frame, text=heading, font=("Arial", 10, "bold"), bg="lightgray", width=15, borderwidth=1, relief="solid").grid(row=0, column=idx)

        # Display all hostellers
        for row_idx, row in enumerate(hostellers, start=1):
            for col_idx, value in enumerate(row):
                tk.Label(frame, text=value, font=("Arial", 10), bg="white", width=15, borderwidth=1, relief="solid").grid(row=row_idx, column=col_idx)

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching hostellers:\n{err}")

def view_attendance_summary():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get the current month and year
        current_month = datetime.now().month
        current_year = datetime.now().year

        # Query to get total attendance records for the current month
        query = """
            SELECT u.first_name, u.last_name, a.status
            FROM attendance a
            JOIN users u ON a.username = u.username
            WHERE MONTH(a.date) = %s AND YEAR(a.date) = %s;
        """
        cursor.execute(query, (current_month, current_year))
        attendance_records = cursor.fetchall()

        if not attendance_records:
            messagebox.showinfo("Attendance Summary", "No attendance records found for the current month.")
            return

        # Calculate the summary details
        total_hostellers = len(set([record[0] + " " + record[1] for record in attendance_records]))  # unique hostellers
        present_count = sum(1 for record in attendance_records if record[2] == 'P')
        absent_count = sum(1 for record in attendance_records if record[2] == 'A')
        leave_count = sum(1 for record in attendance_records if record[2] == 'L')

        attendance_percentage = (present_count / len(attendance_records)) * 100 if attendance_records else 0

        # Create a new window to display the attendance summary
        summary_win = tk.Toplevel()
        summary_win.title("Attendance Summary")
        summary_win.geometry("400x300")
        summary_win.config(bg="white")

        tk.Label(summary_win, text="Attendance Summary", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        # Display the summary information
        summary_text = f"""
        Total Hostellers: {total_hostellers}
        Present: {present_count}
        Absent: {absent_count}
        On Leave: {leave_count}
        Attendance Percentage: {attendance_percentage:.2f}%
        """
        tk.Label(summary_win, text=summary_text, font=("Arial", 12), bg="white").pack(pady=20)

        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        messagebox.showerror("Database Error", f"Error fetching attendance summary:\n{err}")

def show_birthday_alerts():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        # Get today's month and day (ignore the year)
        today = datetime.now()
        today_month_day = today.strftime('%m-%d')

        # Query to get users with today's birthday (ignoring the year)
        query = """
            SELECT first_name, last_name, email
            FROM users
            WHERE DATE_FORMAT(DOB, '%m-%d') = %s;
        """
        cursor.execute(query, (today_month_day,))
        birthday_users = cursor.fetchall()

        if not birthday_users:
            messagebox.showinfo("Birthday Alerts", "No birthdays today.")
            return

        # Create a new window to display today's birthdays
        birthday_win = tk.Toplevel()
        birthday_win.title("Birthday Alerts")
        birthday_win.geometry("400x300")
        birthday_win.config(bg="white")

        tk.Label(birthday_win, text="Today's Birthdays", font=("Arial", 14, "bold"), bg="white").pack(pady=10)

        # Display the list of birthday users
        birthday_text = "\n".join([f"{user[0]} {user[1]} (Email: {user[2]})" for user in birthday_users])
        tk.Label(birthday_win, text=birthday_text, font=("Arial", 12), bg="white").pack(pady=20)

        cursor.close()
        conn.close()

    except Exception as err:
        messagebox.showerror("Database Error", f"Error fetching birthday list:\n{err}")


def filter_hostellers():
    def apply_filter():
        hostel_name = hostel_name_var.get()
        department = department_var.get()
        year_of_study = year_of_study_var.get()
        search_query = search_entry.get().strip()

        # Build the query based on the provided filter values
        query = "SELECT first_name, last_name, hostel_name, department, year_of_study FROM users WHERE role = 'hosteller'"

        # Collect filter conditions
        conditions = []
        params = []

        if hostel_name != "All Hostels":
            conditions.append("hostel_name = %s")
            params.append(hostel_name)
        if department != "All Departments":
            conditions.append("department = %s")
            params.append(department)
        if year_of_study != "All Years":
            conditions.append("year_of_study = %s")
            params.append(year_of_study)
        if search_query:
            conditions.append("(first_name LIKE %s OR last_name LIKE %s OR email LIKE %s OR username LIKE %s)")
            wildcard = f"%{search_query}%"
            params.extend([wildcard, wildcard, wildcard, wildcard])

        # Add conditions to the query if any filters are applied
        if conditions:
            query += " AND " + " AND ".join(conditions)

        # Execute the query
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(query, tuple(params))
            filtered_hostellers = cursor.fetchall()

            # Display the filtered results
            if filtered_hostellers:
                result_window = tk.Toplevel()
                result_window.title("Filtered Hostellers")
                result_window.geometry("600x400")
                result_window.config(bg="white")

                # Create a Label to show the count of filtered hostellers
                count_label = tk.Label(result_window, text=f"Total Hostellers Found: {len(filtered_hostellers)}", font=("Arial", 14, "bold"), bg="white")
                count_label.pack(pady=10)

                # Create a Treeview widget to display the filtered hostellers in columns
                tree = ttk.Treeview(result_window, columns=("First Name", "Last Name", "Hostel Name", "Department", "Year of Study"), show="headings")
                
                # Define the columns
                tree.heading("First Name", text="First Name")
                tree.heading("Last Name", text="Last Name")
                tree.heading("Hostel Name", text="Hostel Name")
                tree.heading("Department", text="Department")
                tree.heading("Year of Study", text="Year of Study")

                # Define the column widths
                tree.column("First Name", width=150)
                tree.column("Last Name", width=150)
                tree.column("Hostel Name", width=120)
                tree.column("Department", width=120)
                tree.column("Year of Study", width=100)

                # Insert the filtered data into the Treeview
                for hosteller in filtered_hostellers:
                    tree.insert("", tk.END, values=hosteller)

                # Add a scrollbar to the Treeview
                scrollbar = ttk.Scrollbar(result_window, orient="vertical", command=tree.yview)
                tree.configure(yscrollcommand=scrollbar.set)
                scrollbar.pack(side="right", fill="y")

                tree.pack(pady=20)

            else:
                messagebox.showinfo("No Results", "No hostellers found matching the filter criteria.")
            
            cursor.close()
            conn.close()

        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Error fetching hosteller data:\n{err}")

    # Create a new window for filter options
    filter_win = tk.Toplevel()
    filter_win.title("Filter Hostellers")
    filter_win.geometry("400x380")
    filter_win.config(bg="white")

    # Name Search Field
    tk.Label(filter_win, text="Search by Name or Email (Optional)", bg="white").pack(pady=5)
    search_entry = tk.Entry(filter_win, font=("Arial", 12), width=25)
    search_entry.pack(pady=5)

    # Hostel Name Dropdown
    tk.Label(filter_win, text="Filter by Hostel Name", bg="white").pack(pady=5)
    hostel_name_var = tk.StringVar()
    hostel_name_dropdown = ttk.Combobox(filter_win, textvariable=hostel_name_var, font=("Arial", 12))
    hostel_name_dropdown['values'] = ["All Hostels", "Hostel A", "Hostel B", "Hostel C"]  # Example hostel names
    hostel_name_dropdown.current(0)  # Set default value to "All Hostels"
    hostel_name_dropdown.pack(pady=5)

    # Department Dropdown
    tk.Label(filter_win, text="Filter by Department", bg="white").pack(pady=5)
    department_var = tk.StringVar()
    department_dropdown = ttk.Combobox(filter_win, textvariable=department_var, font=("Arial", 12))
    department_dropdown['values'] = ["All Departments", "Computer Science", "Mechanical", "Electrical"]  # Example departments
    department_dropdown.current(0)  # Set default value to "All Departments"
    department_dropdown.pack(pady=5)

    # Year of Study Dropdown
    tk.Label(filter_win, text="Filter by Year of Study", bg="white").pack(pady=5)
    year_of_study_var = tk.StringVar()
    year_of_study_dropdown = ttk.Combobox(filter_win, textvariable=year_of_study_var, font=("Arial", 12))
    year_of_study_dropdown['values'] = ["All Years", "1", "2", "3", "4"]  # Example year of study options
    year_of_study_dropdown.current(0)  # Set default value to "All Years"
    year_of_study_dropdown.pack(pady=5)

    # Apply Filter Button
    tk.Button(filter_win, text="Apply Filter", font=("Arial", 12), bg="skyblue", command=apply_filter).pack(pady=20)

# --- Only run when directly executed ---
if __name__ == "__main__":
    open_warden_dashboard()
