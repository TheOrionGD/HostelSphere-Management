import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
import mysql.connector
import hashlib
from db_helper import get_db_connection
from gui_helper import center_window, apply_button_style, apply_label_style, style_entry, THEME

# --- Database Connection ---
try:
    db = get_db_connection()
    cursor = db.cursor()
except Exception:
    exit()

# --- Register Hosteller ---
def register_hosteller(data):
    try:
        # Convert data tuple to list, hash password, and convert back
        data_list = list(data)
        data_list[1] = hashlib.sha256(data_list[1].encode()).hexdigest()
        data = tuple(data_list)
        
        query = """
        INSERT INTO users (
            username, password, role, first_name, last_name, email, phone_number,
            year_of_study, department, hostel_name, room_number, DOB
        )
        VALUES (%s, %s, 'hosteller', %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, data)
        db.commit()
        messagebox.showinfo("Success", "Hosteller registered successfully!")
    except mysql.connector.IntegrityError:
        messagebox.showerror("Error", "Username or Email already exists.")
    except Exception as e:
        messagebox.showerror("Database Error", str(e))

# --- Registration Form GUI ---
def open_extended_registration():
    reg_win = tk.Toplevel()  # Use Toplevel since login window remains in background
    reg_win.title("Extended Hosteller Registration")
    center_window(reg_win, 480, 520)
    reg_win.config(bg="white")

    fields = {}

    hdr = tk.Label(reg_win, text="📝 Hosteller Registry Form", bg="white")
    hdr.pack(pady=15)
    apply_label_style(hdr, font_size=14, bold=True, color=THEME["primary"])

    form_frame = tk.Frame(reg_win, bg="white")
    form_frame.pack(padx=20, pady=5)

    labels = [
        "Username", "Password", 
        "First Name", "Last Name", 
        "Email", "Phone Number", 
        "Year of Study", "Department", 
        "Hostel Name", "Room Number", 
        "DOB"
    ]

    for idx, lbl in enumerate(labels):
        r = idx // 2
        c = idx % 2
        
        field_frame = tk.Frame(form_frame, bg="white")
        field_frame.grid(row=r, column=c, padx=12, pady=6, sticky="w")
        
        lbl_obj = tk.Label(field_frame, text=lbl + ":", bg="white")
        lbl_obj.pack(anchor="w", pady=1)
        apply_label_style(lbl_obj, font_size=9, bold=True, color=THEME["text_muted"])
        
        if lbl == "DOB":
            entry = DateEntry(field_frame, date_pattern='yyyy-mm-dd', font=("Segoe UI", 9))
            entry.pack(anchor="w")
        else:
            entry = tk.Entry(field_frame, show="*" if lbl == "Password" else None, width=22)
            entry.pack(anchor="w")
            style_entry(entry)
            
        fields[lbl] = entry

    def on_submit():
        values = [fields[label].get() for label in labels]
        if all(values):
            register_hosteller(tuple(values))
            reg_win.destroy()
        else:
            messagebox.showwarning("Missing Fields", "Please fill in all fields.")

    submit_btn = tk.Button(reg_win, text="Register Profile", command=on_submit)
    submit_btn.pack(pady=20)
    apply_button_style(submit_btn, bg_color=THEME["success"], hover_bg=THEME["success_hover"])

    reg_win.mainloop()

if __name__ == "__main__":
    open_extended_registration()
