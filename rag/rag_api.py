"""
RAG (Retrieval-Augmented Generation) Service

This module provides a service layer for RAG operations, handling vector store creation,
document processing, and querying. It uses LangChain for document processing and vector storage,
and OpenAI for embeddings and generation.

Example:
    ```python
    from rag.rag_api import RAGService
    
    # Initialize the service
    rag_service = RAGService()
    
    # Create a vector store
    result = rag_service.create_vectorstore(
        files=["doc1.txt", "doc2.txt"],
        store_id="my_store"
    )
    
    # Query the store
    response = rag_service.query(
        store_id="my_store",
        query="What is the main topic?"
    )
    ```
"""

import os
from typing import List, Dict, Any, Optional
from langchain.document_loaders import UnstructuredFileLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

# Load OpenAI API key
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

class RAGService:
    """
    A service class that handles RAG operations including vector store creation and querying.
    
    This class manages the creation and maintenance of vector stores, document processing,
    and querying capabilities. It uses Chroma for vector storage and OpenAI for embeddings
    and generation.
    
    Attributes:
        persist_dir (str): Directory where vector stores are persisted
        embeddings (OpenAIEmbeddings): OpenAI embeddings instance
        vectorstores (Dict[str, Chroma]): Dictionary of vector stores by ID
        chains (Dict[str, ConversationalRetrievalChain]): Dictionary of conversation chains by ID
    """
    
    def __init__(self, persist_dir: str = "./chroma_db"):
        """
        Initialize the RAG service.
        
        Args:
            persist_dir (str): Directory where vector stores will be persisted
        """
        self.persist_dir = persist_dir
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self.vectorstores = {}  # Store multiple vectorstores by ID
        self.chains = {}  # Store multiple chains by ID

    def create_vectorstore(self, files: List[str], store_id: str) -> Dict[str, Any]:
        """
        Create a vector store from a list of files.
        
        This method:
        1. Loads documents from the provided files
        2. Splits them into chunks
        3. Creates embeddings
        4. Stores them in a Chroma vector store
        5. Creates a conversation chain for the store
        
        Args:
            files (List[str]): List of file paths to process
            store_id (str): Unique identifier for the vector store
            
        Returns:
            Dict[str, Any]: Information about the created store
            
        Example:
            ```python
            result = rag_service.create_vectorstore(
                files=["doc1.txt", "doc2.txt"],
                store_id="my_store"
            )
            # Returns: {"store_id": "my_store", "document_count": 42}
            ```
        """
        all_chunks = []
        for path in files:
            loader = UnstructuredFileLoader(path)
            docs = loader.load()
            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunks = splitter.split_documents(docs)
            all_chunks.extend(chunks)

        vectorstore = Chroma.from_documents(
            documents=all_chunks,
            embedding=self.embeddings,
            persist_directory=os.path.join(self.persist_dir, store_id)
        )
        vectorstore.persist()
        
        self.vectorstores[store_id] = vectorstore
        self._create_chain(store_id)
        
        return {
            "store_id": store_id,
            "document_count": len(all_chunks)
        }

    def _create_chain(self, store_id: str) -> None:
        """
        Create a conversational chain for a vector store.
        
        This method creates a conversation chain that includes:
        - A retriever for the vector store
        - Memory for conversation history
        - An OpenAI LLM for generation
        
        Args:
            store_id (str): ID of the vector store to create a chain for
            
        Raises:
            ValueError: If the vector store doesn't exist
        """
        if store_id not in self.vectorstores:
            raise ValueError(f"Vectorstore {store_id} not found")
            
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        retriever = self.vectorstores[store_id].as_retriever()
        
        chain = ConversationalRetrievalChain.from_llm(
            llm=OpenAI(openai_api_key=openai_api_key),
            retriever=retriever,
            memory=memory
        )
        
        self.chains[store_id] = chain

    def query(self, store_id: str, query: str) -> Dict[str, Any]:
        """
        Query a vector store with a natural language question.
        
        Args:
            store_id (str): ID of the vector store to query
            query (str): The question to ask
            
        Returns:
            Dict[str, Any]: The query result
            
        Example:
            ```python
            response = rag_service.query(
                store_id="my_store",
                query="What is the main topic?"
            )
            # Returns: {"answer": "The main topic is...", "store_id": "my_store"}
            ```
            
        Raises:
            ValueError: If the vector store or chain doesn't exist
        """
        if store_id not in self.chains:
            raise ValueError(f"Chain for vectorstore {store_id} not found")
            
        result = self.chains[store_id]({"question": query})
        return {
            "answer": result["answer"],
            "store_id": store_id
        }

    def get_store_info(self, store_id: str) -> Optional[Dict[str, Any]]:
        """
        Get information about a vector store.
        
        Args:
            store_id (str): ID of the vector store to get info for
            
        Returns:
            Optional[Dict[str, Any]]: Information about the store, or None if it doesn't exist
            
        Example:
            ```python
            info = rag_service.get_store_info("my_store")
            # Returns: {"store_id": "my_store", "exists": True, "has_chain": True}
            ```
        """
        if store_id not in self.vectorstores:
            return None
            
        return {
            "store_id": store_id,
            "exists": True,
            "has_chain": store_id in self.chains
        } 