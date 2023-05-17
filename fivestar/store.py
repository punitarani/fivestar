"""fivestar.store.py"""

from langchain.docstore.document import Document
from langchain.vectorstores import Chroma

vectorstore = Chroma.from_documents([Document(page_content=".")])
