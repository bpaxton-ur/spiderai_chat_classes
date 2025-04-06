import os
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI # using Langchain's integration
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

# Load OpenAI API key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Load and split multiple files
def load_and_split_files(file_paths):
    """Load files from given list of file paths

    Args:
        file_paths (list of str): List of file paths in string format

    Returns:
        List of chunks - Documents
    """
    all_chunks = []
    for path in file_paths:
        loader = UnstructuredFileLoader(path)
        docs = loader.load()
        splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        chunks = splitter.split_documents(docs)
        all_chunks.extend(chunks)
    return all_chunks

# Embed and store in Chroma
def create_vectorstore(chunks, persist_dir="./chroma_db"):
    """Create a Chroma vector store based on the Documents list

    Args:
        chunks (List of Documents): Splitter documents
        persist_dir (DB directory): Configured Chroma directory. Defaults to "./chroma_db".

    Returns:
        vectorstore: Chroma vector store
    """
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    vectorstore = Chroma.from_documents(documents=chunks, embedding=embeddings, persist_directory=persist_dir)
    vectorstore.persist()
    return vectorstore

# Build the conversational retrieval chain
    """Create a chain of conversation based on saved vector store
    """
def create_conversational_chain(vectorstore):
    memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    retriever = vectorstore.as_retriever()
    chain = ConversationalRetrievalChain.from_llm(
        llm=OpenAI(openai_api_key=openai_api_key),
        retriever=retriever,
        memory=memory
    )
    return chain

# Main chat loop
def main():
    # This could be customed with a component when extending to the frontend
    files = input("Enter comma-separated paths to the files: ").split(',')
    files = [f.strip() for f in files if f.strip()]
    
    if not files:
        print("No files provided.")
        return
    
    # Correct routine to build a RAG conversation
    print("Loading and processing files...")
    chunks = load_and_split_files(files)

    print("Creating vectorstore...")
    vectorstore = create_vectorstore(chunks)

    print("Setting up conversational chain...")
    qa_chain = create_conversational_chain(vectorstore)

    print("\nYou can now chat with your documents! Type 'exit' to quit.\n")

    while True:
        query = input("You: ")
        if query.lower() == "exit":
            break
        result = qa_chain({"question": query})
        print("OpenAI:", result["answer"])

if __name__ == "__main__":
    main()