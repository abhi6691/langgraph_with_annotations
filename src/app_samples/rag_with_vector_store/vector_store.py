import logging
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

def setup_vector_store(chunks):
    if not chunks:
        raise ValueError("No chunks available for embedding. Please check document loading.")
    
    logging.debug(f"Total chunks loaded: {len(chunks)}")

    embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_documents(chunks, embedding_model)
    return db.as_retriever()