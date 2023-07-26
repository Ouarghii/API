import requests

url = "http://localhost:8001/predict"  # Update the port number to 8001

data = {
    "month_cons": 10.217,
    "inventory": 3.863,
    "product": "Chicken Fajitas"
}

response = requests.post(url, json=data)

if response.status_code == 200:
    result = response.json()
    predicted_rec_qte = int(result['predicted_rec_qte'])  # Corrected variable name

    print("Predicted rec_qte:", predicted_rec_qte)
else:
    print("Error:", response.json())
