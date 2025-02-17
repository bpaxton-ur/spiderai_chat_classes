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

    # Image Type     
    "image_base64":{
        "message_value_keys": set(["filename", "image_base64", "mime_type"]),
        "message_value_attribute_types":{
            "filename": str,
            "image_base64": bytes,
            "mime_type": str            
        },
        "empty_message_value":{"filename":"", "image_base64": b"", "mime_type":""}
    }            
}

