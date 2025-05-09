import tkinter as tk

# Right now, a user's ratings are fetching and passed into this GUI as ratings IF they select to view history.
# TODO: (Elijah) - Cleanse the ratings input, and display it cleanly in a tkinker GUI (currently only plaintext), display the 5 latest or more if it isn't too messy.
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
