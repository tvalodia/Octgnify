import tkinter
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.scrolledtext import ScrolledText

from deck_converter import DeckConverter

TEXT_ENTRY_WIDTH = 50


class GraphicalUserInterface(tk.Frame):

    def __init__(self, master=None):
        super().__init__(master)
        self.message_box = None
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.octgn_installation_path = tk.StringVar()

        self.bg_colour = "#3d6466"
        self.main_frame = tk.Frame(master, width=800, height=600, bg=self.bg_colour)
        # self.main_frame.pack()
        self.main_frame.grid_propagate(True)
        # place frame widgets in window
        self.main_frame.grid(row=0, column=0, sticky="nesw")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # load the first frame
        self.load_main_frame()

    def clear_widgets(self, frame):
        # select all frame widgets and delete them
        for widget in frame.winfo_children():
            widget.destroy()

    def load_main_frame(self):
        self.main_frame.tkraise()

        tk.Label(
            self.main_frame,
            text="Octgnify",
            bg=self.bg_colour,
            fg="white",
            pady=10,
            font=("Shanti", 18)
        ).grid(row=0, column=0, columnspan=3, padx=5, pady=5)

        tk.Label(
            self.main_frame,
            text="Deck source:",
            bg=self.bg_colour,
            fg="white",
            pady=5,
            font=("Shanti", 14),
            anchor='w'
        ).grid(row=1, column=0, padx=5, pady=5, sticky="E")

        current_value = tk.StringVar()
        deck_source = ttk.Combobox(self.main_frame, textvariable=current_value)
        deck_source['values'] = 'ManaBox'
        deck_source['state'] = 'readonly'
        deck_source.grid(row=1, column=1, padx=5, pady=5, sticky="W")
        deck_source.set("ManaBox")

        tk.Label(
            self.main_frame,
            text="Input file:",
            bg=self.bg_colour,
            fg="white",
            pady=5,
            font=("Shanti", 14),
            anchor='w'
        ).grid(row=2, column=0, padx=5, pady=5, sticky="E")

        tk.Entry(self.main_frame,
                 width=TEXT_ENTRY_WIDTH,
                 textvariable=self.input_file) \
            .grid(row=2, column=1, padx=5, pady=5, sticky="W")

        # create button widget
        tk.Button(
            self.main_frame,
            text="...",
            font=("Ubuntu", 14),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command=lambda: self.select_input_file()
        ).grid(row=2, column=2, padx=5, pady=5, sticky="W")

        tk.Label(
            self.main_frame,
            text="Output file:",
            bg=self.bg_colour,
            fg="white",
            pady=5,
            font=("Shanti", 14),
            anchor='w'
        ).grid(row=3, column=0, padx=5, pady=5, sticky="E")

        tk.Entry(self.main_frame, width=TEXT_ENTRY_WIDTH, textvariable=self.output_file) \
            .grid(row=3, column=1, padx=5, pady=5, sticky="W")

        # create button widget
        tk.Button(
            self.main_frame,
            text="...",
            font=("Ubuntu", 14),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command=lambda: self.select_output_file()
        ).grid(row=3, column=2, padx=5, pady=5, sticky="W")

        tk.Label(
            self.main_frame,
            text="Octgn path:",
            bg=self.bg_colour,
            fg="white",
            pady=5,
            font=("Shanti", 14),
            anchor='w'
        ).grid(row=4, column=0, padx=5, pady=5, sticky="E")

        tk.Entry(self.main_frame, width=TEXT_ENTRY_WIDTH, textvariable=self.octgn_installation_path) \
            .grid(row=4, column=1, padx=5, pady=5, sticky="W")

        # create button widget
        tk.Button(
            self.main_frame,
            text="...",
            font=("Ubuntu", 14),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command=lambda: self.select_octgn_installation_path()
        ).grid(row=4, column=2, padx=5, pady=5, sticky="W")

        # create button widget
        tk.Button(
            self.main_frame,
            text="Convert",
            font=("Ubuntu", 14),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command=lambda: self.convert()

        ).grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="NESW")

        self.message_box = ScrolledText(self.main_frame, state='disabled')
        self.message_box.grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky="NESW")

    def select_input_file(self):
        filetypes = (
            ('text files', '*.txt'),
            ('All files', '*.*')
        )

        self.input_file.set(fd.askopenfilename(
            title='Open a file',
            initialdir='/',
            filetypes=filetypes))

    def select_octgn_installation_path(self):
        self.octgn_installation_path.set(fd.askdirectory(
            title='Open a file',
            initialdir='/'))

    def select_output_file(self):
        filetypes = (
            ('o8d files', '*.o8d'),
            ('All files', '*.*')
        )

        self.output_file.set(fd.asksaveasfilename(
            title='Save a file',
            initialdir='/',
            defaultextension=".o8d",
            filetypes=filetypes))

    def convert(self):
        try:
            deck_converter = DeckConverter(self.octgn_installation_path.get(), self.input_file.get(), self.output_file.get())
            deck_converter.add_listener(self)
            deck_converter.convert()
        except FileNotFoundError as fnf:
            self.on_message(str(fnf))
            self.on_complete()

    def on_start(self):
        print("handle start")

    def on_complete(self):
        self.on_message("Deck conversion completed.")

    def on_message(self, message):
        self.message_box.configure(state='normal')
        self.message_box.insert(tkinter.END, message + '\n')
        self.message_box.configure(state='disabled')
