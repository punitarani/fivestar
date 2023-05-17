"""app.py"""

import asyncio

import streamlit as st

from fivestar.product_info import load_product_info
from fivestar.summary import summarize_product, summarize_reviews
from utils import format_amazon_product_url


async def app():
    """
    Streamlit app.
    """
    st.title("FiveStar")

    # Get Amazon URL input for a product
    product_url = st.text_input("Enter Amazon Product URL")
    if not product_url:
        st.stop()

    # Validate and format the URL
    try:
        product_url = format_amazon_product_url(product_url)
    except ValueError:
        st.error("Invalid URL format. URL should contain '/dp/' path segment.")
        st.stop()

    # Get the product id
    product_id = product_url.split("/dp/")[1].split("/")[0]

    # Load product information
    try:
        with st.spinner("Loading product information..."):
            product_info = await load_product_info(product_id)
        with st.spinner("Analyzing product information..."):
            product_summary = await summarize_product(product_id)
        st.subheader(product_info.get("title", "Product Information"))
        st.write(product_summary)
    except Exception as error:
        st.error(f"Unable to load product information for {product_id}. {error}")

    # Load product reviews
    try:
        with st.spinner("Analyzing product reviews..."):
            product_reviews = await summarize_reviews(product_id)
        st.subheader("Product Reviews")
        st.write(product_reviews)
    except Exception as error:
        st.error(f"Unable to load product reviews for {product_id}. {error}")


if __name__ == "__main__":
    asyncio.run(app())
