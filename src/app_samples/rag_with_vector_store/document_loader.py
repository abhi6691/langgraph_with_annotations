from langchain.text_splitter import CharacterTextSplitter
from langchain.docstore.document import Document
from app_samples.rag_with_vector_store.scraper import scrape_bedrock_api_docs

def load_and_split_document():
    text = scrape_bedrock_api_docs()
    splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    
    # Split the text and log chunk details
    chunks = splitter.split_text(text)
    
    # Wrap each chunk in a Document and log its size
    document_chunks = []
    for i, chunk in enumerate(chunks):
        document_chunks.append(Document(page_content=chunk))
    
    return document_chunks