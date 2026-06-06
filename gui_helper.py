# gui_helper.py
import tkinter as tk

THEME = {
    "bg": "#f1f5f9",           # Slate 100
    "card": "#ffffff",         # Pure white
    "text": "#1e293b",         # Slate 800
    "text_muted": "#64748b",   # Slate 500
    "primary": "#4f46e5",      # Indigo 600
    "primary_hover": "#4338ca",# Indigo 700
    "success": "#10b981",      # Emerald 500
    "success_hover": "#059669",# Emerald 600
    "danger": "#ef4444",       # Rose 500
    "danger_hover": "#dc2626", # Rose 600
    "warning": "#f59e0b",      # Amber 500
    "warning_hover": "#d97706" # Amber 600
}

def center_window(root, width, height):
    root.update_idletasks()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    root.geometry(f"{width}x{height}+{x}+{y}")

def apply_button_style(btn, bg_color=THEME["primary"], fg_color="#ffffff", hover_bg=THEME["primary_hover"]):
    btn.config(
        font=("Segoe UI", 11, "bold"),
        bg=bg_color,
        fg=fg_color,
        activebackground=hover_bg,
        activeforeground=fg_color,
        relief="flat",
        bd=0,
        padx=15,
        pady=6,
        cursor="hand2"
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=hover_bg))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg_color))

def apply_label_style(lbl, font_size=10, bold=False, color=THEME["text"]):
    weight = "bold" if bold else "normal"
    lbl.config(
        font=("Segoe UI", font_size, weight),
        bg=lbl.master.cget("bg"),
        fg=color
    )

def style_entry(entry):
    entry.config(
        font=("Segoe UI", 10),
        relief="flat",
        bd=1,
        highlightthickness=1,
        highlightbackground="#cbd5e1",
        highlightcolor=THEME["primary"],
        bg="#ffffff",
        fg=THEME["text"]
    )
