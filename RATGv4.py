import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from matplotlib import style
import matplotlib.dates as mdates
import matplotlib.pyplot as plt

import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename as getname

import numpy as np

from datetime import datetime

# import numpy.core.defchararray as npdefCA

# import pandas as pd


Large_Font = ("Verdana", 12)

style.use("ggplot")

class ratgraph(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "RA Trend Grapher")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (MainPage, PageOne, PageTwo):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class MainPage(tk.Frame):

    CanClose = 0
    f = Figure(figsize=(8, 5), dpi=96)
    a = f.add_subplot(111)

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Main Page", font=Large_Font)
        label.pack(padx=10, pady=10)

        button1 = ttk.Button(self, text="Open Trend File", command=lambda: self.RetrFileName())
        button1.pack()

        button2 = ttk.Button(self, text="Close Graph", command=lambda: self.CloseGraph())
        button2.pack()

        self.canvas = FigureCanvasTkAgg(self.f, self)

    def RetrFileName(self):
        fname = getname(initialdir="C:/Users/Zibit/Desktop/",
                        filetypes=(("RA CSV File", "*.csv"), ("All Files", "*.*")),
                        title="Load a Trend")

        fname = fname.replace("\\", "/")

        data = np.genfromtxt(fname, delimiter=",", dtype=(str, str, "U40", float, float, float),
                             names=["a", "b", "c", "d", "e", "f"])

        x = [datetime.strptime(i, "%H:%M:%S;%f") for i in data["c"]]
        y = data["d"]

        ToDateFmt = mdates.DateFormatter("%M:%S:%f")

        self.a.xaxis.set_major_formatter(ToDateFmt)
        self.a.plot(x, y, label="Carriage Current Output")
        plt.setp(self.a.get_xticklabels(), rotation=15)
        '''
        
        plt.xlabel("Time")
        plt.ylabel("Amps")
        plt.title("RA Trend Grapher")
        plt.legend()
        
        '''

        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2TkAgg(self.canvas, self)
        toolbar.update()

        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.CanClose = 1

    def CloseGraph(self):
        if self.CanClose == 1:
            self.canvas.get_tk_widget().delete("all")
        else:
            self.CanClose = 0

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page One!!!", font=Large_Font)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(MainPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                             command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Page Two!!!", font=Large_Font)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(MainPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                             command=lambda: controller.show_frame(PageOne))
        button2.pack()


app = ratgraph()
app.mainloop()
