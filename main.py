from fastapi import FastAPI, Path
import json
import uvicorn

app = FastAPI(debug=True)  # Enable debug mode in FastAPI


def load_data():
    try:
        with open('test.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"error": "Data file not found."}
    except json.JSONDecodeError:
        return {"error": "Error decoding JSON data."}

@app.get('/')
def read_root():
    return {"message": "Hello, World!"}

@app.get('/about')
def read_about():
    return {"message": "This is a simple FastAPI application."}

@app.get('/items')
def read_items():
    return load_data()

@app.get('/item/{item_id}')
def read_item(item_id: str):
    data = load_data()
    if item_id in data:
        return {item_id: data[item_id]} 
    else:
        return {"error": "Item not found."}

# Add this at the end to run the app in debug mode
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        debug=True,      # Enable debug mode
        reload=True      # Auto-reload on file changes
    )
