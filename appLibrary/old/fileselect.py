import customtkinter as ctk
from tkinter import filedialog
import os
class fselect:
    def __init__(self, root, x, y, height, width):
        self.root = root
        self.x = x
        self.y = y
        self.height = height
        self.width = width

    def select_file(self):
        filepath = filedialog.askopenfilename()
    def init_button(self):
        select_button = ctk.CTkButton(self.root, text="Select File", command=select_file)
        select_button.place(x=self.x, y=self.y)


