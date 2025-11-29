import easygui
import os
import json
import sys
import pyautogui, time, pygetwindow
import pyperclip
import logging

#logging setup
logger = logging.getLogger()

# Set the log level (e.g., INFO level for general logs)
logger.setLevel(logging.INFO)

# Create a file handler that logs to 'input_check_log.txt'
file_handler = logging.FileHandler('pcs_input_log.txt', mode='a')
file_handler.setLevel(logging.INFO)  # Set the file handler's log level

# Create a stream handler to log to the console (stdout)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Set the console handler's log level

# Define the log format
formatter = logging.Formatter('%(asctime)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
#end logging setup

def navToCalOr49S(response_check):
    if response_check:
        #nav to 49S model
        pyautogui.press('down')
        pyautogui.press('down')
    else:
        #nav to CAL model
        pyautogui.press('down')

    #navigate to options
    time.sleep(.5)
    pyautogui.press('alt')
    pyautogui.press('s')
    time.sleep(1)
    pyautogui.press('o')
    time.sleep(.5)
    
    time.sleep(2)
    
    
def navCheckPrice():
    pyautogui.press('alt')
    pyautogui.press('s')
    time.sleep(1)
    pyautogui.press('i')
    time.sleep(.5)
    
    time.sleep(1)

def deleteOption():
    pyautogui.press('alt')
    pyautogui.press('p')
    time.sleep(1)
    pyautogui.press('d')
    time.sleep(.5)
    pyautogui.press('enter')
    
    time.sleep(1)
    
def findOptionCategory(json_category):
    case_dict = {
        "Color": "EXT",
        "Trim": "DECOR",
        "Base Trim": "DECOR",
        "Trim-Color": "EXT",
        "Wheel": "WHEEL",
        "Suspension": "SUSP"
    }
    converted_category = case_dict.get(json_category)
    return converted_category

def addBadOption(code, name, option_type, invoice, msrp):
    pyautogui.press('alt')
    pyautogui.press('p')
    time.sleep(1)
    pyautogui.press('a')
    time.sleep(1)
    pyautogui.write(code, interval=0.1)
    pyautogui.press('tab')
    pyautogui.write(name, interval=0.1)
    pyautogui.press('tab')
    pyautogui.write(option_type, interval=0.1)
    pyautogui.press('tab')
    pyautogui.write("MFG", interval=0.1)
    pyautogui.press('enter')
    time.sleep(.5)
    pyautogui.hotkey('alt', 'c')
    time.sleep(1)
    
    #add price record to new option
    pyautogui.press('alt')
    pyautogui.press('s')
    time.sleep(1)
    pyautogui.press('i')
    time.sleep(1)
    pyautogui.press('tab')
    pyautogui.write(invoice, interval=0.1)
    time.sleep(.5)
    pyautogui.press('tab')
    pyautogui.write(msrp, interval=0.1)
    pyautogui.press('enter')
    time.sleep(.5)

def addOption(invoice, msrp, differential=False):
    pyautogui.press('alt')
    pyautogui.press('p')
    time.sleep(1)
    pyautogui.press('a')
    time.sleep(.5)
    pyautogui.press('tab')
    time.sleep(.5)
    pyautogui.write(invoice, interval=0.1)
    time.sleep(.5)
    pyautogui.press('tab')
    pyautogui.write(msrp, interval=0.1)
    if differential == True:
        pyautogui.press('tab')
        pyautogui.press('down')
        pyautogui.press('down')
    pyautogui.press('enter')
    time.sleep(.5)
    
def addPaintsToColorChart(colors):
    #navigate to option description field, cant use option field because use of different option codes
    pyautogui.press('backspace')
    pyautogui.press('tab')
    time.sleep(.5)
    pyautogui.write("EXT", interval=0.1)
    pyautogui.press('f5')
    time.sleep(.5)
    pyautogui.press('alt')
    pyautogui.press('s')
    time.sleep(.5)
    pyautogui.press('g')
    
    #inside color group window - adding colors
    time.sleep(1)
    pyautogui.press('alt')
    pyautogui.press('p')
    time.sleep(1)
    pyautogui.press('a')
    time.sleep(2)
    for color in colors:
        pyautogui.write(color, interval=0.1)
        time.sleep(.5)
        pyautogui.press('enter')
        time.sleep(.5)
        pyautogui.press('enter')
        time.sleep(.5)
    time.sleep(.5)
    pyautogui.hotkey('alt', 'c')
    #pyautogui.press('alt')
    #pyautogui.press('c')
    time.sleep(.5)
    exitScreen()
    time.sleep(.5)
    #delete EXT text to show all options again
    pyautogui.press('backspace')
    pyautogui.press('f5')
    
def exitScreen():
    pyautogui.hotkey('alt', 'f')
    time.sleep(.5)
    pyautogui.press('c')
    time.sleep(.5)


try:
    #MSG Box to select JSON file
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    easygui.msgbox(
        msg="Please select a JSON File that you want to enter into PCS",
        title="HD Data Input"
    )

    file_path = easygui.fileopenbox(title="Select a JSON file", default=os.path.join(desktop, "*.json"))

    if file_path:
        print(f"Selected file: {file_path}")
    else:
        print("No file selected.")
        os.system("pause")
    
    #useless message to remind user to open PCS
    response = easygui.ynbox("Script will fail if PCS is not Open\nIs PCS Maintenance Open?", title="Confirmation", choices=["Yes", "No"])
    
    if not response:
        sys.exit("PCS not opened. Please Try Again")
    
    #useful message with choice which effects navigation
    cal_response = easygui.ynbox("Did you select a 49 State file or California file?", title="49S or CAL?", choices=["49 State", "California"])
    
    #Bring PCS Window to foreground and maximize
    pcs_window = pygetwindow.getWindowsWithTitle('PCS Maintenance')
    pcs_window[0].activate()
    pcs_window[0].maximize()
    
    
    #load in JSON file then loop through models
    with open(file_path, "r") as file:
        data = json.load(file)
    time.sleep(2)    
    for each_model in data:
        #type model code then year then refresh
        pyautogui.write(each_model["model"], interval=0.1)
        pyautogui.press('tab')
        pyautogui.press('tab')
        #change YEAR here
        pyautogui.write("2026", interval=0.1)
        pyautogui.press('f5')
        time.sleep(.5)
        
        #tab over to model grid
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        pyautogui.press('tab')
        time.sleep(.5)
        
        #using choice from earlier
        navToCalOr49S(cal_response)
        
        #used in loop to collect options based on certain conditions
        bad_options = []
        good_options = []
        bad_price = []
        good_price = []
        paint_list = []
        display_list = []
        #loop through options for current model
        for each_option in each_model["options"]:
            display_text = each_option["option"] + " - " + each_option["name"]
            display_list.append(display_text)
            if each_option["type"] == "Color" or each_option["type"] == "Trim-Color":
                paint_list.append(each_option["option"])
            #write option code then check if it exists in PCS
            #add to bad options if doesnt exist
            pyautogui.write(each_option["option"], interval=0.1)
            pyautogui.press('f5')
            time.sleep(1)
            pyautogui.press('tab')
            pyautogui.press('tab')
            pyautogui.press('tab')
            pyautogui.press('tab')
            pyautogui.press('tab')
            pyautogui.press('tab')
            pyautogui.press('tab')
            pyautogui.press('down')
            pyautogui.press('right')
            time.sleep(.5)
            pyautogui.hotkey('ctrl', 'c')
            time.sleep(1)
            copy_check = pyperclip.paste().strip()
            if not copy_check == each_option["option"]:
                bad_options.append(each_option)
                option_cat = findOptionCategory(each_option["type"])
                addBadOption(each_option["option"], each_option["name"], option_cat, each_option["invoice"], each_option["msrp"])
            else:
                good_options.append(each_option)
                navCheckPrice()
                #nav to invoice then copy
                pyautogui.press('right')
                pyautogui.press('right')
                pyautogui.press('right')
                pyautogui.press('right')
                pyautogui.hotkey('ctrl', 'c')
                time.sleep(1)
                invoice_check = pyperclip.paste().strip()
                if not float(invoice_check) == float(each_option["invoice"]):
                    #check if another *MDL option(we don't want to delete base price)
                    if not each_option["type"] == "Differential":
                        #add to bad price list and delete record
                        bad_price.append(each_option)
                        deleteOption()
                        addOption(each_option["invoice"], each_option["msrp"])
                    else:
                        addOption(each_option["invoice"], each_option["msrp"], True)
                else:
                    #nav to msrp then copy
                    pyautogui.press('right')
                    pyautogui.hotkey('ctrl', 'c')
                    time.sleep(1)
                    msrp_check = pyperclip.paste().strip()
                    if not float(msrp_check) == float(each_option["msrp"]):
                        #add to bad price list and delete record
                        bad_price.append(each_option)
                        deleteOption()
                        addOption(each_option["invoice"], each_option["msrp"])
                    else:
                        good_price.append(each_option)
                
                #back out of pricing screen with good price present in PCS
                time.sleep(1)
                exitScreen()
            
            #return navigation to Option Field
            pyautogui.hotkey('shift', 'tab')
            pyautogui.hotkey('shift', 'tab')
            pyautogui.hotkey('shift', 'tab')
            pyautogui.hotkey('shift', 'tab')
            pyautogui.hotkey('shift', 'tab')
            pyautogui.hotkey('shift', 'tab')
            pyautogui.hotkey('shift', 'tab')
        
        
        #options loop end - allow user to clean up old codes
        addPaintsToColorChart(paint_list)
        display_list = "\n".join(display_list)
        easygui.msgbox(
            msg="New Options:\n" + display_list,
            title="Delete Old Options"
        )
        
        #Log Info then back out to model screen
        logger.info(f"Model: {each_model["model"]} - {each_model["name"]}")
        logger.info(f"Bad Options: {bad_options}")
        logger.info(f"Good Options with Bad Prices: {bad_price}")
        logger.info(f"Good Options with Good Prices: {good_price}")
        exitScreen()
        
        #return to model code input box(undo initial tabs)
        pyautogui.hotkey('shift', 'tab')
        pyautogui.hotkey('shift', 'tab')
        pyautogui.hotkey('shift', 'tab')
        pyautogui.hotkey('shift', 'tab')
        pyautogui.hotkey('shift', 'tab')
        pyautogui.hotkey('shift', 'tab')
        time.sleep(.5)
        
        
        
        #remove after testing
        #print(each_model)

    
except Exception as e:
    print(f"An error occurred: {e}")
            
            
os.system("pause") 