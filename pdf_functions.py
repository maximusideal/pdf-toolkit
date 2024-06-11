# See https://pypdf2.readthedocs.io/en/3.0.0/user/merging-pdfs.html
# import=
import PyPDF2
import os
import re


def ascii_to_int(text):
    """ Helper function: Converts numeric strings to integers, non-numeric remain unchanged. """
    return int(text) if text.isdigit() else text

def natural_keys(text):
    """ 
    Helper function: 
    - Splits a string into a list of integers and non-integer substrings. 
    - Used to create lists of ints and strings. 
    - The `key=` option in `.sort()` method then comapres the relevant lists in list-lexicographical order. 
    """
    return [ascii_to_int(c) for c in re.split(r'(\d+)', text)]


def add_bookmarks(pdf_path, outlinetext_path):
    """ Adds bookmarks to a PDF based on an outline text file. """
    with open(pdf_path, 'rb') as pdf_file, open(outlinetext_path, 'r') as outlinetext_file:

        # read pdf file in PyPDF2; write to new one in PyPDF2
        reader = PyPDF2.PdfReader(pdf_file)
        writer = PyPDF2.PdfWriter()

        # copy the pdf and add bookmarks
        for page in reader.pages:
            writer.add_page(page)

        # add bookmarks from the outline text file
        bookmarks = [None] * 100
        for line in outlinetext_file:
            # find first instance of " > ", " >> ", etc.; count how many >'s are present
            searcher = re.search(r"( >+ )", line)
            if not searcher:
                continue # skip lines that do not contain the separator
            separator = searcher.group(0)

            # gather relevant info
            num_depth = len(separator.strip())
            entries = line.strip().split(separator, maxsplit=1)

            page_number, outline_item_title = int(entries[0])-1, entries[1]
            parent = bookmarks[num_depth-1] if num_depth > 1 else None
            print(parent)

            # add new outline item
            new_bookmark = writer.add_outline_item(title=outline_item_title, page_number=page_number, parent=parent)
            bookmarks[num_depth] = new_bookmark

        # determine output path
        output_pdf_path = os.path.join(os.path.dirname(pdf_path), 'bookmarked_pdf.pdf')
        with open(output_pdf_path, 'wb') as output_pdf_file:
            writer.write(output_pdf_file)

    return output_pdf_path

def combine_pdfs(folder_path):
    """ Combines all PDF files in a folder into one, sorting them naturally. """
    # obtain list of pdfs
    pdf_filepaths = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.pdf')]
    pdf_filepaths.sort(key=natural_keys)  # sort files by integers in titles

    # merge; add titles as bookmarks
    merger = PyPDF2.PdfMerger()
    for pdf in pdf_filepaths:
        with open(pdf, "rb") as file:
            filename, _ = os.path.splitext(os.path.basename(file.name))
            merger.append(file, import_outline=False, outline_item=filename)  # add bookmarks based on filenames

    output_pdf_path = os.path.join(folder_path, 'merged_file.pdf')
    merger.write(output_pdf_path)
    merger.close()
    return output_pdf_path





