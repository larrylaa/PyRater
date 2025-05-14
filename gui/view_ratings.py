import tkinter as tk

# Right now, a user's ratings are fetching and passed into this GUI as ratings IF they select to view history.
# TODO: (Elijah) - Cleanse the ratings input, and display it cleanly in a tkinter GUI (currently only plaintext), display the 5 latest or more if it isn't too messy.

from tkinter import ttk
from datetime import datetime

import tkinter as tk
from tkinter import ttk
from datetime import datetime

class ViewRatingsGUI:
    def __init__(self, master, username, ratings):
        self.master = master
        self.username = username
        self.raw_ratings = self.cleanse_ratings(ratings)
        master.title(f"PyRater - {username}'s Rating History")

        tk.Label(master, text=f"{username}'s Resume Ratings", font=('Helvetica', 14, 'bold')).pack(pady=10)

        frame = tk.Frame(master)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        columns = ('date', 'score', 'feedback')
        self.tree = ttk.Treeview(frame, columns=columns, show='headings', height=8)

        self.tree.heading('date', text='Date Rated')
        self.tree.heading('score', text='Score')
        self.tree.heading('feedback', text='Summary Feedback')

        self.tree.column('date', width=120, anchor='center')
        self.tree.column('score', width=80, anchor='center')
        self.tree.column('feedback', width=500, anchor='w')

        scrollbar = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tree.bind("<Double-1>", self.open_detail_popup)

        self.populate_table()

    def cleanse_ratings(self, ratings):
        """
        Filter and format ratings for display.
        Return list of dicts with relevant fields.
        """
        clean = []
        for r in ratings:
            if r.get('type') != 'Resume Rater':
                continue

            raw_date = r.get('created_at', '')[:10]
            try:
                date_str = datetime.strptime(raw_date, '%Y-%m-%d').strftime('%b %d, %Y')
            except ValueError:
                date_str = raw_date

            entry = {
                'date': date_str,
                'score': r.get('rating', 'N/A'),
                'feedback': r.get('feedback', '').strip(),
                'improvements': r.get('improvements', '').strip(),
                'resume': r.get('resume', '').strip(),
            }

            clean.append(entry)

        return clean[-5:]  # Last 5 ratings

    def populate_table(self):
        if not self.raw_ratings:
            self.tree.insert('', tk.END, values=("No ratings available.", "", ""))
        else:
            for entry in self.raw_ratings:
                short_feedback = entry['feedback'].replace('\n', ' ')
                short_feedback = (short_feedback[:120] + '...') if len(short_feedback) > 120 else short_feedback
                self.tree.insert('', tk.END, values=(entry['date'], entry['score'], short_feedback))

    def open_detail_popup(self, event):
        selected = self.tree.selection()
        if not selected:
            return

        index = self.tree.index(selected[0])
        data = self.raw_ratings[index]

        popup = tk.Toplevel(self.master)
        popup.title("Rating Details")
        popup.geometry("700x600")

        title = f"Rated on {data['date']} | Score: {data['score']}"
        tk.Label(popup, text=title, font=('Helvetica', 12, 'bold')).pack(pady=10)

        for section_title, content in [
            ("Full Feedback", data['feedback']),
            ("Suggestions for Improvement", data['improvements']),
            ("Resume Text", data['resume'])
        ]:
            tk.Label(popup, text=section_title, font=('Helvetica', 10, 'bold')).pack(anchor='w', padx=10, pady=(10, 0))
            text_widget = tk.Text(popup, wrap=tk.WORD, height=8)
            text_widget.insert(tk.END, content)
            text_widget.config(state=tk.DISABLED)
            text_widget.pack(padx=10, pady=5, fill=tk.BOTH, expand=False)

def start_viewer(username, ratings):
    print("Starting Rating Viewer...")
    root = tk.Tk()
    ViewRatingsGUI(root, username, ratings)
    root.mainloop()
