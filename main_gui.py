
# import
import tkinter as tk
from tkinter import ttk, filedialog
from pdf_functions import add_bookmarks, combine_pdfs


# functions
def browse_dir(entry, need_folder=False):
    """ Opens dialog box to select a file or folder; updates the entry with the chosen path. """
    if need_folder: dir = filedialog.askdirectory()
    else: dir = filedialog.askopenfilename()

    entry.delete(0, tk.END)  # remove current entry
    entry.insert(0, dir)  # insert the chosen file path

def run_add_bookmarks(pdf_entry, outlinetext_entry, status_label):
    pdf_path = pdf_entry.get()
    outlinetext_path = outlinetext_entry.get()
    if pdf_path and outlinetext_path:
        try:
            output_pdf_path = add_bookmarks(pdf_path, outlinetext_path)
            status_label.config(text=f"Bookmarking successful! Output at {output_pdf_path}")
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")
    else:
        status_label.config(text="Please select both PDF and outline text files.")

def run_combine_pdfs(folder_entry, status_label):
    folder_path = folder_entry.get()
    if folder_path:
        try:
            output_pdf_path = combine_pdfs(folder_path)
            status_label.config(text=f"PDFs combined successfully! Output at {output_pdf_path}")
        except Exception as e:
            status_label.config(text=f"Error: {str(e)}")
    else:
        status_label.config(text="Please select a folder.")


#===== MAIN WINDOW =====#
# set up the GUI
root = tk.Tk()
root.title("PDF Toolkit")

notebook = ttk.Notebook(root)
notebook.pack(pady=10, expand=True)


#===== TAB 1: Add Bookmarks =====#
tab1 = ttk.Frame(notebook)
notebook.add(tab1, text='Add Bookmarks')

# entry widgets
pdf_entry = tk.Entry(tab1, width=75)
pdf_entry.grid(row=0, column=1, padx=20, pady=10)
outlinetext_entry = tk.Entry(tab1, width=75)
outlinetext_entry.grid(row=1, column=1, padx=20, pady=10)

# buttons
pdf_button = tk.Button(tab1, text="Find PDF", command=lambda: browse_dir(pdf_entry))
pdf_button.grid(row=0, column=2, padx=10, pady=10)

outlinetext_button = tk.Button(tab1, text="Find Text File", command=lambda: browse_dir(outlinetext_entry))
outlinetext_button.grid(row=1, column=2, padx=10, pady=10)

run_button = tk.Button(tab1, text="Add Bookmarks", command=lambda: run_add_bookmarks(pdf_entry, outlinetext_entry, status_label))
run_button.grid(row=2, column=1, pady=10)


#===== TAB 2: Combine PDFs =====#
tab2 = ttk.Frame(notebook)
notebook.add(tab2, text='Combine PDFs')

# entry widgets
folder_entry = tk.Entry(tab2, width=75)
folder_entry.grid(row=0, column=1, padx=20, pady=10)

# buttons
folder_button = tk.Button(tab2, text="Browse Folder", command=lambda: browse_dir(folder_entry, need_folder=True))
folder_button.grid(row=0, column=2, padx=10, pady=10)

combine_button = tk.Button(tab2, text="Combine PDFs", command=lambda: run_combine_pdfs(folder_entry, status_label))
combine_button.grid(row=1, column=1, pady=10)


#===== ALL TABS =====#
# status label for all tabs
status_label = tk.Label(root, text="")
status_label.pack(pady=10)

root.mainloop()



