from openai import OpenAI
from message import SinglePartMessage, MultiPartMessage
from chat import Chat
import convert_messages_to_dict
from typing import List


# from utils.chat_utils.message import SinglePartMessage, MultiPartMessage
# from utils.chat_utils.chat import Chat


# declaring Global variables
API_KEY = ""
client = OpenAI(api_key=API_KEY)
roles = {'genai': 'assistant', 'human': 'user', 'developer': 'system'}



def chat_to_messages(chat: Chat):
    """
    Takes individual messages from chat and returns it in a list of dictionary of following format:
            [{'role': "...", "content": "...."}
                        .
                        .
                        .
             {'role': "...", "content": "...."}]
    Returns:
        List of dictionary in the above format
    """
    
    # mapping message_roles with roles for chatgpt-genai roles
    messages = chat.get_messages()
    
    #converting messages of chat to list of dictionary {"role": "assistant/user/system", "content": [ ....] }
    chat_list = []
    for message in messages:
        if message.get_message_type() == "multipart":
            new_message = {
                "role": roles[message.get_author_type()],
                "content": convert_messages_to_dict.convert_multipart(message)
            }
        else:
            new_message = {
                "role": roles[message.get_author_type()],
                "content": [convert_messages_to_dict.convert_single_part(message)]
            }
        chat_list.append(new_message)

    
    return chat_list

        

def get_response(model: str, message_list: List[dict], stream = False):
    """
    Get the response from the chat using provided model and message_list
    Args:
        model: name of the model
        message_list: list of dictionary {"role": "assistant/user/system", "content": " ...."}
        stream: bool, if True returns a generator of responses, else returns a list of responses
    
    Returns:
    """
    response = client.chat.completions.create(
        model=model,
        messages = message_list,
        stream = stream
    )
    return response




#############################################
#    Non-Streaming
#############################################

#for multiple messages
def get_chat_input(chat: Chat):
    """
    Generates response for a particular chat (Chat <- chat.py)

    Args:
        chat: a chat instance with message_type as only SinglePartMessage type

    Returns: 
        chat: the same parameter chat is returned with appended new message from the chat
    """

    # converting the message_types to appropriate list for generating response
    message_list = chat_to_messages(chat)

    # generating response from gpt
    response = get_response('gpt-4o', message_list)

    # getting only the text content from the response
    generated_reply = response.choices[0].message.content
    
    chat.append_message_chunk_by_attribute(author="", 
                                               author_type="genai", 
                                               message_type="text", 
                                               message_chunk_by_attribute=generated_reply, 
                                               key = "text")

    return chat

#############################################
#           Streaming
#############################################
def get_chat_input_streaming(chat: Chat):
    """
    Generates response for a particular chat (Chat <- chat.py)

    Args:
        chat: a chat instance with message_type as only SinglePartMessage type

    Returns: 
        chat: the same parameter chat is returned with appended new message from the chat one stream at a time
    """

    # converting the message_types to appropriate list for generating response
    print("Generating response...")
    print(5+5)
    message_list = chat_to_messages(chat)
    
    # generating response from gpt
    response = get_response('gpt-4o', message_list, stream = True)
    # Process the streaming response
    for chunk in response:
        
        chat.append_message_chunk_by_attribute(author="", 
                                               author_type="genai", 
                                               message_type="text", 
                                               message_chunk_by_attribute={'text': chunk.choices[0].message.content}, 
                                               key = "text")
        yield chat


def generate_response(chat: Chat, stream = False):
    """
    Generates response for a particular chat (Chat <- chat.py)

    Args:
        chat: a chat instance with message_type as only SinglePartMessage type

    Returns: 
        chat: the same parameter chat is returned with appended new message from the chat
    """
    if not stream:
        get_chat_input(chat)
    else:
        print("Streaming response...")
        get_chat_input_streaming(chat)