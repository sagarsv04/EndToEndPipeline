import requests
import json

# URL of the Flask API
url = 'http://localhost:5001/predict'

# Example payload with features
payload = [
    {
        "user_age": 30,
        "user_income": 500000,
        "user_clicks": 10,
        "income_click_ratio": 5000
    },
    {
        "user_age": 40,
        "user_income": 60000,
        "user_clicks": 50,
        "income_click_ratio": 4000
    }
]

# Send POST request to the Flask API
response = requests.post(url, json=payload)

# Print the prediction results
if response.status_code == 200:
    print("Predictions:", response.json())
else:
    print(f"Failed to get predictions. Status code: {response.status_code}, Error: {response.text}")
