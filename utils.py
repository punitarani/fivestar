"""utils.py"""

from urllib.parse import urlparse


def format_amazon_product_url(url):
    """
    Format the Amazon product URL to exclude irrelevant query string
    :param url: Amazon product URL
    :return: Formatted Amazon product URL
    """
    parsed_url = urlparse(url)
    path = parsed_url.path

    if "/dp/" not in path:
        raise ValueError("Invalid URL format. URL should contain '/dp/' path segment.")

    product_id = path.split("/dp/")[1]
    formatted_url = f"https://www.amazon.com/dp/{product_id}"
    return formatted_url
