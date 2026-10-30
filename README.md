# Convert PDF to Text
- run the command 
```python convert-pdf-to-text.py```
to extract the text of the selected Harley-Davidson price list
# Convert Text to JSON
1. run the command
```python convert-text-to-json.py```
to convert your semi-structured text into JSON
2. built-in validation will flag any suspicious row that will require manual intervention
3. JSON file saving is not available if validation fails - rerun after fixing text data
# Enter JSON Data into PCS
1. Open PCS Maintenance
2. Manually select the necessary effective date for this run
3. Make sure your keyboard cursor (not mouse) has the Model Code field selected
4. run the command
```python input-json-to-pcs.py```
5. Follow all on-screen instructions and prompts

# Manually Sanitize, PDF -> Text [DEPRECATED]
These steps have been automated but they will remain archived here.  
1. Open new Harley-Davidson Price List, select all(Ctrl + A) text, and copy(Ctrl + C)
2. Paste Price List contents into a text file
3. Remove all odd characters (copyright, trademark, registered trademark)
4. Replace "Standard" with "$0"
5. Remove Header text lines and standard equipment lines (starts with "Family" or no $ present in line?)
6. Save your sanitized file