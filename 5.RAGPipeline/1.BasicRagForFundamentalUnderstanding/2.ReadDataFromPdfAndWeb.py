from langchain_ollama import ChatOllama
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, PyPDFDirectoryLoader
from langchain_core.documents import Document


def load_pdf(file_path="../VaibhavZodge.pdf"):
    """Load a PDF file and return its content."""
    # https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.pdf.PyPDFLoader.html
    loader = PyPDFLoader(file_path)
    documents = loader.load() # It returns a list of Document objects, each containing the text content of the PDF page.
    return documents

def load_pdf_return_documents(file_path="../VaibhavZodge.pdf"):
    """Load a PDF file and return its content."""
    # https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.pdf.PyPDFLoader.html
    loader = PyPDFLoader(file_path)
    documents = loader.load() # It returns a list of Document objects, each containing the text content of the PDF page.
    docs = []
    id=1
    for document in documents:
        docs.append(Document(id=id, page_content=document.page_content))
        id=id+1
    return docs

def load_from_web(url="https://github.com/zodgevaibhav"):
    # https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.web_base.WebBaseLoader.html
    loader = WebBaseLoader(url)
    documents = loader.load()
    return documents


def load_pdf_directory(directory_path="./"):
    """Load all PDF files from a directory and return their content."""
    # https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.pdf.PyPDFDirectoryLoader.html
    loader = PyPDFDirectoryLoader(directory_path)
    documents = loader.load()
    return documents

# documents = load_pdf_return_documents()
# print("\n\n********* Documents : "+str(documents))

documents = load_from_web()
print("\n\n ********* Web : "+str(documents))




