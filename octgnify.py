# initiallize app with basic settings
import tkinter as tk

from gui import GraphicalUserInterface

root = tk.Tk()
root.title("Octgnify")
root.eval("tk::PlaceWindow . center")
app = GraphicalUserInterface(master=root)
app.mainloop()

OCTGN_DIRECTORY = "E:/Games/Octgn"
INPUT_FILE = "ninjitsu.txt"
OUTPUT_FILE = "ninjistu.o8d"

