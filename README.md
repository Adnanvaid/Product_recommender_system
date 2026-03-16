# Amazon Product Recommendation System
Project Overview

This project implements a machine learning–based product recommendation system that suggests similar products based on user input.
The system uses an Amazon product dataset containing product metadata, ratings, and sales-related attributes to generate meaningful recommendations.

The application is built using a microservice architecture where the machine learning model is served through an API and accessed through an interactive web interface.

# Tech Stack

Python
1. Machine Learning (Similarity-based recommendation)
2. FastAPI – Backend API
3. Streamlit – Frontend interface
4. Docker – Containerization
5. Pandas, NumPy, Scikit-learn

# Features

1. Product similarity based recommendation
2. Real-time API-based prediction
3. Interactive user interface
4. Containerized deployment using Docker
5. scalable architecture separating frontend and backend

# How to Run the Project
1. Install Dependencies-- pip install -r requirements.txt
2. Run FastAPI Backend-- uvicorn api:app --reload
3. Run Streamlit Frontend-- streamlit run frontend.py

# Running with Docker
1. Build Docker Image-- docker build -t amazon-product-recommender .
2. Run Container-- docker run -p 8000:8000 -p 8501:8501 adnan78630/amazon_product_recommender
