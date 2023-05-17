"""FastAPI app entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fivestar.product_info import load_product_info
from fivestar.summary import summarize_product, summarize_reviews, get_pros_cons, chat_with_reviews

app = FastAPI()

# Add CORS middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/info")
async def product_info_handler(product_id: str) -> dict:
    """
    Get product information.
    :param product_id: Product ID to lookup.
    :return: Product information.
    """
    product_info = await load_product_info(product_id)
    return product_info


@app.get("/summarize-product")
async def summarize_product_handler(product_id: str) -> dict:
    """
    Summarize product reviews.
    :param product_id: Product ID to lookup.
    :return: Summary of product information.
    """
    product_info = await load_product_info(product_id)
    product_summary = await summarize_product(product_id)

    return {
        "info": product_info,
        "summary": product_summary,
    }


@app.get("/summarize-reviews")
async def summarize_reviews_handler(product_id: str) -> dict:
    """
    Summarize product reviews.
    :param product_id: Product ID to lookup.
    :return: Summary of product reviews.
    """
    reviews_summary = await summarize_reviews(product_id)
    return {
        "reviews": reviews_summary,
    }


@app.get("/pros-cons")
async def get_pros_cons_handler(product_id: str) -> dict:
    """
    Get pros and cons of product.
    :param product_id: Product ID to lookup.
    :return: Pros and cons of product.
    """
    pros_cons = await get_pros_cons(product_id)
    return pros_cons


@app.get("/chat")
async def chat_with_reviews_handler(product_id: str, query: str) -> dict:
    """
    Chat with product reviews.
    :param product_id: Product ID to lookup.
    :param query: Query to ask.
    :return: Response to query.
    """
    response = await chat_with_reviews(product_id, query)
    return {
        "response": response,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app")
