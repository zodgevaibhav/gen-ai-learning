from langchain_ollama import ChatOllama
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, PyPDFDirectoryLoader
from langchain_ollama import OllamaEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.documents import Document



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

# Create an instance of the InMemoryVectorStore class to store the embeddings
# When we give embedding object to the vector store, it initialize with the given embedding function.
    # Ref: https://python.langchain.com/api_reference/core/vectorstores/langchain_core.vectorstores.in_memory.InMemoryVectorStore.html#langchain_core.vectorstores.in_memory.InMemoryVectorStore.dump
vector_store = InMemoryVectorStore(embedding=obj_embeddings)

vector_store.add_documents(load_pdf_return_documents())

similar_vectors = vector_store.search("Does vaibhav have github ?", search_type="similarity", k=1)

print("\n\n********* Similar Vectors : "+str(similar_vectors))

# Save the vector store to a file
##vector_store.dump("vector_store.json")
