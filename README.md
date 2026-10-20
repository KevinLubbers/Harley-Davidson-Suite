# Manually Sanitize, PDF -> Text
Planning to automate this with a script soon. 
1. Open new Harley-Davidson Price List, select all(Ctrl + A) text, and copy(Ctrl + C)
2. Paste Price List contents into a text file
3. Remove all odd characters (copyright, trademark, registered trademark)
4. Replace "Standard" with "$0"
5. Remove Header text lines and standard equipment lines (starts with "Family" or no $ present in line?)
6. Save your sanitized file

# Convert Text to JSON
1. run the command
```python convert-text-to-json.py```
2. Report any schema issues to PCS at run-time


# Enter Data into PCS
1. Open PCS Maintenance
2. Select the necessary effective date for this run
3. Make sure your cursor (not mouse) has the Model Code field selected
4. run the command
```python input-json-to-pcs.py```

