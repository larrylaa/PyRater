import tkinter as tk
from tkinter import filedialog, messagebox
from pdfminer.high_level import extract_text
import os

# TODO: FOR ELIJAH
class ViewRatingsGUI:
    def __init__(self, master, username, ratings):
        self.master = master
        self.username = username
        self.ratings = ratings
        master.title("PyRater - Ratings History")

def start_viewer(username, ratings):
    print("Starting Rating Viewer...")
    root = tk.Tk()
    ViewRatingsGUI(root, username, ratings)
    root.mainloop()
