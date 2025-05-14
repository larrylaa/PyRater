import tkinter as tk

# Right now, a user's ratings are fetching and passed into this GUI as ratings IF they select to view history.
# TODO: (Elijah) - Cleanse the ratings input, and display it cleanly in a tkinter GUI (currently only plaintext), display the 5 latest or more if it isn't too messy.

from tkinter import ttk
from datetime import datetime

class ViewRatingsGUI:
    def __init__(self, master, username, ratings):
        self.master = master
        self.username = username
        self.cleaned = self.cleanse_ratings(ratings)

        master.title(f"PyRater - {username}'s Rating History")

        notebook = ttk.Notebook(master)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.resume_tab = tk.Frame(notebook)
        self.job_tab = tk.Frame(notebook)

        notebook.add(self.resume_tab, text='Resume Rater')
        notebook.add(self.job_tab, text='Job Matcher')

        self.build_table(self.resume_tab, self.cleaned['resume'], is_job=False)
        self.build_table(self.job_tab, self.cleaned['job'], is_job=True)

    def cleanse_ratings(self, ratings):
        resume_ratings = []
        job_ratings = []

        for r in ratings:
            r_type = r.get('type')
            if r_type not in ['Resume Rater', 'Job Matcher']:
                continue

            raw_date = r.get('created_at', '')[:10]
            try:
                date_str = datetime.strptime(raw_date, '%Y-%m-%d').strftime('%b %d, %Y')
            except ValueError:
                date_str = raw_date

            entry = {
                'date': date_str,
                'score': r.get('rating', 'N/A'),
                'type': r_type,
                'feedback': r.get('feedback', '').strip(),
                'improvements': r.get('improvements', '').strip(),
                'resume': r.get('resume', '').strip(),
                'job_description': r.get('job_description', '').strip()
            }

            if r_type == 'Resume Rater':
                resume_ratings.append(entry)
            elif r_type == 'Job Matcher':
                job_ratings.append(entry)

        return {
            'resume': resume_ratings,
            'job': job_ratings
        }

    def build_table(self, parent, data, is_job=False):
        columns = ('date', 'score', 'feedback')
        tree = ttk.Treeview(parent, columns=columns, show='headings', height=10)

        tree.heading('date', text='Date Rated')
        tree.heading('score', text='Score')
        tree.heading('feedback', text='Summary Feedback')

        tree.column('date', width=120, anchor='center')
        tree.column('score', width=80, anchor='center')
        tree.column('feedback', width=520, anchor='w')

        scrollbar = ttk.Scrollbar(parent, orient='vertical', command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        for entry in data:
            short_feedback = entry['feedback'].replace('\n', ' ')
            short_feedback = (short_feedback[:120] + '...') if len(short_feedback) > 120 else short_feedback
            tree.insert('', tk.END, values=(entry['date'], entry['score'], short_feedback))

        tree.bind("<Double-1>", lambda event, entries=data: self.open_detail_popup(event, tree, entries))

    def open_detail_popup(self, event, tree, entries):
        selected = tree.selection()
        if not selected:
            return

        index = tree.index(selected[0])
        data = entries[index]

        popup = tk.Toplevel(self.master)
        popup.title(f"{data['type']} - Rating Details")
        popup.geometry("800x700")

        title = f"{data['type']} | Rated on {data['date']} | Score: {data['score']}"
        tk.Label(popup, text=title, font=('Helvetica', 12, 'bold')).pack(pady=10)

        fields = [
            ("Feedback", data['feedback']),
            ("Suggestions for Improvement", data['improvements']),
            ("Resume", data['resume']),
        ]

        if data['type'] == 'Job Matcher':
            fields.append(("Job Description", data['job_description']))

        for label, content in fields:
            if not content.strip():
                continue
            tk.Label(popup, text=label, font=('Helvetica', 10, 'bold')).pack(anchor='w', padx=10, pady=(10, 0))
            text_widget = tk.Text(popup, wrap=tk.WORD, height=8)
            text_widget.insert(tk.END, content)
            text_widget.config(state=tk.DISABLED)
            text_widget.pack(padx=10, pady=5, fill=tk.BOTH, expand=False)

def start_viewer(username, ratings):
    print("Starting Rating Viewer...")
    root = tk.Tk()
    ViewRatingsGUI(root, username, ratings)
    root.mainloop()
