"""fivestar.product_info.py"""

import json
import os

import httpx

AMAZON_PRODUCT_BASE_URL = "https://www.amazon.com/dp/"


async def get_amazon_product_info(product_id: str) -> dict:
    """
    Get Product Information from Amazon.
    :param product_id: Product ID to lookup.
    :return: Product information.
    """
    url = "https://amazon23.p.rapidapi.com/product-details"
    querystring = {"asin": product_id, "country": "US"}

    headers = {
        "X-RapidAPI-Key": os.getenv("RAPID_API_KEY"),
        "X-RapidAPI-Host": "amazon23.p.rapidapi.com"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, params=querystring)
        data = json.loads(response.content).get("result")[0]

        return {
            "title": data.get("title", product_id),
            "description": data.get("description", ""),
            "features": data.get("feature_bullets", []),
        }
    except Exception as error:
        error_msg = f"Unable to get product info for {product_id}"
        print(error_msg)
        raise ValueError(error_msg) from error
