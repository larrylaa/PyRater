import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import os
from pdfminer.high_level import extract_text
from docx import Document as DocxDocument

class ResumeReviewerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Resume Reviewer")

        self.rating_var = tk.StringVar(value="X / 10")
        self.rating_label = tk.Label(master, textvariable=self.rating_var, font=("Arial", 24))
        self.rating_label.pack(pady=10)

        self.upload_frame = tk.Frame(master)
        self.upload_frame.pack(pady=10)

        self.upload_button = tk.Button(self.upload_frame, text="Upload Resume", command=self.upload_file)
        self.upload_button.pack(side=tk.LEFT, padx=5)

        self.file_path_label = tk.Label(self.upload_frame, text="No file selected")
        self.file_path_label.pack(side=tk.LEFT)

        self.preview_label = tk.Label(master, text="Resume Preview:")
        self.preview_label.pack()

        self.preview_text = tk.Text(master, height=15, width=60)
        self.preview_text.pack(pady=10)
        self.preview_text.config(state=tk.DISABLED)

        self.rate_button = tk.Button(master, text="Rate Resume", command=self.rate_resume, state=tk.DISABLED)
        self.rate_button.pack(pady=10)

        self.feedback_label = tk.Label(master, text="Resume Feedback:")
        self.feedback_label.pack()

        self.feedback_text = tk.Text(master, height=10, width=60)
        self.feedback_text.pack(pady=10)
        self.feedback_text.config(state=tk.DISABLED)

        self.resume_file_path = None

    def upload_file(self):
        filetypes = (
            ('PDF files', '*.pdf'),
            ('Word files', '*.docx *.doc'),
            ('Text files', '*.txt'),
            ('All files', '*.*')
        )
        filepath = filedialog.askopenfilename(
            title='Open a file',
            initialdir=os.path.expanduser("~"),
            filetypes=filetypes)

        if filepath:
            self.resume_file_path = filepath
            self.file_path_label.config(text=os.path.basename(filepath))
            self.display_resume_preview(filepath)
            self.rate_button.config(state=tk.NORMAL)

        # TODO: UPLOAD TO LOCAL DIRECTORY

    def display_resume_preview(self, filepath):
        preview_text = ""
        try:
            if filepath.lower().endswith(".pdf"):
                preview_text = self.extract_text_from_pdf(filepath)
            elif filepath.lower().endswith((".docx", ".doc")):
                preview_text = self.extract_text_from_word(filepath)
            elif filepath.lower().endswith(".txt"):
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    preview_text = f.read(500) 
            else:
                preview_text = "Unsupported file format for preview."
        except Exception as e:
            preview_text = f"Error displaying preview: {e}"

        self.preview_text.config(state=tk.NORMAL)
        self.preview_text.delete("1.0", tk.END)
        self.preview_text.insert(tk.END, preview_text)
        self.preview_text.config(state=tk.DISABLED)

    def extract_text_from_pdf(self, pdf_path):
        try:
            text = extract_text(pdf_path, maxpages=1) 
            return text
        except Exception as e:
            return f"Error extracting text from PDF: {e}"

    def extract_text_from_word(self, docx_path):
        try:
            doc = DocxDocument(docx_path)
            full_text = []
            for para in doc.paragraphs:
                full_text.append(para.text)
            return '\n'.join(full_text)
        except Exception as e:
            return f"Error extracting text from Word document: {e}"

    def rate_resume(self):
        if self.resume_file_path:
            # TODO: ADD GEMINI RATING LOGIC
            feedback = ""
            rating = 1

            self.rating_var.set(f"{rating}/10")
            self.feedback_text.config(state=tk.NORMAL)
            self.feedback_text.delete("1.0", tk.END)
            self.feedback_text.insert(tk.END, feedback)
            self.feedback_text.config(state=tk.DISABLED)
        else:
            messagebox.showerror("Error", "Please upload a resume file first.")

if __name__ == "__main__":
    root = tk.Tk()
    gui = ResumeReviewerGUI(root)
    root.mainloop()