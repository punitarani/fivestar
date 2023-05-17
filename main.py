"""FastAPI app entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fivestar.product_info import load_product_info
from fivestar.summary import summarize_product, summarize_reviews

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


@app.get("/summarize-product")
async def summarize_product_handler(product_id: str):
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
async def summarize_reviews_handler(product_id: str):
    """
    Summarize product reviews.
    :param product_id: Product ID to lookup.
    :return: Summary of product reviews.
    """
    reviews_summary = await summarize_reviews(product_id)
    return {
        "reviews": reviews_summary,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app")
