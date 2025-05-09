import os
from tkinter import filedialog
from pdfminer.high_level import extract_text

def choose_pdf_file():
    filetypes = (('PDF files', '*.pdf'),)
    filepath = filedialog.askopenfilename(
        title='Open a file',
        initialdir=os.path.expanduser("~"),
        filetypes=filetypes
    )
    return filepath

def extract_text_from_pdf(pdf_path):
    try:
        return extract_text(pdf_path, maxpages=1)
    except Exception as e:
        return f"Error extracting text from PDF: {e}"

def get_pdf_preview(filepath):
    if filepath.lower().endswith(".pdf"):
        return extract_text_from_pdf(filepath)
    else:
        return "Please upload a PDF file."
