# Build knowledge base using Langchain and Ollama


from langchain_ollama import ChatOllama
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, PyPDFDirectoryLoader
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter



def load_pdf_return_documents(file_path="./VaibhavZodge.pdf"):
    """Load a PDF file and return its content."""
    # https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.pdf.PyPDFLoader.html
    docs = []
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    id=1
    for document in documents:
        docs.append(Document(id=id, page_content=document.page_content))
        id=id+1

    return docs


# Create an instance of the OllamaEmbeddings class
obj_embeddings = OllamaEmbeddings(model = "llama3")

# Create an instance of the Chroma class to store the embeddings
# When we give embedding object to the vector store, it initialize with the given embedding function.
    # Ref: https://python.langchain.com/api_reference/chroma/vectorstores/langchain_chroma.vectorstores.Chroma.html#langchain_chroma.vectorstores.Chroma
vector_store = Chroma(embedding_function=obj_embeddings, collection_name="vaibhav_zodge", persist_directory="./chroma_db")

# Load the PDF documents and split them into chunks
# The text splitter is used to split the documents into smaller chunks for better embedding
# and retrieval performance.
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)

# Load the PDF documents and split them into chunks
docs = splitter.split_documents(load_pdf_return_documents())

# Add the documents to the vector store
vector_store.add_documents(docs)

# Search for similar vectors in the vector store
similar_vectors = vector_store.search("Does vaibhav have github ?", search_type="similarity", k=5)

print("\n\n********* Similar Vectors : "+str(similar_vectors))


