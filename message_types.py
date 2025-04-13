"""
utils/chat_utils/message_types.py

This file contains a dictionary of all allowable message types and you can expand this if you want.

Note: The structure for each message type is as follows:

type_name : {
    "message_value_keys": set(list of attributes for type),
    "message_value_attribute_types":{
        name of attribute # 1: type of attribute # 1,
        name of attribute # 2: type of attribute # 2,
        ...
        name of attribute # N: type of attribute # N,
        },
    "empty_message_value": Value of an empty message of this type
 }

Author: M. Saif Mehkari
Version: 1.0
License Info: See license.txt file
"""

message_types = {
    # Text Type     
    "text":{
        "message_value_keys": set(["text"]),
        "message_value_attribute_types":{
            "text": str
        },
        "empty_message_value":{"text": ""},
    },

    # Image Type (Base64)
    "image_base64":{
        "message_value_keys": set(["filename", "image_base64", "mime_type"]),
        "message_value_attribute_types":{
            "filename": str,
            "image_base64": bytes,
            "mime_type": str,
        },
        "empty_message_value":{"filename":"", "image_base64": b"", "mime_type":""}
    }, 

    # Image Type (URL)     
    "image_url":{
        "message_value_keys": set(["filename", "url", "mime_type"]),
        "message_value_attribute_types":{
            "filename": str,
            "url": str,
            "mime_type": str,
        },
        "empty_message_value":{"filename":"", "url":"", "mime_type":""}
    },   

    # File Type (Base64)     
    "file_base64":{
        "message_value_keys": set(["filename", "file_base64", "mime_type"]),
        "message_value_attribute_types":{
            "filename": str,
            "file_base64": bytes,
            "mime_type": str,
        },
        "empty_message_value":{"filename":"", "file_base64": b"", "mime_type":""}
    },  

    # File Type (URL)     
    "file_url":{
        "message_value_keys": set(["filename", "url", "mime_type"]),
        "message_value_attribute_types":{
            "filename": str,
            "url": str,
            "mime_type": str,
        },
        "empty_message_value":{"filename":"", "url":"", "mime_type":""}
    },   

    # Audio Type (Base64)     
    "audio_base64":{
        "message_value_keys": set(["filename", "audio_base64", "mime_type"]),
        "message_value_attribute_types":{
            "filename": str,
            "audio_base64": bytes,
            "mime_type": str,
        },
        "empty_message_value":{"filename":"", "audio_base64": b"", "mime_type":""}
    },

    # Audio Type (URL)     
    "audio_url":{
        "message_value_keys": set(["filename", "url", "mime_type"]),
        "message_value_attribute_types":{
            "filename": str,
            "url": str,
            "mime_type": str,
        },
        "empty_message_value":{"filename":"", "url":"", "mime_type":""}
    },

    # Vector Store Type
    "vector_store":{
        "message_value_keys": set(["store_id", "documents", "embeddings"]),
        "message_value_attribute_types":{
            "store_id": str,
            "documents": list,
            "embeddings": list,
        },
        "empty_message_value":{"store_id": "", "documents": [], "embeddings": []}
    },

    # RAG Create Store Type
    "rag_create_store":{
        "message_value_keys": set(["store_id", "files"]),
        "message_value_attribute_types":{
            "store_id": str,
            "files": list,
        },
        "empty_message_value":{"store_id": "", "files": []}
    },

    # RAG Query Type
    "rag_query":{
        "message_value_keys": set(["store_id", "query"]),
        "message_value_attribute_types":{
            "store_id": str,
            "query": str,
        },
        "empty_message_value":{"store_id": "", "query": ""}
    },

    # RAG Response Type
    "rag_response":{
        "message_value_keys": set(["type", "store_id", "answer", "document_count", "message"]),
        "message_value_attribute_types":{
            "type": str,
            "store_id": str,
            "answer": str,
            "document_count": int,
            "message": str,
        },
        "empty_message_value":{
            "type": "",
            "store_id": "",
            "answer": "",
            "document_count": 0,
            "message": ""
        }
    }
}