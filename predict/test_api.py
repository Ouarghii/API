import requests

# Define the URL of your FastAPI server
url = "http://127.0.0.1:8001/"

# Define the data you want to send in the request body
data = {
    "history": ["1% Milk", "1% Milk", "2% Milk"]
}

# Define the headers with Content-Type set to "application/json"


# Send the POST request to the server
response = requests.post(url, json=data)

# Check the request and response
print("Request Body:", response.request.body)
print("Status Code:", response.status_code)
print("Response JSON:", response.json())
