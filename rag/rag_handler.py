"""
RAG (Retrieval-Augmented Generation) Handler

This module provides a handler that integrates RAG operations with the chat class system.
It processes chat messages to perform RAG operations and returns appropriate responses.

Example:
    ```python
    from rag.rag_api import RAGService
    from rag.rag_handler import RAGHandler
    from message import SinglePartMessage
    from chat import Chat
    
    # Initialize the service and handler
    rag_service = RAGService()
    rag_handler = RAGHandler(rag_service)
    
    # Create a chat
    chat = Chat()
    
    # Create a vector store
    create_store_message = SinglePartMessage.create_message(
        author="human",
        author_type="human",
        message_type="rag_create_store",
        message_value={
            "store_id": "my_store",
            "files": ["doc1.txt", "doc2.txt"]
        }
    )
    chat.append_message(create_store_message)
    response = rag_handler.process_message(chat)
    if response:
        chat.append_message(response)
    ```
"""

from typing import Optional
from message import SinglePartMessage
from chat import Chat
from rag.rag_api import RAGService

class RAGHandler:
    """
    A handler that integrates RAG operations with the chat class system.
    
    This class processes chat messages to perform RAG operations and returns
    appropriate responses. It acts as a bridge between the chat system and
    the RAG service.
    
    Attributes:
        rag_service (RAGService): The RAG service instance to use for operations
    """
    
    def __init__(self, rag_service: RAGService):
        """
        Initialize the RAG handler.
        
        Args:
            rag_service (RAGService): The RAG service instance to use
        """
        self.rag_service = rag_service

    def process_message(self, chat: Chat) -> Optional[SinglePartMessage]:
        """
        Process the last message in the chat and return a response if needed.
        
        This method:
        1. Gets the last message from the chat
        2. Determines the message type
        3. Performs the appropriate RAG operation
        4. Returns a response message
        
        Args:
            chat (Chat): The chat containing the message to process
            
        Returns:
            Optional[SinglePartMessage]: A response message, or None if no response is needed
            
        Example:
            ```python
            # Process a vector store creation message
            response = rag_handler.process_message(chat)
            if response:
                chat.append_message(response)
                
            # Process a query message
            response = rag_handler.process_message(chat)
            if response:
                chat.append_message(response)
            ```
        """
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