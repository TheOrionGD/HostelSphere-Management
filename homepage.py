# HOMEPAGE.PY
import tkinter as tk
from tkinter import messagebox
from gui_helper import center_window, apply_button_style, apply_label_style, THEME

def open_login():
    import login  # Ensure login.py is loaded correctly
    # login.py auto-launches secure login window upon import

def show_homepage():
    root = tk.Tk()
    root.title("🏠 HostelSphere Management System")
    center_window(root, 750, 500)
    root.config(bg=THEME["bg"])

    # --- Navbar Frame ---
    navbar = tk.Frame(root, bg="#ffffff", height=60, bd=0, highlightthickness=1, highlightbackground="#e2e8f0")
    navbar.pack(fill='x', side="top")
    navbar.pack_propagate(False)

    # Logo Text
    logo_lbl = tk.Label(navbar, text="🏠 HostelSphere", bg="#ffffff")
    logo_lbl.pack(side="left", padx=20)
    apply_label_style(logo_lbl, font_size=14, bold=True, color=THEME["primary"])

    # Navbar Action Buttons
    nav_buttons = [
        ("Copyright", lambda: messagebox.showinfo("Copyright", "© 2026 | HostelSphere (GD)")),
        ("Features", lambda: messagebox.showinfo("Features", "Attendance Logs, Outpass Management, Warden Dashboards, Birthday Reminders")),
        ("Home", lambda: messagebox.showinfo("Home", "Welcome to the HostelSphere desktop manager home."))
    ]

    for text, cmd in nav_buttons:
        btn = tk.Button(navbar, text=text, command=cmd, relief="flat", bg="#ffffff", bd=0, cursor="hand2")
        btn.pack(side="right", padx=15, fill="y")
        # Apply modern navigation link styling
        btn.config(font=("Segoe UI", 10, "bold"), fg=THEME["text_muted"])
        btn.bind("<Enter>", lambda e, b=btn: b.config(fg=THEME["primary"]))
        btn.bind("<Leave>", lambda e, b=btn: b.config(fg=THEME["text_muted"]))

    # --- Hero Content Panel ---
    content_frame = tk.Frame(root, bg=THEME["bg"])
    content_frame.pack(expand=True, fill="both", padx=40, pady=30)

    welcome_lbl = tk.Label(content_frame, text="Welcome to HostelSphere Management", bg=THEME["bg"])
    welcome_lbl.pack(pady=10)
    apply_label_style(welcome_lbl, font_size=18, bold=True, color=THEME["text"])

    desc_lbl = tk.Label(content_frame, text="A secure, role-based desktop database manager for campuses.", bg=THEME["bg"])
    desc_lbl.pack(pady=5)
    apply_label_style(desc_lbl, font_size=11, color=THEME["text_muted"])

    get_started_btn = tk.Button(content_frame, text="🚀 Get Started Portal", command=open_login)
    get_started_btn.pack(pady=20)
    apply_button_style(get_started_btn, bg_color=THEME["primary"], hover_bg=THEME["primary_hover"])

    # --- Features Grid ---
    features_lbl = tk.Label(content_frame, text="System Capabilities", bg=THEME["bg"])
    features_lbl.pack(pady=10)
    apply_label_style(features_lbl, font_size=12, bold=True, color=THEME["text"])

    grid_frame = tk.Frame(content_frame, bg=THEME["bg"])
    grid_frame.pack(fill="x", pady=10)

    features = [
        ("📅 Attendance Logs", "Track and manage student daily presence"),
        ("📤 Outpass Auditing", "Submit, approve, or cancel outpass items"),
        ("🎂 Birthday Alerts", "Identify and display today's birthdays"),
        ("🔍 Smart Roster Filters", "Filter student rosters dynamically")
    ]

    for idx, (title, desc) in enumerate(features):
        r = idx // 2
        c = idx % 2
        
        card = tk.Frame(grid_frame, bg="#ffffff", bd=0, highlightthickness=1, highlightbackground="#e2e8f0", padx=15, pady=10)
        card.grid(row=r, column=c, padx=10, pady=8, sticky="nsew")
        grid_frame.columnconfigure(c, weight=1)
        
        c_title = tk.Label(card, text=title, bg="#ffffff")
        c_title.pack(anchor="w")
        apply_label_style(c_title, font_size=10, bold=True, color=THEME["primary"])

        c_desc = tk.Label(card, text=desc, bg="#ffffff")
        c_desc.pack(anchor="w", pady=2)
        apply_label_style(c_desc, font_size=9, color=THEME["text_muted"])

    # --- Footer Bar ---
    footer = tk.Frame(root, bg="#ffffff", height=30, bd=0, highlightthickness=1, highlightbackground="#e2e8f0")
    footer.pack(fill='x', side="bottom")
    footer.pack_propagate(False)

    footer_lbl = tk.Label(footer, text="Academic Semester Submission • Designed for KRCT Systems", bg="#ffffff")
    footer_lbl.pack(expand=True)
    apply_label_style(footer_lbl, font_size=8, color=THEME["text_muted"])

    root.mainloop()

if __name__ == "__main__":
    show_homepage()
