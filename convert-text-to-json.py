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
    #last character has changed between MY26 and 27
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

    #invoice and msrp validation check
    msrp = findMSRP(text)
    invoice = findInvoice(text)
    if float(invoice) > float(msrp):
        validation_errors.append(f"Bad invoice price on line {debug_line_count}")

    #trim code validation
    trim = findTrim(text)
    if trim and trim not in trim_code_set:
        validation_errors.append(f"Unknown trim code {trim} on line {debug_line_count}")

    option_split = re.split(" ", text)
    if not trim:
        if len(option_split) <= 3:
            option = "DFRT"
            option_name = "Manufacturer Destination Charge"
            option_type = "Freight"
            loop_option = {"option": f"{option}", "type": f"{option_type}", "name": f"{option_name}", "msrp": f"{msrp}", "invoice": f"{invoice}"}
            option_array.append(loop_option)
            #invoice and msrp should be the same for DFRT
            if float(invoice) != float(msrp):
                validation_errors.append(f"Bad DFRT price on line {debug_line_count}")
        else:
            option = option_split[0]
            option_name = " ".join(option_split[2:-2])
            option_type = option_split[1]
            loop_option = {"option": f"{option}", "type": f"{option_type}", "name": f"{option_name}", "msrp": f"{msrp}", "invoice": f"{invoice}"}
            option_array.append(loop_option)
            if len(option) > 3:
                validation_errors.append(f"Bad option code found on line {debug_line_count}")
            if option_type not in option_type_set:
                validation_errors.append(f"Bad option type found on line {debug_line_count}")
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
        if trim_name not in trim_name_set:
            validation_errors.append(f"Unknown trim name {trim_name} on line {debug_line_count}")
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
    
    easygui.msgbox(
        msg="Please select the sanitized HD Order Guide in txt format",
        title="Order Guide Extractor"
    )

    file_path = easygui.fileopenbox(title="Select a TXT file", default=os.path.join(os.getcwd(), "*.txt"))

    if file_path:
        print(f"Selected file: {file_path}")
    else:
        print("No file selected.")
        os.system("pause")

    #Holds all converted data
    loop_list = []
    data = {}
    options = []

    #used in validation
    debug_line_count = 1
    validation_errors = []

    family_set = {"REVOLUTIONMAX", "TOURING", "TRIKE", "SOFTAIL", "CVO"}

    model_codes_seen = set()
    model_code_duplicates = set()

    trim_code_set = {"G00", "G01", "G06"}
    trim_name_set = {"Chrome Trim", "Black Trim", "Solo Trim",
    "Solo Chrome Trim", "Solo Black Trim", "Chrome 2 up Trim", "Black 2 up Trim"}

    option_type_set = {"Color", "Trim", "Base Trim", "Trim-Color", "Wheel", "Suspension"}
    #end validation variables

    with open(file_path) as file:
        lines = file.readlines()
        for line in lines:
            line = line.strip()
            check = isHeader(line)

            #if check is true, the line is a header
            if check:
                #since it's a header and there's data already (not first cycle), add data then clear data
                if data:
                    data["options"] = options
                    loop_list.append(data)
                    data = {}
                    options = []

                #start header validation
                #family check
                family_name = findFamily(line)
                if family_name.upper() not in family_set:
                    validation_errors.append(f"Unknown family {family_name} on line {debug_line_count}")

                #use 2 sets to find duplicate model codes
                model_code = findModel(line)
                if model_code in model_codes_seen:
                    model_code_duplicates.add(model_code)
                    validation_errors.append(f"Duplicate model code {model_code} on line {debug_line_count}")
                else:
                    model_codes_seen.add(model_code)

                #invoice and msrp checks
                header_msrp = findMSRP(line)
                header_invoice = findInvoice(line)
                if header_msrp == "0" or header_invoice == "0":
                    validation_errors.append(f"$0 price record found on HEADER line {debug_line_count}")
                if float(header_invoice) >= float(header_msrp):
                    validation_errors.append(f"Bad invoice price on line {debug_line_count}")

                #color check
                color_code, color_name = findColor(line)

                #trim check
                head_trim = findTrim(line)
                trim_name = findHeadTrimName(line)
                if head_trim not in trim_code_set:
                    validation_errors.append(f"Unknown trim code {head_trim} on line {debug_line_count}")
                if trim_name not in trim_name_set:
                    validation_errors.append(f"Unknown trim name {trim_name} on line {debug_line_count}")
                #end header validation

                #start adding header data   
                data = {
                    "family": family_name,
                    "model": model_code,
                    "name": findModelName(line),
                    }
                options.append({"option": "*MDL",
                        "type": "Price",
                        "name": "Base Price",
                        "msrp": header_msrp,
                        "invoice": header_invoice})
                options.append({"option": f"{color_code}",
                        "type": "Color",
                        "name": f"{color_name}",
                        "msrp": "0",
                        "invoice": "0"})
                if head_trim:
                    options.append({"option": f"{head_trim}",
                        "type": "Base Trim",
                        "name": f"{trim_name}",
                        "msrp": "0",
                        "invoice": "0"})
            #if line is not a header, it must be an option!    
            else:
                options.extend(findLoopOption(line))

            
            debug_line_count += 1
        #end each line loop
                
    #print validation errors
    if len(validation_errors) > 0:
        print("Cannot save file.")
        print("Validation Errors:")
        for error in validation_errors:
            print(error)
    #or save file to where user chooses
    else:
        data["options"] = options
        loop_list.append(data)
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