import tkinter as tk
from tkinter import messagebox
from services.gemini import gemini_match
from services.supabase_db import store_rating
from utils.pdf_utils import choose_pdf_file, get_pdf_preview
import os

class JobMatcherGUI:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        master.title("PyRater - Job Matcher")

        self.canvas = tk.Canvas(master, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        self.scrollable_frame = tk.Frame(self.canvas)
        self.scroll_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n", tags="frame")

        self.scrollable_frame.bind("<Configure>", self._on_frame_configure)
        self.canvas.bind("<Configure>", self._on_canvas_configure)

        self.inner_frame = tk.Frame(self.scrollable_frame)
        self.inner_frame.pack(anchor="center", pady=20)

        self.rating_var = tk.StringVar(value="X / 100")
        self.rating_label = tk.Label(self.inner_frame, textvariable=self.rating_var, font=("Arial", 24))
        self.rating_label.pack(pady=10)

        self.upload_frame = tk.Frame(self.inner_frame)
        self.upload_frame.pack(pady=5)

        self.upload_button = tk.Button(self.upload_frame, text="Upload Resume", command=self.upload_resume)
        self.upload_button.pack(side=tk.LEFT, padx=5)

        self.file_path_label = tk.Label(self.upload_frame, text="No resume selected")
        self.file_path_label.pack(side=tk.LEFT)

        self.preview_label = tk.Label(self.inner_frame, text="Resume Preview:")
        self.preview_label.pack()

        self.preview_text = tk.Text(self.inner_frame, height=12, width=100)
        self.preview_text.pack(pady=5)
        self.preview_text.config(state=tk.DISABLED)

        self.jd_frame = tk.Frame(self.inner_frame)
        self.jd_frame.pack(pady=5)

        self.jd_upload_button = tk.Button(self.jd_frame, text="Upload Job Description", command=self.upload_job_description)
        self.jd_upload_button.pack(side=tk.LEFT, padx=5)

        self.jd_file_path_label = tk.Label(self.jd_frame, text="No job description selected")
        self.jd_file_path_label.pack(side=tk.LEFT)

        self.jd_preview_label = tk.Label(self.inner_frame, text="Job Description Preview:")
        self.jd_preview_label.pack()

        self.jd_preview_text = tk.Text(self.inner_frame, height=12, width=100)
        self.jd_preview_text.pack(pady=5)
        self.jd_preview_text.config(state=tk.DISABLED)

        self.rate_button = tk.Button(self.inner_frame, text="Chance Me", command=self.chance_resume, state=tk.DISABLED)
        self.rate_button.pack(pady=10)

        self.feedback_label = tk.Label(self.inner_frame, text="Fit Feedback")
        self.feedback_label.pack()
        self.feedback_text = tk.Text(self.inner_frame, height=8, width=100)
        self.feedback_text.pack(pady=5)
        self.feedback_text.config(state=tk.DISABLED)

        self.improvement_label = tk.Label(self.inner_frame, text="Suggested Improvements")
        self.improvement_label.pack()
        self.improvement_text = tk.Text(self.inner_frame, height=8, width=100)
        self.improvement_text.pack(pady=5)
        self.improvement_text.config(state=tk.DISABLED)

        self.resume_file_path = None
        self.job_description_path = None

    def _on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.scroll_window, width=canvas_width)

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def upload_resume(self):
        filepath = choose_pdf_file()
        if filepath:
            self.resume_file_path = filepath
            self.file_path_label.config(text=os.path.basename(filepath))
            self.display_preview(filepath, self.preview_text)
            self.check_both_files_uploaded()

    def upload_job_description(self):
        filepath = choose_pdf_file()
        if filepath:
            self.job_description_path = filepath
            self.jd_file_path_label.config(text=os.path.basename(filepath))
            self.display_preview(filepath, self.jd_preview_text)
            self.check_both_files_uploaded()

    def display_preview(self, filepath, text_widget):
        try:
            preview_text = get_pdf_preview(filepath)
        except Exception as e:
            preview_text = f"Error displaying preview: {e}"
        text_widget.config(state=tk.NORMAL)
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, preview_text)
        text_widget.config(state=tk.DISABLED)

    def check_both_files_uploaded(self):
        if self.resume_file_path and self.job_description_path:
            self.rate_button.config(state=tk.NORMAL)

    def chance_resume(self):
        if not self.resume_file_path or not self.job_description_path:
            messagebox.showerror("Error", "Please upload both resume and job description.")
            return

        feedback_arr = gemini_match(self.resume_file_path, self.job_description_path)

        rating = feedback_arr[0]
        feedback = feedback_arr[1]
        improvements = feedback_arr[2]

        self.rating_var.set(f"{rating} / 100")

        self.feedback_text.config(state=tk.NORMAL)
        self.feedback_text.delete("1.0", tk.END)
        self.feedback_text.insert(tk.END, feedback)
        self.feedback_text.config(state=tk.DISABLED)

        self.improvement_text.config(state=tk.NORMAL)
        self.improvement_text.delete("1.0", tk.END)
        self.improvement_text.insert(tk.END, improvements)
        self.improvement_text.config(state=tk.DISABLED)

        resume_text = self.preview_text.get("1.0", tk.END)
        jd_preview_text = self.jd_preview_text.get("1.0", tk.END)

        store_rating(rating, feedback, improvements, resume_text, self.username.lower(), "Job Matcher", jd_preview_text)

def start_matcher(username):
    print("Starting Job Matcher...")
    root = tk.Tk()
    root.geometry("1000x800")
    JobMatcherGUI(root, username)
    root.mainloop()
