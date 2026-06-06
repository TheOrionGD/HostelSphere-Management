#login.py
import tkinter as tk
from tkinter import messagebox
import mysql.connector
import hashlib
from hosteller_dashboard import open_hosteller_dashboard
from warden_dashboard import open_warden_dashboard
from register import open_extended_registration
from db_helper import get_db_connection
from gui_helper import center_window, apply_button_style, apply_label_style, style_entry, THEME

# --- Database Connection ---
try:
    db = get_db_connection()
    cursor = db.cursor()
    print("Database connection successful.")
except Exception:
    exit()

# --- Theme Colors ---
theme_colors = {
    "light": {"bg": "#eafaf1", "fg": "#2c3e50"},
    "dark": {"bg": "#0f2027", "fg": "#7fffd4"}
}
current_theme = "light"

# --- Toggle Theme ---
def toggle_theme(root):
    global current_theme
    current_theme = "dark" if current_theme == "light" else "light"
    root.configure(bg=theme_colors[current_theme]["bg"])
    for widget in root.winfo_children():
        try:
            if isinstance(widget, (tk.Label, tk.Frame)):
                widget.configure(bg=theme_colors[current_theme]["bg"])
                if isinstance(widget, tk.Label):
                    widget.configure(fg=theme_colors[current_theme]["fg"])
            elif isinstance(widget, tk.Entry):
                if current_theme == "dark":
                    widget.configure(bg="#1e293b", fg="#f8fafc", insertbackground="#f8fafc")
                else:
                    widget.configure(bg="#ffffff", fg="#1e293b", insertbackground="#1e293b")
        except tk.TclError:
            pass

# --- Register User ---
def register_user(username, password):
    if not username or not password:
        messagebox.showwarning("⚠️ Incomplete", "Please fill out both fields.")
        return
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    try:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (%s, %s, 'hosteller')",
            (username, hashed_password)
        )
        db.commit()
        messagebox.showinfo("🎉 Success", "User registered successfully!")
    except mysql.connector.IntegrityError:
        messagebox.showerror("❌ Error", "Username already exists.")

# --- Login User ---
def login_user(username, password, win):
    cursor.execute("SELECT user_id, role, password FROM users WHERE username=%s", (username,))
    result = cursor.fetchone()
    if result:
        user_id, role, stored_pass = result
        hashed_input = hashlib.sha256(password.encode()).hexdigest()
        
        # Check against SHA-256 hash or fallback to plaintext check for legacy entries
        if hashed_input == stored_pass or password == stored_pass:
            print(f"User logged in: {username} | Role: {role}")
            win.destroy()
            if role == "warden":
                open_warden_dashboard(username)
            elif role == "hosteller":
                open_hosteller_dashboard(username)
            else:
                messagebox.showerror("Login Error", f"Unknown role: {role}")
        else:
            messagebox.showerror("❌ Login Failed", "Invalid credentials.")
    else:
        messagebox.showerror("❌ Login Failed", "Invalid credentials.")

# --- Login Window ---
def main_login():
    login_win = tk.Tk()
    login_win.title("🔐 Secure Login Portal")
    center_window(login_win, 420, 420)
    login_win.configure(bg=theme_colors[current_theme]["bg"])

    header_lbl = tk.Label(login_win, text="👤 User Access Portal", bg=login_win["bg"])
    header_lbl.pack(pady=20)
    apply_label_style(header_lbl, font_size=16, bold=True, color=theme_colors[current_theme]["fg"])

    user_lbl = tk.Label(login_win, text="🧑‍💻 Username:", bg=login_win["bg"])
    user_lbl.pack(pady=5)
    apply_label_style(user_lbl, font_size=10, bold=True, color=theme_colors[current_theme]["fg"])
    
    username_entry = tk.Entry(login_win, width=30)
    username_entry.pack(pady=5)
    style_entry(username_entry)

    pass_lbl = tk.Label(login_win, text="🔑 Password:", bg=login_win["bg"])
    pass_lbl.pack(pady=5)
    apply_label_style(pass_lbl, font_size=10, bold=True, color=theme_colors[current_theme]["fg"])
    
    password_entry = tk.Entry(login_win, show="*", width=30)
    password_entry.pack(pady=5)
    style_entry(password_entry)

    button_frame = tk.Frame(login_win, bg=login_win["bg"])
    button_frame.pack(pady=20)

    login_btn = tk.Button(button_frame, text="✅ Login", width=12,
                          command=lambda: login_user(username_entry.get(), password_entry.get(), login_win))
    login_btn.grid(row=0, column=0, padx=10)
    apply_button_style(login_btn, bg_color="#2ecc71", hover_bg="#27ae60")

    register_btn = tk.Button(button_frame, text="📝 Register", width=12,
                             command=open_extended_registration)
    register_btn.grid(row=0, column=1, padx=10)
    apply_button_style(register_btn, bg_color="#3498db", hover_bg="#2980b9")

    theme_btn = tk.Button(login_win, text="🎨 Switch Theme", relief="flat", bd=0, cursor="hand2")
    theme_btn.pack(pady=10)
    apply_button_style(theme_btn, bg_color="#78909c", hover_bg="#607d8b")
    
    def on_theme_toggle():
        toggle_theme(login_win)
        header_lbl.configure(bg=login_win["bg"], fg=theme_colors[current_theme]["fg"])
        user_lbl.configure(bg=login_win["bg"], fg=theme_colors[current_theme]["fg"])
        pass_lbl.configure(bg=login_win["bg"], fg=theme_colors[current_theme]["fg"])
        button_frame.configure(bg=login_win["bg"])
        
    theme_btn.configure(command=on_theme_toggle)

    login_win.mainloop()

if __name__ == "__main__":
    main_login()
