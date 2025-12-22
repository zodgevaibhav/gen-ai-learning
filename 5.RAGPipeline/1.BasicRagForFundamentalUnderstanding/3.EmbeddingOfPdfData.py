from langchain_ollama import ChatOllama
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, PyPDFDirectoryLoader
from langchain_ollama import OllamaEmbeddings

def creating_embedding(readPdf):
    embeddings = OllamaEmbeddings(model = "llama3")
    embedded_data = embeddings.embed_documents(readPdf)
    return embedded_data

def load_pdf(file_path="../VaibhavZodge.pdf"):
    """Load a PDF file and return its content."""
    # https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.pdf.PyPDFLoader.html
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    return documents



readPdf = str(load_pdf())
print(creating_embedding(readPdf));
