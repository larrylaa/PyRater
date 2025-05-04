import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from pdfminer.high_level import extract_text
from gemini import gemini_rate
from supabase_db import store_rating, check_if_user_exists, fetch_user_ratings
import os
class ResumeReviewerGUI:
    def __init__(self, master):
        self.master = master
        master.title("Resume Rater")

        self.rating_var = tk.StringVar(value="X / 100")
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

        self.feedback_label = tk.Label(master, text="Resume Feedback")
        self.feedback_label.pack()
        self.feedback_text = tk.Text(master, height=10, width=60)
        self.feedback_text.pack(pady=10)
        self.feedback_text.config(state=tk.DISABLED)

        self.improvement_label = tk.Label(master, text="Suggested Improvements")
        self.improvement_label.pack()
        self.improvement_text = tk.Text(master, height=10, width=60)
        self.improvement_text.pack(pady=10)
        self.improvement_text.config(state=tk.DISABLED)

        self.resume_file_path = None

    def upload_file(self):
        filetypes = (
            ('PDF files', '*.pdf'),
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

    def display_resume_preview(self, filepath):
        preview_text = ""
        try:
            if filepath.lower().endswith(".pdf"):
                preview_text = self.extract_text_from_pdf(filepath)
            else:
                preview_text = "Please upload a PDF file."
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

    def rate_resume(self):
        if self.resume_file_path:
            print(username)
            feedback_arr = gemini_rate(self.resume_file_path)

            rating = feedback_arr[0] 
            feedback = feedback_arr[1]
            improvements = feedback_arr[2]
            resume_text = self.preview_text.get("1.0", tk.END) 

            # set ratings
            self.rating_var.set(f"{rating} / 100")

            # set feedback
            self.feedback_text.config(state=tk.NORMAL)
            self.feedback_text.delete("1.0", tk.END)
            self.feedback_text.insert(tk.END, feedback)
            self.feedback_text.config(state=tk.DISABLED)

            # set improvements
            self.improvement_text.config(state=tk.NORMAL)
            self.improvement_text.delete("1.0", tk.END)
            self.improvement_text.insert(tk.END, improvements)
            self.improvement_text.config(state=tk.DISABLED)

            store_rating(rating, feedback, improvements, resume_text, username.lower())

        else:
            messagebox.showerror("Error", "Please upload a resume file first.")

def start_app():
    print("Starting app...")
    root = tk.Tk()
    gui = ResumeReviewerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    username = str(input("Enter your username: "))
    if check_if_user_exists(username.lower()):
        print(f"Hi {username}, welcome back to PyRater!")

        print("Select a menu option below.")
        print("1. Start App")
        print("2. See Ratings")
        print("3. Exit")
        option = int(input("Enter an option: "))

        if option == 1:
            start_app()
        elif option == 2:
            # TODO: clean this input and print it out to console or display it using tkinker nicely. (assigned to: elijah)
            print(fetch_user_ratings(username.lower()))
        elif option == 3:
            exit()
        else:
            print("Invalid option entered, please re-run the app and try again.")
            exit()
    else:
        print(f'Hi {username}, welcome to PyRater!')
        start_app()

