import easygui
import pymupdf
import re
from datetime import datetime

#user selects pdf
file_path = easygui.fileopenbox(title="Select the Harley-Davidson PDF to Convert", filetypes=["*.pdf"])
file_name = file_path.split("\\")[-1]
whole_text = ""
if file_path:
    #open file and extract text from each page
    with pymupdf.open(file_path) as pdf:
        for page_number in range(pdf.page_count):
            page = pdf.load_page(page_number)
            page_text = page.get_text("text")
            whole_text += page_text

    #remove odd characters 
    whole_text = whole_text.replace("Standard", "$0")
    whole_text = whole_text.replace("Stardard", "$0")
    whole_text = whole_text.replace("™", "")
    whole_text = whole_text.replace("©", "")
    whole_text = whole_text.replace("®", "")

    #lines removed without RegEx
    lines_to_remove = ["Family","Model", "Model Name", "Model Code", "Spec",
        "Option Code Option Type", "Option Name", "MSRP", "Dealer Net",
        "2027 MODEL YEAR - MILITARY DOM", "2027 MODEL YEAR - MILITARY CAL",
        "CONFIDENTIAL PRICE LIST"]

    #lines removed with RegEx
    whole_text = re.sub(
        r"^(?:Anti-Lock Braking \(ABS\) standard|\d|updated \d\d?/\d\d?/\d\d\d\d|EFFECTIVE [a-zA-Z]{3}\s\d\d\d\d|Security System standard|RIder Safety Enhancements standard)(?:\n)",
        "",
        whole_text,
        flags=re.MULTILINE
    )

    #remove lines not in list
    whole_text = "\n".join(
        line.strip() for line in whole_text.splitlines()
        if line.strip() not in lines_to_remove
    )
    #Removes HEADER Family Names
    whole_text = re.sub(r"CVO\n(?=CVO\n)", "", whole_text)
    whole_text = re.sub(r"Touring\n(?=Touring\n|TOURING\n)", "", whole_text)
    whole_text = re.sub(r"Softail\n(?=Softail\n|SOFTAIL\n)", "", whole_text)
    whole_text = re.sub(r"Trike\n(?=Trike\n|TRIKE\n)", "", whole_text)
    whole_text = re.sub(r"Revolution Max\n(?=REVOLUTION MAX\n|Revolution Max\n|REVOLUTIONMAX\n)", "", whole_text)

    #use Freight to determine where each model ends (2 lines after Freight)
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

    #bring each model together by adding a line break after two money matches
    full_print = ""
    for each_list in list_items:
        print_text = " ".join(each_list)
        print_text = re.sub(r'(\$\d[\d,]*\s+\$\d[\d,]*)\s*', r'\1\n', print_text)
        full_print += print_text

    #save output to text file
    file_date =  f"./default_extraction_output/" + f"HD_Sanitized_{file_name}-" + datetime.now().strftime("%Y-%m-%d_%H-%M")
    with open(f"{file_date}.txt", "w") as file:
        file.write(full_print)

    print(f"File saved.")