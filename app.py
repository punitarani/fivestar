"""app.py"""

from time import sleep

import streamlit as st

from utils import format_amazon_product_url


def app():
    """Streamlit App"""
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

    # TODO: Implement the rest of the app
    with st.spinner("Loading product reviews..."):
        sleep(2)
    st.write(f"Product Reviews for {product_url}")


if __name__ == "__main__":
    app()
