import tkinter as tk
from tkinter import ttk

#import is my main GUI project for the Channel 5 segment allocator assignment.import tkinter.filedialog
# It asks for a respondent name, then Q1, then all the Q2 statements.
# It makes sure everything is filled in before you can export to CSV.

# Q1 viewing preference options (label and code)
Q1_CHOICES = [
    ("TV at time of broadcast", 1),
    ("TV later than original broadcast time (recorded)", 2),
    ("Free on-demand video (iPlayer, My5 etc)", 3),
    ("Paid for on-demand video (Netflix, Prime etc)", 4),
    ("Online video content/live streaming (YouTube, Twitch, TikTok etc)", 5)
]

# Q2 attitudinal statements
q2questions = [
    "I prefer to watch TV on my own so there are no distractions",
    "When watching TV I’m using another screen at the same time",
    "I prefer to binge my favourite shows, watching an entire series over a course of a day or week",
    "I post on social media about the TV I’m watching",
    "I follow the shows I’m watching on social media",
    "I read blog posts, reviews or listen to podcasts about my favourite shows",
    "I tend to watch the same things again and again",
    "I watch programmes that people are talking about, so I can join in the conversation",
    "There is enough free TV to watch, without paying for more",
    "I’m the first to seek out new programmes to watch",
    "I have TV on whilst doing something else (i.e. whilst I’m doing household chores or while I’m working)",
    "I watch TV to spend time with my friends and family",
    "I enjoy finding new programmes to watch",
    "I mainly get recommendations for programmes from friends and family"
]

# Attitudinal dropdown options (label only and label→code mapping)
q2_options = [
    "Disagree strongly",
    "Disagree",
    "Neither agree nor disagree",
    "Agree",
    "Agree strongly"
]
q2_lookup = {
    "Disagree strongly": 1,
    "Disagree": 2,
    "Neither agree nor disagree": 3,
    "Agree": 4,
    "Agree strongly": 5
}

class App(tk.Tk):
    def __init__(self):
        # This sets up the window and the three main screens for the app.
        super().__init__()
        self.title("Company Segment Allocator")
        self.geometry("800x600")
        self.name_var = tk.StringVar()
        self.q1_var = tk.IntVar(value=0)
        self.q2_vars = [tk.StringVar(value="") for _ in range(14)]
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.page1 = NamePage(self.container, self)
        self.page2 = Q1Page(self.container, self)
        self.page3 = Q2Page(self.container, self)
        for page in (self.page1, self.page2, self.page3):
            page.grid(row=0, column=0, sticky="nsew")
        self.show_page(self.page1)

    def show_page(self, page):
        # This just makes the right frame come to the front.
        page.tkraise()

    def export_data(self):
        # This is the function that saves everything into a CSV file for marking.
        # It checks that name and Q1 are not missing, but that should never happen.
        if not self.name_var.get().strip():
            tk.messagebox.showerror("Error", "Respondent name missing.")
            return
        if self.q1_var.get() == 0:
            tk.messagebox.showerror("Error", "Q1 response missing.")
            return
        # This puts together the answers for CSV output.
        q2_codes = []
        for svar in self.q2_vars:
            label = svar.get()
            if label in q2_lookup:
                q2_codes.append(q2_lookup[label])
            else:
                q2_codes.append(0)  # Should never happen if validated above
        headers = ["Name", "Q1"] + [f"B5r{i+1}" for i in range(14)]
        row = [self.name_var.get().strip(), self.q1_var.get()] + q2_codes
        # Save as CSV
        path = tk.filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV", "*.csv")])
        if not path:
            return
        with open(path, "w", newline="") as file:
            wr = csv.writer(file)
            wr.writerow(headers)
            wr.writerow(row)
        tk.messagebox.showinfo("Export Complete", f"Responses exported to {path}")

class NamePage(ttk.Frame):
    def __init__(self, parent, app):
        ttk.Frame.__init__(self, parent)
        self.app = app
        ttk.Label(self, text="Respondent Name", font=("Arial", 16, "bold")).pack(pady=25)
        ttk.Entry(self, textvariable=app.name_var, width=50).pack()
        # Add error label for validation messages
        self.err = ttk.Label(self, text="", foreground="red")
        self.err.pack()
        ttk.Button(self, text="Next", command=self.go_next).pack(pady=35)
    def go_next(self):
        # If no name is given, make the user try again.
        name = self.app.name_var.get().strip()
        if not name:
            self.err.config(text="Please enter the respondent's name.")
        else:
            self.err.config(text="")
            self.app.show_page(self.app.page2)

class Q1Page(ttk.Frame):
    def __init__(self, parent, app):
        ttk.Frame.__init__(self, parent)
        self.app = app
        ttk.Label(self, text="Q1. Where do you turn to first?", font=("Arial", 16, "bold")).pack(pady=18, anchor="w")
        for txt, val in Q1_CHOICES:
            ttk.Radiobutton(self, text=txt, variable=app.q1_var, value=val).pack(anchor="w")
        self.err = ttk.Label(self, text="", foreground="red")
        self.err.pack()
        nav = ttk.Frame(self)
        nav.pack(pady=40)
        ttk.Button(nav, text="Back", command=lambda: app.show_page(app.page1)).pack(side="left", padx=20)
        ttk.Button(nav, text="Next", command=self.go_next).pack(side="right", padx=20)
    def go_next(self):
        # Must pick one of the viewing options, or can't go forward.
        if self.app.q1_var.get() == 0:
            self.err.config(text="Please select an answer for Q1.")
        else:
            self.err.config(text="")
            self.app.show_page(self.app.page3)

class Q2Page(ttk.Frame):
    def __init__(self, parent, app):
        ttk.Frame.__init__(self, parent)
        self.app = app
        ttk.Label(self, text="Q2. Attitudinal Statements", font=("Arial", 16, "bold")).pack(pady=20)
        ttk.Label(self, text="Please select one response per statement:", font=("Arial", 12)).pack(anchor="w", pady=4)
        self.combos = []
        for i in range(len(q2questions)):
            # This makes a question label and dropdown for each attitudinal statement.
            frame = ttk.Frame(self)
            frame.pack(fill="x", pady=2)
            ttk.Label(frame, text=f"{i+1}. {q2questions[i]}", width=70, wraplength=490, anchor="w", justify="left").pack(side="left")
            cb = ttk.Combobox(frame, state="readonly", width=25, values=q2_options, textvariable=app.q2_vars[i])
            cb.pack(side="right")
            cb.set("")
            self.combos.append(cb)
        self.err = ttk.Label(self, text="", foreground="red")
        self.err.pack()
        nav = ttk.Frame(self)
        nav.pack(pady=30)
        ttk.Button(nav, text="Back", command=lambda: app.show_page(app.page2)).pack(side="left", padx=20)
        ttk.Button(nav, text="Export to CSV", command=self.export).pack(side="right", padx=20)
    def export(self):
        # Checks all dropdowns are answered. Stops and tells user if not.
        for idx, svar in enumerate(self.app.q2_vars):
            if svar.get() == "":
                self.err.config(text=f"Please answer statement {idx+1}.")
                return
        self.err.config(text="")
        self.app.export_data()

if __name__ == "__main__":
    # This just runs the whole program.
    App().mainloop()
import tkinter.messagebox
import csv



