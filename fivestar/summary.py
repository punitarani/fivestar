"""fivestar.summary.py"""

import json

from langchain.chains import ConversationalRetrievalChain
from langchain.chains.summarize import load_summarize_chain
from langchain.chat_models import ChatOpenAI
from langchain.docstore.document import Document
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.memory import ConversationBufferMemory

from fivestar.product_info import load_product_info, load_product_reviews
from fivestar.store import vectorstore

llm = ChatOpenAI(model_name="gpt-4")
embeddings = OpenAIEmbeddings()
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


async def summarize_reviews(product_id: str) -> str:
    """
    Summarize product reviews.
    :param product_id: Product ID to lookup.
    :return: Summary of product reviews.
    """

    await load_product_reviews(product_id)

    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever(), memory=memory)

    query = """
    Please provide a comprehensive summary of the product associated with the provided ID. 
    What are its main features? What are the positive and negative aspects of this product as expressed in customer reviews? 
    What is the overall sentiment of the reviews? 
    How does it compare to other similar products in the market? 
    What improvements or changes do customers commonly suggest for this product? 
    Finally, based on these reviews, would you say the product is worth buying?
    """
    result = qa({"question": query})
    return result["answer"]
