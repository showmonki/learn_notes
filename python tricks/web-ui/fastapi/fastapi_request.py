import requests

test_data = {
        "data": [
            {"name": "Alice", "age": 25, "city": "New York"},
            {"name": "Bob", "age": 30, "city": "San Francisco"},
            {"name": "Charlie", "age": 28, "city": "Los Angeles"}
        ]
    }
response = requests.post("http://localhost:8000/process_json/", json=test_data)

print(response.json())