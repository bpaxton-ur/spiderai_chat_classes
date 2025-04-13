"""
RAG System Example

This module demonstrates how to use the RAG system with the chat class.
It shows how to:
1. Create a vector store from documents
2. Query the vector store
3. Handle responses

Example Usage:
    ```bash
    python rag_example.py
    ```
"""

from rag.rag_api import RAGService
from rag.rag_handler import RAGHandler
from message import SinglePartMessage
from chat import Chat

def main():
    """
    Main function demonstrating RAG system usage.
    
    This function:
    1. Initializes the RAG service and handler
    2. Creates a vector store from documents
    3. Queries the vector store
    4. Prints the results
    """
    # Initialize the RAG service and handler
    rag_service = RAGService()
    rag_handler = RAGHandler(rag_service)
    
    # Create a new chat
    chat = Chat()
    
    # Example 1: Create a vector store
    print("\n=== Creating Vector Store ===")
    create_store_message = SinglePartMessage.create_message(
        author="human",
        author_type="human",
        message_type="rag_create_store",
        message_value={
            "store_id": "example_store",
            "files": ["path/to/document1.txt", "path/to/document2.txt"]
        }
    )
    
    # Add the message to the chat
    chat.append_message(create_store_message)
    
    # Process the message
    response = rag_handler.process_message(chat)
    if response:
        chat.append_message(response)
        # Print the response
        response_type = response.get_message_value_by_attribute("type")
        if response_type == "store_created":
            print(f"Store created: {response.get_message_value_by_attribute('store_id')}")
            print(f"Document count: {response.get_message_value_by_attribute('document_count')}")
        elif response_type == "error":
            print(f"Error: {response.get_message_value_by_attribute('message')}")
    
    # Example 2: Query the vector store
    print("\n=== Querying Vector Store ===")
    query_message = SinglePartMessage.create_message(
        author="human",
        author_type="human",
        message_type="rag_query",
        message_value={
            "store_id": "example_store",
            "query": "What is the main topic of the documents?"
        }
    )
    
    # Add the message to the chat
    chat.append_message(query_message)
    
    # Process the message
    response = rag_handler.process_message(chat)
    if response:
        chat.append_message(response)
        # Print the response
        response_type = response.get_message_value_by_attribute("type")
        if response_type == "query_result":
            print(f"Answer: {response.get_message_value_by_attribute('answer')}")
        elif response_type == "error":
            print(f"Error: {response.get_message_value_by_attribute('message')}")

if __name__ == "__main__":
    main() 