import tkinter as tk
from tkinter import ttk

def check_name():
    name = name_var.get().strip()
    if not name:
        error_label.config(text="Please enter the respondent's name.")
    else:
        error_label.config(text="Name accepted!")

root = tk.Tk()
root.title("Channel 5 Segment Allocator")
root.geometry("800x600")

name_var = tk.StringVar()

ttk.Label(root, text="Respondent Name", font=("Arial", 16, "bold")).pack(pady=30)
name_entry = ttk.Entry(root, textvariable=name_var, width=50)
name_entry.pack()
error_label = ttk.Label(root, text="", foreground="red")
error_label.pack()
ttk.Button(root, text="Next", command=check_name).pack(pady=35)

root.mainloop()
