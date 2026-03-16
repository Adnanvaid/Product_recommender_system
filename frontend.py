import streamlit as st
import requests
import pandas as pd

# =========================
# Config
# =========================
st.set_page_config(
    page_title="Amazon Product Recommender",
    page_icon="🛍️",
    layout="wide"
)

FASTAPI_BASE_URL = "http://127.0.0.1:8000"

# =========================
# Helper Functions
# =========================
def fetch_products():
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/products", timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Unable to connect to FastAPI backend: {e}")
        return []

def fetch_recommendations(product_name, top_n):
    try:
        payload = {
            "product_name": product_name,
            "top_n": top_n
        }

        response = requests.post(
            f"{FASTAPI_BASE_URL}/recommend",
            json=payload,
            timeout=15
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching recommendations: {e}")
        return {}

# =========================
# UI
# =========================
st.title("🛍️ Amazon Product Recommender System")
st.write("Get product recommendations from your FastAPI backend.")

with st.sidebar:
    st.header("Settings")
    top_n = st.slider("Number of recommendations", min_value=1, max_value=20, value=5)

# Load products from backend
products_data = fetch_products()

if not products_data:
    st.warning("No products available from backend.")
    st.stop()

# FastAPI returns: {"products": [...]}
if isinstance(products_data, dict) and "products" in products_data:
    product_names = products_data["products"]

elif isinstance(products_data, list) and len(products_data) > 0:
    if isinstance(products_data[0], str):
        product_names = products_data
    elif isinstance(products_data[0], dict) and "product_name" in products_data[0]:
        product_names = [item["product_name"] for item in products_data]
    else:
        st.error("Unexpected response format from /products endpoint.")
        st.stop()

else:
    st.error("Unexpected response format from /products endpoint.")
    st.stop()

selected_product = st.selectbox("Select a product", sorted(product_names))

if st.button("Get Recommendations"):
    with st.spinner("Fetching recommendations..."):
        recommendations_data = fetch_recommendations(selected_product, top_n)

    recommendations = recommendations_data.get("recommendations", [])

    if not recommendations:
        st.info("No recommendations found.")
    else:
        st.subheader(f"Recommendations for: {selected_product}")

        for item in recommendations:
            with st.container():
                col1, col2 = st.columns([1, 4])

                with col1:
                    img_link = item.get("img_link", "")
                    if img_link:
                        st.image(img_link, width=120)
                    else:
                        st.write("No image")

                with col2:
                    st.markdown(f"### {item.get('product_name', 'N/A')}")
                    st.write(f"**Category:** {item.get('category', 'N/A')}")
                    st.write(f"**Rating:** {item.get('rating', 'N/A')}")
                    st.write(f"**Price:** {item.get('discounted_price', 'N/A')}")
                    if item.get("similarity_score") is not None:
                        st.write(f"**Similarity Score:** {item.get('similarity_score')}")
                    if item.get("product_link"):
                        st.markdown(f"[View Product]({item['product_link']})")

                st.markdown("---")

        st.subheader("Recommendation Table")
        st.dataframe(pd.DataFrame(recommendations), use_container_width=True)