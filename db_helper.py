# db_helper.py
import mysql.connector
from tkinter import messagebox

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "gd_hms"
}

def get_db_connection():
    try:
        return mysql.connector.connect(**DB_CONFIG)
    except mysql.connector.Error as err:
        messagebox.showerror(
            "🔌 Database Connection Failure",
            f"Failed to connect to MySQL database on host '{DB_CONFIG['host']}'.\n\n"
            f"Error Details: {err}\n\n"
            "Please ensure that:\n"
            "1. Your MySQL server (e.g. WampServer, XAMPP, or Local Service) is active.\n"
            "2. Port 3306 is open and listening.\n"
            "3. The database 'gd_hms' exists."
        )
        raise err
