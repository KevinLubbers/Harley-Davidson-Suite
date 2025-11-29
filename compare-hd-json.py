import json
import easygui
from deepdiff import DeepDiff
import pandas

pandas.set_option('display.max_rows', None)


def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def compare_dicts(dict1, dict2):
    diff = DeepDiff(dict1, dict2)
    df = pandas.DataFrame(diff.get("values_changed", []))
    df = df.T
    df['new_num_value'] = pandas.to_numeric(df['new_value'], errors='coerce')
    df['old_num_value'] = pandas.to_numeric(df['old_value'], errors='coerce')
    df['difference'] = df.apply(lambda row: row['new_num_value'] - row['old_num_value'] if isinstance(row['new_num_value'], (int, float)) else "No Math", axis=1)
    df.drop(['new_num_value', 'old_num_value'], axis=1, inplace=True)
    print(df)
    

file_path_old = easygui.fileopenbox(title="Select the first JSON file", filetypes=["*.json"])
file_path_new = easygui.fileopenbox(title="Select the second JSON file", filetypes=["*.json"])

if file_path_old and file_path_new:
    old_dict = load_json(file_path_old)
    new_dict = load_json(file_path_new)

compare_dicts(old_dict, new_dict)

input("Press Enter to continue...")

