# See https://pypdf2.readthedocs.io/en/3.0.0/modules/PdfWriter.html#PyPDF2.PdfWriter.add_outline_item
# import
import tkinter as tk
from tkinter import filedialog
import PyPDF2
import os
import re
from pdf_functions import add_bookmarks, combine_pdfs

def browse_file(entry):
    """ Opens dialog box to select a file; updates the entry with the chosen path. """
    filepath = filedialog.askopenfilename()  # choose file path
    entry.delete(0, tk.END)  # remove current entry
    entry.insert(0, filepath)  # insert the chosen file path

def run(pdf_entry, outlinetext_entry, status_label):
    pdf_path = pdf_entry.get()
    outlinetext_path = outlinetext_entry.get()
    if pdf_path and outlinetext_path:
        output_pdf_path = add_bookmarks(pdf_path, outlinetext_path)
        status_label.config(text=f"Bookmarking successful! Output at {output_pdf_path}")
    else:
        status_label.config(text="Error.")

# set up the GUI
root = tk.Tk()
root.title("PDF Bookmark Adder")

# entry widgets
pdf_entry = tk.Entry(root, width=75)
pdf_entry.grid(row=0, column=1, padx=20, pady=10)
outlinetext_entry = tk.Entry(root, width=75)
outlinetext_entry.grid(row=1, column=1, padx=20, pady=10)

# buttons
pdf_button = tk.Button(root, text="Browse PDF", command=lambda: browse_file(pdf_entry))
pdf_button.grid(row=0, column=2, padx=10, pady=10)

outlinetext_button = tk.Button(root, text="Browse Text File", command=lambda: browse_file(outlinetext_entry))
outlinetext_button.grid(row=1, column=2, padx=10, pady=10)

status_label = tk.Label(root, text="")
status_label.grid(row=3, column=1, pady=10)

run_button = tk.Button(root, text="Add Bookmarks", command=lambda: run(pdf_entry, outlinetext_entry, status_label))
run_button.grid(row=2, column=1, pady=10)

root.mainloop()



