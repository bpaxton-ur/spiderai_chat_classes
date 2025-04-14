# RAG (Retrieval-Augmented Generation) System

This RAG system integrates with the chat class to provide document-based question answering capabilities. It uses LangChain for document processing and vector storage, and OpenAI for embeddings and generation.

## Features

- Create and manage multiple vector stores
- Process documents and create embeddings
- Query vector stores with natural language questions
- Maintain conversation history for context-aware responses
- Integrates seamlessly with the chat class system

## Prerequisites

- Python 3.8+
- OpenAI API key
- Required Python packages (install via `pip install -r requirements.txt`):
  - langchain
  - openai
  - chromadb
  - python-dotenv

## Setup

1. Create a `.env` file in your project root with your OpenAI API key:
```env
OPENAI_API_KEY=your_api_key_here
```

2. Import the necessary components:
```python
from rag.rag_api import RAGService
from rag.rag_handler import RAGHandler
from message import SinglePartMessage
from chat import Chat
```

## Usage

### Basic Setup

```python
# Initialize the RAG service and handler
rag_service = RAGService()
rag_handler = RAGHandler(rag_service)

# Create a new chat
chat = Chat()
```

### Creating a Vector Store

To create a vector store from documents:

```python
# Create a rag_create_store message
create_store_message = SinglePartMessage.create_message(
    author="human",
    author_type="human",
    message_type="rag_create_store",
    message_value={
        "store_id": "my_store",  # Unique identifier for the store
        "files": ["path/to/document1.txt", "path/to/document2.txt"]  # List of document paths
    }
)

# Add the message to the chat
chat.append_message(create_store_message)

# Process the message
response = rag_handler.process_message(chat)
if response:
    chat.append_message(response)
```

### Querying a Vector Store

To query a vector store:

```python
# Create a rag_query message
query_message = SinglePartMessage.create_message(
    author="human",
    author_type="human",
    message_type="rag_query",
    message_value={
        "store_id": "my_store",  # The store to query
        "query": "What is the main topic of the documents?"  # Your question
    }
)

# Add the message to the chat
chat.append_message(query_message)

# Process the message
response = rag_handler.process_message(chat)
if response:
    chat.append_message(response)
```

### Handling Responses

RAG responses come in different types:

```python
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
```

## Message Types

The RAG system uses several message types:

1. `rag_create_store`: For creating new vector stores
   - `store_id`: Unique identifier for the store
   - `files`: List of document paths to process

2. `rag_query`: For querying vector stores
   - `store_id`: The store to query
   - `query`: The question to ask

3. `rag_response`: For RAG system responses
   - `type`: Response type ("store_created", "query_result", or "error")
   - `store_id`: The store ID
   - `answer`: The answer to the query (for query results)
   - `document_count`: Number of documents processed (for store creation)
   - `message`: Error message (for errors)

## Error Handling

The system handles various error cases:
- Non-existent vector stores
- Invalid file paths
- Processing errors

All errors are returned as `rag_response` messages with `type: "error"`.

## Notes

1. Use unique `store_id` values for different document collections
2. Keep document paths relative to your project root
3. Process documents in batches if dealing with large collections
4. Use descriptive queries for better results
5. Check for error responses after each operation

## Example

See `rag_example.py` for a complete working example of the RAG system in action. 