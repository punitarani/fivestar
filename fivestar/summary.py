"""fivestar.summary.py"""

import json

from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document

from fivestar.product_info import load_product_info

llm = ChatOpenAI(model_name="gpt-4")
summarize_chain = load_summarize_chain(llm, chain_type="map_reduce")


async def summarize_product(product_id: str) -> str:
    """
    Summarize product reviews.
    :param product_id: Product ID to lookup.
    :return: Summary of product reviews.
    """
    product_info = await load_product_info(product_id)

    docs = [
        Document(page_content=(json.dumps(product_info.get(key, ""))))
        for key in ["title", "description", "features"]
    ]

    summary = summarize_chain.run(docs)
    return summary
