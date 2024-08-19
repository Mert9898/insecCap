import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage
from tkinter.font import Font
from scanner import scan_file, load_signature_db
from real_time_monitor import start_real_time_monitor
from PIL import Image, ImageTk

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
app.title("insecCap Antivirus")
app.geometry("400x300")  # Set window size

image = Image.open("insectCap.png")
image = image.resize((150, 150))  # Resize to 150x150 pixels
logo_image = ImageTk.PhotoImage(image)

# Load logo image
try:
    logo_label = tk.Label(app, image=logo_image)
    logo_label.pack(pady=10)
except tk.TclError:
    print("Logo image 'insectCap.png' not found. Make sure it is in the application directory.")

# Custom font for the title
title_font = Font(family="Helvetica", size=18, weight="bold")

title_label = tk.Label(app, text="ınsecCap", font=title_font)
title_label.pack(pady=10)

btn_scan = tk.Button(app, text="Scan File", command=browse_file, font=("Helvetica", 12), bg="#4CAF50", fg="white", padx=10, pady=5)
btn_scan.pack(pady=20)

# Start real-time monitoring
start_real_time_monitor(signature_db)

app.mainloop()
