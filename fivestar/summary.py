"""fivestar.summary.py"""

import json

from langchain import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from tenacity import retry, stop_after_attempt

from fivestar.product_info import load_product_info, load_product_reviews
from fivestar.store import vectorstore
from . import DATA_DIR

llm_3 = OpenAI(model_name="text-davinci-003")
llm_3_5 = ChatOpenAI(model_name="gpt-3.5-turbo")
llm_4 = ChatOpenAI(model_name="gpt-4")

buffers = {}
qa_chains = {}


async def summarize_product(product_id: str) -> str:
    """
    Summarize product reviews.
    :param product_id: Product ID to lookup.
    :return: Summary of product reviews.
    """
    await load_product_info(product_id)

    query = """
    Please provide a comprehensive summary of the product. 
    What are its main features and benefits? 
    Provide a brief overview of the product's specifications. 
    Provide an unbiased summary of the product based on the information provided. 
    Describe the product as if you were explaining it to a friend but without opinion or bias. 
    It should be written in complete sentences and formatted as if you were writing for a company's website.
    The response should be no more than 3-4 sentences.
    """

    try:
        with open(DATA_DIR.joinpath("summaries", "info", f"{product_id}.txt"), "r") as f:
            summary = f.read()
            memory = _get_conv_mem_buf(product_id)
            memory.save_context({"question": query}, {"answer": summary})
            return summary
    except FileNotFoundError:
        pass

    qa = _get_qa_chain(product_id)

    result = qa({"question": query})
    summary = result["answer"]

    with open(DATA_DIR.joinpath("summaries", "info", f"{product_id}.txt"), "w") as f:
        f.write(summary)

    return summary


async def summarize_reviews(product_id: str) -> str:
    """
    Summarize product reviews.
    :param product_id: Product ID to lookup.
    :return: Summary of product reviews.
    """
    await load_product_reviews(product_id)

    query = """
    Please provide a comprehensive summary of the product reviews. 
    What are its main features? 
    What are the positive and negative aspects of this product as expressed in customer reviews? 
    What is the overall sentiment of the reviews? 
    How does it compare to other similar products in the market? 
    What improvements or changes do customers commonly suggest for this product? 
    Finally, based on these reviews, would you say the product is worth buying? 
    Provide all this information in a concise yet comprehensive summary only based on the reviews provided.
    It should be written in complete sentences and formatted as if you were writing for a company's website.
    The response should be no more than 3-4 sentences.
    """

    try:
        with open(DATA_DIR.joinpath("summaries", "reviews", f"{product_id}.txt"), "r") as f:
            summary = f.read()
            memory = _get_conv_mem_buf(product_id)
            memory.save_context({"question": query}, {"answer": summary})
            return summary
    except FileNotFoundError:
        pass

    qa = _get_qa_chain(product_id)

    result = qa({"question": query})
    summary = result["answer"]

    with open(DATA_DIR.joinpath("summaries", "reviews", f"{product_id}.txt"), "w") as f:
        f.write(summary)

    return summary


@retry(stop=stop_after_attempt(3))
async def get_pros_cons(product_id: str) -> dict:
    """
    Get pros and cons of product.
    :param product_id: Product ID to lookup.
    :return: Pros and cons of product.
    """

    await load_product_reviews(product_id)

    query = """
    Please provide a comprehensive list of up to 5 pros and cons each for the product. 
    What are the positive and negative aspects of this product as expressed in customer reviews? 
    Provide all this information in a concise yet comprehensive list only based on the reviews provided.
    You need to respond to this question in JSON format with the following structure:
    {"pros": ["pro1", "pro2", ...], "cons": ["con1", "con2", ...]}
    Do not include any data other than the JSON object in your response.
    """

    await load_product_info(product_id)
    await load_product_reviews(product_id)

    try:
        with open(DATA_DIR.joinpath("summaries", "pros-cons", f"{product_id}.json"), "r") as f:
            pros_cons = json.load(f)
            memory = _get_conv_mem_buf(product_id)
            memory.save_context({"question": query}, {"answer": json.dumps(pros_cons)})
            return pros_cons
    except FileNotFoundError:
        pass

    qa = _get_qa_chain(product_id)

    result = qa({"question": query})
    pros_cons = result["answer"]
    print(f"Pros and cons for {product_id}: {pros_cons}")
    pros_cons = json.loads(pros_cons)

    with open(DATA_DIR.joinpath("summaries", "pros-cons", f"{product_id}.json"), "w") as f:
        json.dump(pros_cons, f)

    return pros_cons


async def chat_with_reviews(product_id: str, query: str) -> str:
    """
    Chat with product reviews.
    :param product_id: Product ID to lookup.
    :param query: Query to ask.
    :return: Response to query.
    """
    await load_product_reviews(product_id)

    qa = _get_qa_chain(product_id)

    # Add following moderation to prevent irrelevant questions
    query += """
    \n\nAnswer the question(s) based on the product reviews provided only.
    The replies should be relevant to the product reviews provided and concise with relevant information.
    \n\n
    Only answer questions related to the product. 
    If the question is not related to the product, please respond with the following verbatim: 
    I'm sorry, I don't know the answer to that question.
    """

    result = qa({"question": query})
    return result["answer"]


def _get_conv_mem_buf(product_id: str) -> ConversationBufferMemory:
    """
    Get conversation memory buffer.
    :param product_id: Product ID to lookup.
    :return: Conversation memory buffer.
    """
    if product_id not in buffers:
        buffers[product_id] = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return buffers[product_id]


def _get_qa_chain(product_id, llm=llm_3_5):
    """
    Get QA chain.
    :param product_id: Product ID to lookup.
    :return: QA chain.
    """
    if product_id not in qa_chains:
        memory = _get_conv_mem_buf(product_id)
        qa_chains[product_id] = ConversationalRetrievalChain.from_llm(llm, vectorstore.as_retriever(), memory=memory)
    return qa_chains[product_id]
