# prediction.py
import pickle
import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Load the trained model
model = pickle.load(open('_model.pkl', 'rb'))
scaler = pickle.load(open('scaler.pkl', 'rb'))
res = pickle.load(open('dta.pkl', 'rb'))

class PredictionInput(BaseModel):
    month_cons: float
    inventory: float
    product: str

class PredictionOutput(BaseModel):
    predicted_rec_qte: float

@app.post("/predict", response_model=PredictionOutput)
def predict(data: PredictionInput):
    try:
        month_cons = data.month_cons
        inventory = data.inventory
        product = data.product

        encoded_product = res.loc[res['product'] == product, 'encoded_product'].values[0]
        input_data = np.array([[month_cons, inventory, encoded_product]])

        scaled_input_data = scaler.transform(input_data)

        prediction = model.predict(scaled_input_data)
        predicted_rec_qte = prediction[0][0]

        return PredictionOutput(predicted_rec_qte=predicted_rec_qte)

    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid input data. Please provide valid month_cons, inventory, and product.")
