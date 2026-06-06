# hosteller_dashboard.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import calendar
from tkcalendar import DateEntry
from db_helper import get_db_connection


# --- Hosteller Functions ---
def view_hosteller_info(username):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT first_name, last_name, email, phone_number, year_of_study, department, hostel_name, room_number
        FROM users WHERE username = %s AND role = 'hosteller'
    """, (username,))
    result = cursor.fetchone()

    if not result:
        messagebox.showerror("Error", "Hosteller data not found.")
        return

    info_win = tk.Toplevel()
    info_win.title("Your Information")
    info_win.geometry("400x400")
    info_win.config(bg="#E0FFF0")

    labels = [
        "First Name", "Last Name", "Email", "Phone Number",
        "Year of Study", "Department", "Hostel Name", "Room Number"
    ]

    for label, value in zip(labels, result):
        tk.Label(info_win, text=f"{label}:", font=("Arial", 10, "bold"), bg="#E0FFF0").pack(pady=2, anchor="w", padx=20)
        tk.Label(info_win, text=value, font=("Arial", 10), bg="#E0FFF0").pack(pady=1, anchor="w", padx=40)

    tk.Button(info_win, text="Close", command=info_win.destroy).pack(pady=20)

def manage_attendance(username):
    from tkcalendar import Calendar
    import tkinter as tk
    from tkinter import ttk

    def mark_attendance(status):
        selected_date = cal.get_date()
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO attendance (username, date, status)
                VALUES (%s, %s, %s)
                ON DUPLICATE KEY UPDATE status = VALUES(status)
            """, (username, selected_date, status))
            conn.commit()
            messagebox.showinfo("Success", f"Marked {status} for {selected_date}")
            load_attendance()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def load_attendance():
        for item in tree.get_children():
            tree.delete(item)

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT date, status FROM attendance
            WHERE username = %s ORDER BY date DESC
        """, (username,))
        for date, status in cursor.fetchall():
            tree.insert('', 'end', values=(date, status))
        conn.close()

    att_win = tk.Toplevel()
    att_win.title("Manage Attendance")
    att_win.geometry("500x500")
    att_win.config(bg="#F0FFF0")

    tk.Label(att_win, text="Select a date and mark your attendance:", font=("Arial", 12, "bold"), bg="#F0FFF0").pack(pady=10)

    cal = Calendar(att_win, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack(pady=10)

    btn_frame = tk.Frame(att_win, bg="#F0FFF0")
    btn_frame.pack(pady=10)
    for label, status in [("Present", "P"), ("Absent", "A"), ("Leave", "L")]:
        tk.Button(btn_frame, text=label, width=10, command=lambda s=status: mark_attendance(s)).pack(side="left", padx=5)

    tree = ttk.Treeview(att_win, columns=("Date", "Status"), show="headings")
    tree.heading("Date", text="Date")
    tree.heading("Status", text="Status")
    tree.pack(pady=20, fill="both", expand=True)

    load_attendance()

    tk.Button(att_win, text="Close", command=att_win.destroy).pack(pady=10)

def request_outpass(username):
    def submit_request():
        start_date = start_cal.get_date()
        end_date = end_cal.get_date()
        reason = reason_text.get("1.0", tk.END).strip()

        if start_date > end_date:
            messagebox.showerror("Invalid Dates", "Start date cannot be after end date.")
            return
        if not reason:
            messagebox.showwarning("Missing Reason", "Please enter a reason for your outpass request.")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
        # Get user_id from username
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("User Error", "User not found in the database.")
                return

            user_id = result[0]

        # Insert into outpass_requests with user_id and request_date as NOW()
            cursor.execute("""
                INSERT INTO outpass_requests (user_id, start_date, end_date, reason, status, request_date)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """, (user_id, start_date, end_date, reason, 'Pending'))

            conn.commit()
            messagebox.showinfo("Request Submitted", "Your outpass request has been submitted.")
            outpass_win.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()



    # Create popup window
    outpass_win = tk.Toplevel()
    outpass_win.title("Request Outpass")
    outpass_win.geometry("450x400")
    outpass_win.config(bg="#F5F5DC")

    # Start Date (Dropdown calendar)
    tk.Label(outpass_win, text="Select Start Date:", bg="#F5F5DC", font=("Arial", 12)).pack(pady=5)
    start_cal = DateEntry(outpass_win, date_pattern='yyyy-mm-dd', width=15)
    start_cal.pack(pady=5)

    # End Date (Dropdown calendar)
    tk.Label(outpass_win, text="Select End Date:", bg="#F5F5DC", font=("Arial", 12)).pack(pady=5)
    end_cal = DateEntry(outpass_win, date_pattern='yyyy-mm-dd', width=15)
    end_cal.pack(pady=5)

    # Reason Text Field
    tk.Label(outpass_win, text="Reason for Outpass:", bg="#F5F5DC", font=("Arial", 12)).pack(pady=10)
    reason_text = tk.Text(outpass_win, height=5, width=45, wrap="word", font=("Arial", 10))
    reason_text.pack(pady=5)

    # Buttons
    tk.Button(outpass_win, text="Submit Request", command=submit_request, bg="#4CAF50", fg="white", width=20).pack(pady=15)
    tk.Button(outpass_win, text="Cancel", command=outpass_win.destroy, width=20).pack()


def view_outpass_history(username):
    import tkinter as tk
    from tkinter import ttk, messagebox

    def load_outpass_history():
        for item in tree.get_children():
            tree.delete(item)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Step 1: Get user_id from username
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Error", "User not found in the database.")
                return

            user_id = result[0]

            # Step 2: Fetch outpass history using user_id, including request_id for deletion
            cursor.execute("""
                SELECT request_id, start_date, end_date, reason, status
                FROM outpass_requests
                WHERE user_id = %s
                ORDER BY request_date DESC
            """, (user_id,))
            rows = cursor.fetchall()

            if not rows:
                return

            for row in rows:
                req_id, start_date, end_date, reason, status = row
                tree.insert('', 'end', iid=req_id, values=(start_date, end_date, reason, status))

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def cancel_selected_outpass():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select an outpass request to cancel.")
            return

        req_id = selected_item[0]
        item_values = tree.item(req_id, 'values')
        status = item_values[3]

        if status != "Pending":
            messagebox.showerror("Action Blocked", f"Only 'Pending' requests can be cancelled. Status: '{status}'")
            return

        confirm = messagebox.askyesno("Confirm Cancellation", "Are you sure you want to cancel (delete) this outpass request?")
        if not confirm:
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM outpass_requests WHERE request_id = %s", (req_id,))
            conn.commit()
            messagebox.showinfo("Success", "Outpass request cancelled successfully.")
            load_outpass_history()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    # Create a new window for outpass history
    history_win = tk.Toplevel()
    history_win.title("Outpass History")
    history_win.geometry("600x450")
    history_win.config(bg="#FFF8DC")

    # Heading
    tk.Label(history_win, text="Your Outpass Request History", font=("Arial", 14, "bold"), bg="#FFF8DC").pack(pady=10)

    # Treeview to display the outpass history
    tree = ttk.Treeview(history_win, columns=("Start Date", "End Date", "Reason", "Status"), show="headings")
    tree.heading("Start Date", text="Start Date")
    tree.heading("End Date", text="End Date")
    tree.heading("Reason", text="Reason")
    tree.heading("Status", text="Status")
    tree.pack(pady=10, fill="both", expand=True)

    # Load data
    load_outpass_history()

    # Cancel button
    tk.Button(history_win, text="❌ Cancel Selected Request", font=("Arial", 11, "bold"), bg="#ff6666", fg="white", command=cancel_selected_outpass).pack(pady=5)

    # Close button
    tk.Button(history_win, text="Close", command=history_win.destroy).pack(pady=5)

# --- Hosteller Dashboard ---
    tree.insert('', 'end', values=(date, status))
    conn.close()

    att_win = tk.Toplevel()
    att_win.title("Manage Attendance")
    att_win.geometry("500x500")
    att_win.config(bg="#F0FFF0")

    tk.Label(att_win, text="Select a date and mark your attendance:", font=("Arial", 12, "bold"), bg="#F0FFF0").pack(pady=10)

    cal = Calendar(att_win, selectmode="day", date_pattern="yyyy-mm-dd")
    cal.pack(pady=10)

    btn_frame = tk.Frame(att_win, bg="#F0FFF0")
    btn_frame.pack(pady=10)
    for label, status in [("Present", "P"), ("Absent", "A"), ("Leave", "L")]:
        tk.Button(btn_frame, text=label, width=10, command=lambda s=status: mark_attendance(s)).pack(side="left", padx=5)

    tree = ttk.Treeview(att_win, columns=("Date", "Status"), show="headings")
    tree.heading("Date", text="Date")
    tree.heading("Status", text="Status")
    tree.pack(pady=20, fill="both", expand=True)

    load_attendance()

    tk.Button(att_win, text="Close", command=att_win.destroy).pack(pady=10)

def request_outpass(username):
    def submit_request():
        start_date = start_cal.get_date()
        end_date = end_cal.get_date()
        reason = reason_text.get("1.0", tk.END).strip()

        if start_date > end_date:
            messagebox.showerror("Invalid Dates", "Start date cannot be after end date.")
            return
        if not reason:
            messagebox.showwarning("Missing Reason", "Please enter a reason for your outpass request.")
            return

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
        # Get user_id from username
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()
            if not result:
                messagebox.showerror("User Error", "User not found in the database.")
                return

            user_id = result[0]

        # Insert into outpass_requests with user_id and request_date as NOW()
            cursor.execute("""
                INSERT INTO outpass_requests (user_id, start_date, end_date, reason, status, request_date)
                VALUES (%s, %s, %s, %s, %s, NOW())
            """, (user_id, start_date, end_date, reason, 'Pending'))

            conn.commit()
            messagebox.showinfo("Request Submitted", "Your outpass request has been submitted.")
            outpass_win.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()



    # Create popup window
    outpass_win = tk.Toplevel()
    outpass_win.title("Request Outpass")
    outpass_win.geometry("450x400")
    outpass_win.config(bg="#F5F5DC")

    # Start Date (Dropdown calendar)
    tk.Label(outpass_win, text="Select Start Date:", bg="#F5F5DC", font=("Arial", 12)).pack(pady=5)
    start_cal = DateEntry(outpass_win, date_pattern='yyyy-mm-dd', width=15)
    start_cal.pack(pady=5)

    # End Date (Dropdown calendar)
    tk.Label(outpass_win, text="Select End Date:", bg="#F5F5DC", font=("Arial", 12)).pack(pady=5)
    end_cal = DateEntry(outpass_win, date_pattern='yyyy-mm-dd', width=15)
    end_cal.pack(pady=5)

    # Reason Text Field
    tk.Label(outpass_win, text="Reason for Outpass:", bg="#F5F5DC", font=("Arial", 12)).pack(pady=10)
    reason_text = tk.Text(outpass_win, height=5, width=45, wrap="word", font=("Arial", 10))
    reason_text.pack(pady=5)

    # Buttons
    tk.Button(outpass_win, text="Submit Request", command=submit_request, bg="#4CAF50", fg="white", width=20).pack(pady=15)
    tk.Button(outpass_win, text="Cancel", command=outpass_win.destroy, width=20).pack()


def view_outpass_history(username):
    import tkinter as tk
    from tkinter import ttk, messagebox

    def load_outpass_history():
        for item in tree.get_children():
            tree.delete(item)

        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # Step 1: Get user_id from username
            cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Error", "User not found in the database.")
                return

            user_id = result[0]

            # Step 2: Fetch outpass history using user_id, including request_id for deletion
            cursor.execute("""
                SELECT request_id, start_date, end_date, reason, status
                FROM outpass_requests
                WHERE user_id = %s
                ORDER BY request_date DESC
            """, (user_id,))
            rows = cursor.fetchall()

            if not rows:
                return

            for row in rows:
                req_id, start_date, end_date, reason, status = row
                tree.insert('', 'end', iid=req_id, values=(start_date, end_date, reason, status))

        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    def cancel_selected_outpass():
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("Selection Required", "Please select an outpass request to cancel.")
            return

        req_id = selected_item[0]
        item_values = tree.item(req_id, 'values')
        status = item_values[3]

        if status != "Pending":
            messagebox.showerror("Action Blocked", f"Only 'Pending' requests can be cancelled. Status: '{status}'")
            return

        confirm = messagebox.askyesno("Confirm Cancellation", "Are you sure you want to cancel (delete) this outpass request?")
        if not confirm:
            return

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM outpass_requests WHERE request_id = %s", (req_id,))
            conn.commit()
            messagebox.showinfo("Success", "Outpass request cancelled successfully.")
            load_outpass_history()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            conn.close()

    # Create a new window for outpass history
    history_win = tk.Toplevel()
    history_win.title("Outpass History")
    history_win.geometry("600x450")
    history_win.config(bg="#FFF8DC")

    # Heading
    tk.Label(history_win, text="Your Outpass Request History", font=("Arial", 14, "bold"), bg="#FFF8DC").pack(pady=10)

    # Treeview to display the outpass history
    tree = ttk.Treeview(history_win, columns=("Start Date", "End Date", "Reason", "Status"), show="headings")
    tree.heading("Start Date", text="Start Date")
    tree.heading("End Date", text="End Date")
    tree.heading("Reason", text="Reason")
    tree.heading("Status", text="Status")
    tree.pack(pady=10, fill="both", expand=True)

    # Load data
    load_outpass_history()

    # Cancel button
    tk.Button(history_win, text="❌ Cancel Selected Request", font=("Arial", 11, "bold"), bg="#ff6666", fg="white", command=cancel_selected_outpass).pack(pady=5)

    # Close button
    tk.Button(history_win, text="Close", command=history_win.destroy).pack(pady=5)

# --- Hosteller Dashboard ---
dashboard_themes = {
    "light": {"bg": "#eafaf1", "fg": "#2c3e50", "btn_bg": "lightgreen", "btn_fg": "black"},
    "dark": {"bg": "#0f2027", "fg": "#7fffd4", "btn_bg": "#1c3b47", "btn_fg": "#7fffd4"}
}
current_theme = "light"

def open_hosteller_dashboard(hosteller_username):
    global current_theme
    win = tk.Tk()
    win.title("Hosteller Dashboard")
    from gui_helper import center_window, apply_button_style, apply_label_style
    center_window(win, 600, 520)
    win.config(bg=dashboard_themes[current_theme]["bg"])

    # Greeting & Calendar labels
    greeting = f"Welcome, {hosteller_username}!" if hosteller_username else "Welcome, Hosteller!"
    header_lbl = tk.Label(win, text=greeting, bg=win["bg"])
    header_lbl.pack(pady=15)
    apply_label_style(header_lbl, font_size=16, bold=True, color=dashboard_themes[current_theme]["fg"])

    cal_lbl = tk.Label(win, text=calendar.month_name[datetime.now().month], bg=win["bg"])
    cal_lbl.pack()
    apply_label_style(cal_lbl, font_size=14, bold=True, color=dashboard_themes[current_theme]["fg"])

    # Track buttons to update their theme
    created_buttons = []

    def toggle_theme():
        global current_theme
        current_theme = "dark" if current_theme == "light" else "light"
        theme = dashboard_themes[current_theme]
        win.config(bg=theme["bg"])
        header_lbl.config(bg=theme["bg"], fg=theme["fg"])
        cal_lbl.config(bg=theme["bg"], fg=theme["fg"])
        for text, b in zip([t for t, _ in btns], created_buttons):
            hover_color = "#112630" if current_theme == "dark" else "#b2dfb2"
            if "Theme" in text:
                apply_button_style(b, bg_color="#5bc0de", hover_bg="#31b0d5")
            elif "Logout" in text:
                apply_button_style(b, bg_color="#ff6666", hover_bg="#ff4d4d")
            else:
                apply_button_style(b, bg_color=theme["btn_bg"], fg_color=theme["btn_fg"], hover_bg=hover_color)

    btns = [
        ("📋 View Personal Info", lambda: view_hosteller_info(hosteller_username)),
        ("📅 Manage Attendance", lambda: manage_attendance(hosteller_username)),
        ("📤 Request Out Pass", lambda: request_outpass(hosteller_username)),
        ("🔍 View Out Pass History", lambda: view_outpass_history(hosteller_username)),
        ("🎨 Switch Theme", toggle_theme),
        ("🚪 Logout", win.destroy)
    ]

    for text, cmd in btns:
        btn = tk.Button(win, text=text, command=cmd)
        btn.pack(pady=8)
        # Style properly with hover effects
        hover_color = "#112630" if current_theme == "dark" else "#b2dfb2"
        if "Theme" in text:
            apply_button_style(btn, bg_color="#5bc0de", hover_bg="#31b0d5")
        elif "Logout" in text:
            apply_button_style(btn, bg_color="#ff6666", hover_bg="#ff4d4d")
        else:
            apply_button_style(btn, bg_color=dashboard_themes[current_theme]["btn_bg"], fg_color=dashboard_themes[current_theme]["btn_fg"], hover_bg=hover_color)
        created_buttons.append(btn)

    win.mainloop()
# --- Only run if executed directly ---
if __name__ == "__main__":
    open_hosteller_dashboard()
