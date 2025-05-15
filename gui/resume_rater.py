import tkinter as tk
from tkinter import messagebox
from services.gemini import gemini_rate
from services.supabase_db import store_rating
from utils.pdf_utils import choose_pdf_file, get_pdf_preview
import os

class ResumeRaterGUI:
    def __init__(self, master, username):
        self.master = master
        self.username = username
        master.title("PyRater - Resume Rater")

        # Canvas for scrollable area
        self.canvas = tk.Canvas(master, highlightthickness=0)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Bind mousewheel
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Scrollable frame container
        self.scrollable_frame = tk.Frame(self.canvas)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="n")

        # Resize callback to center content
        self.canvas.bind("<Configure>", self._center_content)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        # Actual centered content frame
        self.content_frame = tk.Frame(self.scrollable_frame)
        self.content_frame.pack(anchor="n")

        # ======= GUI WIDGETS START HERE ======= #
        self.rating_var = tk.StringVar(value="X / 100")
        self.rating_label = tk.Label(self.content_frame, textvariable=self.rating_var, font=("Arial", 24))
        self.rating_label.pack(pady=10)

        self.upload_frame = tk.Frame(self.content_frame)
        self.upload_frame.pack(pady=10)

        self.upload_button = tk.Button(self.upload_frame, text="Upload Resume", command=self.upload_file)
        self.upload_button.pack(side=tk.LEFT, padx=5)

        self.file_path_label = tk.Label(self.upload_frame, text="No file selected")
        self.file_path_label.pack(side=tk.LEFT)

        self.preview_label = tk.Label(self.content_frame, text="Resume Preview:")
        self.preview_label.pack()

        preview_frame = tk.Frame(self.content_frame)
        preview_frame.pack(pady=10)

        self.preview_text = tk.Text(preview_frame, height=15, width=100, wrap=tk.WORD)
        scroll_preview = tk.Scrollbar(preview_frame, command=self.preview_text.yview)
        self.preview_text.configure(yscrollcommand=scroll_preview.set)

        self.preview_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_preview.pack(side=tk.RIGHT, fill=tk.Y)

        self.preview_text.config(state=tk.DISABLED)

        self.rate_button = tk.Button(self.content_frame, text="Rate Resume", command=self.rate_resume, state=tk.DISABLED)
        self.rate_button.pack(pady=10)

        self.feedback_label = tk.Label(self.content_frame, text="Resume Feedback")
        self.feedback_label.pack()
        
        feedback_frame = tk.Frame(self.content_frame)
        feedback_frame.pack(pady=10)

        self.feedback_text = tk.Text(feedback_frame, height=10, width=100, wrap=tk.WORD)
        scroll_feedback = tk.Scrollbar(feedback_frame, command=self.feedback_text.yview)
        self.feedback_text.configure(yscrollcommand=scroll_feedback.set)

        self.feedback_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_feedback.pack(side=tk.RIGHT, fill=tk.Y)

        self.feedback_text.config(state=tk.DISABLED)

        self.improvement_label = tk.Label(self.content_frame, text="Suggested Improvements")
        self.improvement_label.pack()
        
        improvement_frame = tk.Frame(self.content_frame)
        improvement_frame.pack(pady=10)

        self.improvement_text = tk.Text(improvement_frame, height=10, width=100, wrap=tk.WORD)
        scroll_improvement = tk.Scrollbar(improvement_frame, command=self.improvement_text.yview)
        self.improvement_text.configure(yscrollcommand=scroll_improvement.set)

        self.improvement_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_improvement.pack(side=tk.RIGHT, fill=tk.Y)

        self.improvement_text.config(state=tk.DISABLED)

        self.resume_file_path = None

    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _center_content(self, event):
        canvas_width = event.width
        content_width = self.content_frame.winfo_reqwidth()
        x_offset = max((canvas_width - content_width) // 2, 0)
        self.canvas.coords(self.canvas_window, x_offset, 0)

    def upload_file(self):
        filepath = choose_pdf_file()
        if filepath:
            self.resume_file_path = filepath
            self.file_path_label.config(text=os.path.basename(filepath))
            self.display_resume_preview(filepath)
            self.rate_button.config(state=tk.NORMAL)

    def display_resume_preview(self, filepath):
        preview_text = ""
        try:
            preview_text = get_pdf_preview(filepath)
        except Exception as e:
            preview_text = f"Error displaying preview: {e}"

        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert(tk.END, preview_text)
        self.preview_text.config(state=tk.DISABLED)
        
    def rate_resume(self):
        if self.resume_file_path:
            feedback_arr = gemini_rate(self.resume_file_path)

            rating = feedback_arr[0]
            feedback = feedback_arr[1]
            improvements = feedback_arr[2]
            resume_text = self.preview_text.get("1.0", tk.END)

            self.rating_var.set(f"{rating} / 100")

            self.feedback_text.config(state=tk.NORMAL)
            self.feedback_text.delete("1.0", tk.END)
            self.feedback_text.insert(tk.END, feedback)
            self.feedback_text.config(state=tk.DISABLED)

            self.improvement_text.config(state=tk.NORMAL)
            self.improvement_text.delete("1.0", tk.END)
            self.improvement_text.insert(tk.END, improvements)
            self.improvement_text.config(state=tk.DISABLED)

            store_rating(rating, feedback, improvements, resume_text, self.username.lower(), "Resume Rater", "N/A")
        else:
            messagebox.showerror("Error", "Please upload a resume file first.")

def start_rater(username):
    print("Starting Resume Rater...")
    root = tk.Tk()
    root.geometry("1000x800")
    ResumeRaterGUI(root, username)
    root.mainloop()
