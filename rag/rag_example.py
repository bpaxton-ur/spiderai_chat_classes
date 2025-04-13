from rag.rag_api import RAGService
from rag.rag_handler import RAGHandler
from message import SinglePartMessage
from chat import Chat

def main():
    # Initialize the RAG service and handler
    rag_service = RAGService()
    rag_handler = RAGHandler(rag_service)
    
    # Create a new chat
    chat = Chat()
    
    # Example 1: Create a vector store
    # Create a rag_create_store message
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
    
    # Example 2: Query the vector store
    # Create a rag_query message
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
    
    # Print the chat history
    for message in chat.get_messages():
        if message.get_message_type() == "rag_response":
            response_type = message.get_message_value_by_attribute("type")
            if response_type == "store_created":
                print(f"Store created: {message.get_message_value_by_attribute('store_id')}")
                print(f"Document count: {message.get_message_value_by_attribute('document_count')}")
            elif response_type == "query_result":
                print(f"Answer: {message.get_message_value_by_attribute('answer')}")
            elif response_type == "error":
                print(f"Error: {message.get_message_value_by_attribute('message')}")

if __name__ == "__main__":
    main() 