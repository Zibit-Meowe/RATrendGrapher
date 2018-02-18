from tkinter import ttk, Tk, Menu
from tkinter.filedialog import askopenfilename
import numpy as np
import numpy.core.defchararray as np_f
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
import matplotlib.dates as mdates
from datetime import datetime
import csv

value_list = []


# This is where we lauch the file manager bar.
def OpenFile():
    name = askopenfilename(initialdir="C:/",
                           filetypes=(("RA CSV File", "*.csv"), ("All Files", "*.*")),
                           title="Choose a file."
                           )
    value_list.append(name)
    data = np.genfromtxt(value_list[0], delimiter=',', skip_header=3900, skip_footer=26516,
                         dtype=(str, str, 'U40', float, float, float), names=['a', 'b', 'c', 'd', 'e', 'f'])

    # x = data['c']
    x = [datetime.strptime(i, '%H:%M:%S;%f') for i in data['c']]
    y = data['d']

    hfmt = matplotlib.dates.DateFormatter('%M:%S:%f')

    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.xaxis.set_major_formatter(hfmt)
    plt.setp(ax.get_xticklabels(), rotation=15)
    ax.plot(x, y, label="Carriage Current Output")
    plt.xlabel('Time')
    plt.ylabel('Amps')
    plt.title('RA Trend Grapher')
    plt.legend()
    plt.show()


root = Tk()
Title = root.title("File Opener")
label = ttk.Label(root, text="Rockwell Trend Grapher", foreground="red", font=("Helvetica", 16))
label.pack()

# Menu Bar

menu = Menu(root)
root.config(menu=menu)

file = Menu(menu)

file.add_command(label='Open', command=OpenFile)
file.add_command(label='Exit', command=lambda: exit())

menu.add_cascade(label='File', menu=file)

root.mainloop()

style.use('ggplot')

# csvname = input("Enter the name of the Rockwell Trend CSV file")


