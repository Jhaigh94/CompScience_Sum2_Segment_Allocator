import tkinter as tk
from tkinter import ttk

Q1_CHOICES = [
    ("TV at time of broadcast", 1),
    ("TV later than original broadcast time (recorded)", 2),
    ("Free on-demand video (iPlayer, My5 etc)", 3),
    ("Paid for on-demand video (Netflix, Prime etc)", 4),
    ("Online video content/live streaming (YouTube, Twitch, TikTok etc)", 5)
]
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
q2_options = ["Disagree strongly", "Disagree", "Neither agree nor disagree", "Agree", "Agree strongly"]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Channel 5 Segment Allocator")
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
        page.tkraise()

class NamePage(ttk.Frame):
    def __init__(self, parent, app):
        ttk.Frame.__init__(self, parent)
        self.app = app
        ttk.Label(self, text="Respondent Name", font=("Arial", 16, "bold")).pack(pady=25)
        ttk.Entry(self, textvariable=app.name_var, width=50).pack()
        self.err = ttk.Label(self, text="", foreground="red")
        self.err.pack()
        ttk.Button(self, text="Next", command=self.go_next).pack(pady=35)
    def go_next(self):
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
        ttk.Button(nav, text="Export (test)", command=self.export).pack(side="right", padx=20)
    def export(self):
        for idx, svar in enumerate(self.app.q2_vars):
            if svar.get() == "":
                self.err.config(text=f"Please answer statement {idx+1}.")
                return
        self.err.config(text="(Would export data here)")

if __name__ == "__main__":
    App().mainloop()
