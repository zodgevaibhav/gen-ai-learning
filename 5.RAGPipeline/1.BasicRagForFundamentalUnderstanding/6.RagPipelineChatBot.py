
from langchain_ollama import ChatOllama
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, PyPDFDirectoryLoader
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate


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

def rag_pipeline(context, question="Who is Vaibhav Zodge?"):    
    template = """
    You are a helpful assistant. Answer the question based on the context provided.
    Answer with not more than 100 words.
    Don't talk about context, just answer the question.
    If you don't know the answer, say "I don't know".
    Question: {question}
    Context: {context}
    Answer:
    """

    prompt_template = ChatPromptTemplate.from_template(template)
    prompt = prompt_template.invoke({"question":question, "context":context})
    #print("\n\n********* Prompt : "+str(prompt))

    model = ChatOllama(model="llama3", temperature=0.1)

    response = model.invoke(prompt)
    return response.content


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
question = "Explain Vaibhav Zodge in point by point format"
context = vector_store.search(question, search_type="similarity", k=5)

response = rag_pipeline(context, question)

print(response)


