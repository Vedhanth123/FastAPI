import json
import os

def getData(filename):

    if not os.path.exists(filename):
        print(f"Erorr! the file {filename} doesn't exist")
        return None
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{filename}'. Check the file format.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def sendData(filename, data):

    if not os.path.exists(filename):
        print(f"Erorr! the file {filename} doesn't exist")
        return None
    try:
        with open(filename, 'w') as file:
            json.dump(data, file, indent=4)
            return True
    except json.JSONDecodeError:
        print(f"Error: Failed to decode JSON from '{filename}'. Check the file format.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


data = getData('test_backend_todolist.json')
print(data)