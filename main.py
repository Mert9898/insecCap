import tkinter as tk
from tkinter import filedialog, messagebox
from scanner import scan_file, load_signature_db
from real_time_monitor import start_real_time_monitor

# Path to the virus definition database
SIGNATURE_DB_PATH = 'virus_definitions.db'

# Load virus signatures from the database
signature_db = load_signature_db(SIGNATURE_DB_PATH)

def browse_file():
    filename = filedialog.askopenfilename()
    if filename:
        if scan_file(filename, signature_db):
            messagebox.showinfo("Scan Result", "File is clean.")
        else:
            messagebox.showwarning("Scan Result", "File is infected.")

app = tk.Tk()
app.title("Antivirus Software")

btn_scan = tk.Button(app, text="Scan File", command=browse_file)
btn_scan.pack(pady=20)

# Start real-time monitoring
start_real_time_monitor(signature_db)

app.mainloop()
