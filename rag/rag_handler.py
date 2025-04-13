from typing import Optional
from message import SinglePartMessage
from chat import Chat
from rag.rag_api import RAGService

class RAGHandler:
    """Handles RAG operations through the chat class"""
    
    def __init__(self, rag_service: RAGService):
        self.rag_service = rag_service

    def process_message(self, chat: Chat) -> Optional[SinglePartMessage]:
        """Process the last message in the chat and return a response if needed"""
        last_message = chat.get_messages()[-1]
        
        if last_message.get_message_type() == "rag_create_store":
            # Handle vector store creation
            store_id = last_message.get_message_value_by_attribute("store_id")
            files = last_message.get_message_value_by_attribute("files")
            
            result = self.rag_service.create_vectorstore(files, store_id)
            
            return SinglePartMessage.create_message(
                author="genai",
                author_type="genai",
                message_type="rag_response",
                message_value={
                    "type": "store_created",
                    "store_id": result["store_id"],
                    "document_count": result["document_count"]
                }
            )
            
        elif last_message.get_message_type() == "rag_query":
            # Handle vector store query
            store_id = last_message.get_message_value_by_attribute("store_id")
            query = last_message.get_message_value_by_attribute("query")
            
            # Check if store exists
            store_info = self.rag_service.get_store_info(store_id)
            if not store_info:
                return SinglePartMessage.create_message(
                    author="genai",
                    author_type="genai",
                    message_type="rag_response",
                    message_value={
                        "type": "error",
                        "message": f"Vector store {store_id} not found"
                    }
                )
            
            result = self.rag_service.query(store_id, query)
            
            return SinglePartMessage.create_message(
                author="genai",
                author_type="genai",
                message_type="rag_response",
                message_value={
                    "type": "query_result",
                    "store_id": result["store_id"],
                    "answer": result["answer"]
                }
            )
            
        return None 