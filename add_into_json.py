# Python program to update
# JSON

import json
 
n1 = input("1")
n2 = input("2")
n3 = input("3")

# function to add to JSON
def write_json(new_data, filename='dataset/intents.json'):
    with open(filename,'r+') as file:
          # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["intents"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)
 
    # python object to be appended
y = {"tag":n1,
     "patterns": [n2],
     "responses": [n3]
    }
     
write_json(y)