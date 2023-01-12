from upDownTime import mon_net_connection
from pingPlotter import *
from process import *
import threading
from tkinter import *

gui_window = Tk()
gui_window.geometry("300x300")
gui_window.title("Ping Plotter")

graph_button = Button(gui_window,
                      text="Generate graph",
                      command=Graph_Generator)
graph_button.pack(pady=30)

def process():
    message=buildBaseline()
    
prob_button = Button(gui_window, text="prob", command=buildBaseline)
process_button = Button(gui_window,
                        text="Processes using network",
                        command=checkConnections)

text_box = Text(
    gui_window,
    height=12,
    width=40
)
text_box.pack()
text_box.insert('end', message)

gui_window.columnconfigure(0, weight=1)
gui_window.columnconfigure(1, weight=3)

graph_button.grid(column=0, row=0, sticky=W, padx=5, pady=5)
prob_button.grid(column=0, row=1, sticky=W, padx=5, pady=5)
text_box.grid(column=1, row=0, sticky=E, padx=5, pady=5)

process_button.grid(column=1, row=0, sticky=W, padx=5, pady=5)

gui_window.mainloop()