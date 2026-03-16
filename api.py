from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Annotated
import pickle
import pandas as pd

# load saved recommender objects
with open("recommender_model.pkl", "rb") as f:
    recommender_data = pickle.load(f)

df = recommender_data["df"]
cosine_sim = recommender_data["cosine_sim"]
indices = recommender_data["indices"]

app = FastAPI()


# request model
class RecommendationInput(BaseModel):
    product_name: Annotated[str, Field(..., description="Name of the selected product")]
    top_n: Annotated[int, Field(5, gt=0, le=20, description="Number of recommendations")]


@app.get("/")
def home():
    return {"message": "Amazon Product Recommender API is running"}


@app.get("/products")
def get_products():
    product_list = sorted(df["product_name"].dropna().unique().tolist())
    return {"products": product_list}

@app.get("/sample-products")
def sample_products():
    return df["product_name"].head(20).tolist()


@app.post("/recommend")
def recommend_products(data: RecommendationInput):
    product_name = data.product_name
    top_n = data.top_n

    if product_name not in indices:
        return {"recommendations": []}

    idx = indices[product_name]

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    sim_scores = sim_scores[1: top_n + 1]

    recommendations = []
    for i, score in sim_scores:
        recommendations.append({
            "product_name": df.iloc[i]["product_name"],
            "category": df.iloc[i]["category"],
            "rating": float(df.iloc[i]["rating"]),
            "discounted_price": float(df.iloc[i]["discounted_price"]),
            "img_link": df.iloc[i]["img_link"],
            "product_link": df.iloc[i]["product_link"],
            "similarity_score": float(score)
        })

    return {"recommendations": recommendations}