import easygui
import os
import re
import json
from datetime import datetime

def isHeader(text):
    head_split = re.split(" ", text)
    pattern = r"\d"
    matches = re.findall(pattern, head_split[0])
    if matches or len(head_split) < 4:
        return False
    else:
        return True
        
def findFamily(text):
    split = re.split(" ", text)
    family = split[0]
    return family
    
def findModel(text):
    split = re.split(" ", text)
    model = split[1]
    return model

def findModelName(text):
    #first split based on unique Model Code String
    #second split is to remove Family and Model strings, leaving Model Name (multi word names works)
    pattern = r"1....\*V"
    model_name = re.split(pattern, text)
    model_name = re.split(" ", model_name[0])
    model_name = model_name[2:]
    model_name = " ".join(model_name).strip()
    return model_name

def findInvoice(text):
    #find money pattern and remove ,'s
    pattern = r"(?<=\$)(0|(\d{1,3},)?\d{3})"
    matches = re.findall(pattern, text)
    invoice = [match[0].replace(",", "") for match in matches]
    #extra check for when there is only 1 match (because of Standard / $0)
    if len(invoice) > 1:
        invoice = invoice[1]
    else:
        invoice = invoice[0]
    return invoice
    
def findMSRP(text):
    #find money pattern and remove ,'s
    pattern = r"(?<=\$)(0|(\d{1,3},)?\d{3})"
    matches = re.findall(pattern, text)
    msrp = [match[0].replace(",", "") for match in matches]
    msrp = msrp[0]
    return msrp
    
def findTrim(text):
    pattern = r"(?<=\w\d\d\s-\s)G0\d"
    matches = re.findall(pattern, text)
    if not matches:
        return False
    else:
        return matches[0]

def findTrimName(text):
    pattern = r"(?:Vivid Black - |Roasted Amber Fade - |Sapphire Storm - |Phantom Eclipse - |Emerald Storm - |Denim Black - |Black Denim - )(\w+\s\d\s\w+|\w+\s\w+|\w+)"
    matches = re.findall(pattern, text)
    if not matches:
        return False
    else:
        name = matches[0] + " Trim"
        return name

def findHeadTrimName(text):
    pattern = r"(?:Vivid Black - |Roasted Amber Fade - |Sapphire Storm - |Phantom Eclipse - |Emerald Storm - |Denim Black - |Black Denim - )(\w+\s\d\s\w+|\w+\s\w+|\w+)"
    matches = re.findall(pattern, text)
    if not matches:
        return False
    else:
        name = matches[0] + " Trim"
        return name

def findColor(text):
    pattern = r"(\w\d\d)(?=\s-\sG0\d)"
    code_matches = re.findall(pattern, text)
    pattern = r"(?<=Trim )(\w+\s\w+\s\w+|\w+\s\w+|\w+)"
    name_matches = re.findall(pattern, text)
    return code_matches[0], name_matches[0]
    
