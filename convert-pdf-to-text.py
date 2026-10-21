import easygui
import pymupdf

file_path = easygui.fileopenbox(title="Select the Harley-Davidson PDF to Convert", filetypes=["*.pdf"])
whole_text = ""
if file_path:
    with pymupdf.open(file_path) as pdf:
    # Loop through each page
        for page_number in range(pdf.page_count):
            page = pdf.load_page(page_number)
            
            # Extract text from the page
            page_text = page.get_text("text")
            whole_text += page_text

    # Print the extracted text
    print(whole_text)