import tkinter as tk
from tkinter import ttk

Q1_CHOICES = [
    ("TV at time of broadcast", 1),
    ("TV later than original broadcast time (recorded)", 2),
    ("Free on-demand video (iPlayer, My5 etc)", 3),
    ("Paid for on-demand video (Netflix, Prime etc)", 4),
    ("Online video content/live streaming (YouTube, Twitch, TikTok etc)", 5)
]

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Channel 5 Segment Allocator")
        self.geometry("800x600")
        self.name_var = tk.StringVar()
        self.q1_var = tk.IntVar(value=0)
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)
        self.page1 = NamePage(self.container, self)
        self.page2 = Q1Page(self.container, self)
        for page in (self.page1, self.page2):
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
            self.err.config(text="(Would continue to next page here)")

if __name__ == "__main__":
    App().mainloop()