def findLoopOption(text):
    option_array = []
    msrp = findMSRP(text)
    invoice = findInvoice(text)
    trim = findTrim(text)
    option_split = re.split(" ", text)
    if not trim:
        if len(option_split) <= 3:
            option = "DFRT"
            option_name = "Manufacturer Destination Charge"
            option_type = "Freight"
            loop_option = {"option": f"{option}", "type": f"{option_type}", "name": f"{option_name}", "msrp": f"{msrp}", "invoice": f"{invoice}"}
            option_array.append(loop_option)
        else:
            option = option_split[0]
            option_name = " ".join(option_split[2:-2])
            option_type = option_split[1]
            loop_option = {"option": f"{option}", "type": f"{option_type}", "name": f"{option_name}", "msrp": f"{msrp}", "invoice": f"{invoice}"}
            option_array.append(loop_option)
    else:
        option = re.split("-", option_split[0])
        #carry over from old code I believe, should never happen
        if len(option) < 2:
            option = re.split("-", option_split[1])
            if len(option) > 1:
                option = option[1]
                option_name = " ".join(option_split[3:-2])
                option_type = option_split[2]
            else:
                option = option_split[0]
                option_name = " ".join(option_split[2:-2])
                option_type = option_split[1]
        #end code that never runs
                
        else:
            option = option[1]
            option_name = " ".join(option_split[2:-2])
            option_type = option_split[1]
            
        trim_name = findTrimName(text)
        color_code, color_name = findColor(line)
        if trim_name:
            trim_option = {"option": f"{trim}", "type": "Trim", "name": f"{trim_name}", "msrp": "0", "invoice": "0"}
            loop_option = {"option": f"{color_code}", "type": "Color", "name": f"{color_name}", "msrp": "0", "invoice": "0"}
            diff_MDL = {"option": "*MDL", "type": "Differential", "name": "Base Price", "msrp": f"{msrp}", "invoice": f"{invoice}"}            
            option_array.append(diff_MDL)
        else:
            trim_option = {"option": f"{trim}", "type": "Trim", "name": f"{trim_name}", "msrp": f"{msrp}", "invoice": f"{invoice}"}
            loop_option = {"option": f"{option}", "type": f"{option_type}", "name": "Vivid Black (CHECK)", "msrp": "0", "invoice": "0"}
        option_array.append(trim_option)
        option_array.append(loop_option)
        

    
    return option_array

try:
    
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    easygui.msgbox(
        msg="Please select the sanitized HD Order Guide in txt format",
        title="Order Guide Extractor"
    )

    file_path = easygui.fileopenbox(title="Select a TXT file", default=os.path.join(desktop, "*.txt"))

    if file_path:
        print(f"Selected file: {file_path}")
    else:
        print("No file selected.")
        os.system("pause")

    loop_list = []
    data = {}
    options = []
    
    with open(file_path) as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            check = isHeader(line)
            
            if check:
                if data:
                    data["options"] = options
                    loop_list.append(data)
                    #print(data)
                    data = {}
                    options = []
                    
                data = {
                    "family": findFamily(line),
                    "model": findModel(line),
                    "name": findModelName(line),
                    }
                options.append({"option": "*MDL",
                        "type": "Price",
                        "name": "Base Price",
                        "msrp": findMSRP(line),
                        "invoice": findInvoice(line)})
                color_code, color_name = findColor(line)
                options.append({"option": f"{color_code}",
                        "type": "Color",
                        "name": f"{color_name}",
                        "msrp": "0",
                        "invoice": "0"})
                head_trim = findTrim(line)
                
                if head_trim:
                    trim_name = findHeadTrimName(line)
                    options.append({"option": f"{head_trim}",
                        "type": "Base Trim",
                        "name": f"{trim_name}",
                        "msrp": "0",
                        "invoice": "0"})
                
            else:
                options.extend(findLoopOption(line))
                
    

    data["options"] = options
    loop_list.append(data)
    #print(data)
    #print(loop_list)
    '''old save function
    print("Saving list as JSON file")
    current_date_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    file_name = f"HD_JSON_{current_date_time}.json"
    
    with open(file_name, "w") as file:
        json.dump(loop_list, file, indent=4)
    print("Save Complete!")
    '''
    #new save function
    file_date =  "./default_extraction_output/" + "HD-comparison-" + datetime.now().strftime("%Y-%m-%d_%H-%M")
    save_file_path = easygui.filesavebox(
        default=f"{file_date}",
        filetypes=["*.json"],
        title="Choose where to save the extracted Order Guide")

    if save_file_path is None:
        print("No file selected. Exiting.")
        exit()
    if not save_file_path.endswith('.json'):
        save_file_path += '.json'
        
    with open(save_file_path, "w") as outfile:
        json.dump(loop_list, outfile, indent=2)
        print(f"JSON dumped to {save_file_path}")

except Exception as e:
    print(f"An error occurred: {e}")
            
            
os.system("pause") 