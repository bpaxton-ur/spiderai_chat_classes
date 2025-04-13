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
    """A pure service class that handles RAG operations without chat processing"""
    
    def __init__(self, persist_dir: str = "./chroma_db"):
        self.persist_dir = persist_dir
        self.embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
        self.vectorstores = {}  # Store multiple vectorstores by ID
        self.chains = {}  # Store multiple chains by ID

    def create_vectorstore(self, files: List[str], store_id: str) -> Dict[str, Any]:
        """Create a vectorstore from files"""
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
        """Create a conversational chain for a vectorstore"""
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
        """Query a vectorstore and return the response"""
        if store_id not in self.chains:
            raise ValueError(f"Chain for vectorstore {store_id} not found")
            
        result = self.chains[store_id]({"question": query})
        return {
            "answer": result["answer"],
            "store_id": store_id
        }

    def get_store_info(self, store_id: str) -> Optional[Dict[str, Any]]:
        """Get information about a vector store"""
        if store_id not in self.vectorstores:
            return None
            
        return {
            "store_id": store_id,
            "exists": True,
            "has_chain": store_id in self.chains
        } 