import easygui
import pymupdf
import re
import datetime

file_path = easygui.fileopenbox(title="Select the Harley-Davidson PDF to Convert", filetypes=["*.pdf"])
file_name = file_path.split("/")[-1]
today = datetime.date.today().strftime("%m-%d-%Y")
whole_text = ""
if file_path:
    with pymupdf.open(file_path) as pdf:
    # Loop through each page
        for page_number in range(pdf.page_count):
            page = pdf.load_page(page_number)
            page_text = page.get_text("text")
            whole_text += page_text

    # Print the extracted text
    whole_text = whole_text.replace("Standard", "$0")
    whole_text = whole_text.replace("Stardard", "$0")
    whole_text = whole_text.replace("™", "")
    whole_text = whole_text.replace("©", "")
    whole_text = whole_text.replace("®", "")

    lines_to_remove = ["Family","Model", "Model Name", "Model Code", "Spec",
        "Option Code Option Type", "Option Name", "MSRP", "Dealer Net",
        "Trike", "Softail", "Revolution Max", "Touring"]

    whole_text = re.sub(
        r"^(?:Anti-Lock Braking \(ABS\) standard|\d|Security System standard|RIder Safety Enhancements standard)(?:\n)",
        "",
        whole_text,
        flags=re.MULTILINE
    )
    whole_text = "\n".join(
        line for line in whole_text.splitlines()
        if line not in lines_to_remove
    )

    lines = whole_text.splitlines()

    list_items = []
    current_item = []

    i = 0
    while i < len(lines):
        current_item.append(lines[i])

        if lines[i].strip() == "Freight":
            # Include the two lines following Freight
            current_item.extend(lines[i + 1:i + 3])

            list_items.append(current_item)
            current_item = []
            i += 3
        else:
            i += 1

    # Keep any leftover lines, if there are any
    if current_item:
        list_items.append(current_item)

    for each_list in list_items:
        print(" ".join(each_list))
        print("\n")