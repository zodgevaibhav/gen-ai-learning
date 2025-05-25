import streamlit as st
from langchain_ollama import ChatOllama
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, PyPDFDirectoryLoader
from langchain_ollama import OllamaEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.prompts import ChatPromptTemplate






import tempfile

def create_embeddings_from_pdf(pdf_file):
    """Load a PDF file and return its content."""
    # https://python.langchain.com/api_reference/community/document_loaders/langchain_community.document_loaders.pdf.PyPDFLoader.html
    docs = []
    # Save the uploaded file to a temporary location
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        tmp_file.write(pdf_file.read())
        tmp_file_path = tmp_file.name
    # Load the PDF file using PyPDFLoader
    loader = PyPDFLoader(tmp_file_path)
    # Load the pages from the PDF file
    pages = loader.load_and_split()
    # Create Document objects for each page
    id=1
    for page in pages:
        docs.append(Document(id=id, page_content=page.page_content))
        id=id+1

    # Split the documents into smaller chunks for better embedding and retrieval performance.
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
          # Chunk size is the maximum length of each chunk, and chunk overlap is the number of characters that overlap between chunks.
          # Overlping meaning, the last 200 characters of the previous chunk will be included in the next chunk.
          # Overlapping helps to maintain context between chunks.
    docs = splitter.split_documents(docs)

    vector_store = Chroma(embedding_function=OllamaEmbeddings(model="llama3"), collection_name="vaibhav_zodge", persist_directory="./chroma_db")
    vector_store.add_documents(docs)
    
    # Store vector store to session state for later use
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = vector_store
    

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


################# MAIN FUNCTION ####################

st.title("RAG Pipeline Chatbot")
st.header("Upload PDF and Chat with it")

with st.sidebar:
    st.subheader("Upload PDF")
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    # Create embeddings from the uploaded PDF file
    create_embeddings_from_pdf(uploaded_file)
    st.success("PDF uploaded and embeddings created successfully!")

# Check if the vector store is already created
if "vector_store" in st.session_state:
    st.success("Vector store is ready to use!")

question = st.chat_input("Ask a question about the PDF content:")
if question:
    # Search for similar vectors in the vector store
    context = st.session_state.vector_store.search(question, search_type="similarity", k=5)
    
    # Generate response using RAG pipeline
    response = rag_pipeline(context, question)
    
    # Display the response
    st.write(response)



