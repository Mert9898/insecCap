import tkinter as tk
import virus_defibitions
from tkinter import filedialog, messagebox
from scanner import scan_file

def browse_file():
    filename = filedialog.askopenfilename()
    if filename:
        if scan_file(filename, virus_defibitions.db):
            messagebox.showinfo("Scan Result", "File is clean.")
        else:
            messagebox.showwarning("Scan Result", "File is infected.")

app = tk.Tk()
app.title("Antivirus Software")

btn_scan = tk.Button(app, text="Scan File", command=browse_file)
btn_scan.pack(pady=20)

app.mainloop()
