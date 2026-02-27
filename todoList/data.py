import json
import os


'''
def getData(filename):

    if not os.path.exists(filename):
        print(f"Erorr! the file {filename} doesn't exist")
        raise Exception
    try:
        with open(filename, 'r') as file:
            data = json.load(file)
            return data
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise Exception
'''
def getData(filename):
    with open(filename, 'r') as file:
        data = json.load(file)
        return data
    


# def sendData(filename, data):

#     if not os.path.exists(filename):
#         print(f"Erorr! the file {filename} doesn't exist")
#         raise Exception
#     try:
#         with open(filename, 'w') as file:
#             json.dump(data, file, indent=4)
#             return True
#     except Exception as e:
#         raise Exception

def sendData(filename, data):

    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)
        return True
