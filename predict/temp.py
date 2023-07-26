from fastapi import FastAPI, HTTPException
import pickle
import numpy as np
from typing import List
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()

# Load the necessary data and models
unique_products = pickle.load(open('C:/Users/Raslen/Downloads/dta.pkl', 'rb'))
cosine_sim = pickle.load(open('C:/Users/Raslen/Downloads/food_model.pkl', 'rb'))
indices = pickle.load(open('C:/Users/Raslen/Downloads/indices.pkl', 'rb'))

def get_recommendations(title, cosine_sim=cosine_sim, indices=indices, unique_products=unique_products):
    if title not in indices:
        raise HTTPException(status_code=404, detail="Product not found")
    idx = indices[title]
    sim_scores = cosine_sim[idx]
    sim_indexes = np.argsort(sim_scores)[::-1][1:5]
    sim_product_names = unique_products[sim_indexes]
    return sim_product_names.tolist()

class RequestData(BaseModel):
    history: List[str]

@app.post("/")
def recommend_products(request_data: RequestData):
    history = request_data.history
    recommendations = []
    for product in history:
        try:
            recommended_items = get_recommendations(product)
            recommendations.extend(recommended_items)
        except HTTPException as e:
            response = JSONResponse(content={"error": e.detail}, status_code=e.status_code)
            return response

    return {"recommendations": recommendations}
