#!/bin/bash

echo "Starting FastAPI server..."
python -m uvicorn api:app --host 0.0.0.0 --port 8000 &

echo "Starting Streamlit frontend..."
python -m streamlit run frontend.py --server.port 8501 --server.address 0.0.0.0