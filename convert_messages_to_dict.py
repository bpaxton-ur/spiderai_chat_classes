import requests
import convert_file_to_text
import base64
from message import SinglePartMessage, MultiPartMessage


#for generating transcription from audio
from openai import OpenAI
API_KEY = ""
client = OpenAI(api_key=API_KEY)



def convert_text(message: SinglePartMessage):
    """
    Convert a single part message with message_type "text" to appropriate dictionary 
    to feed it into chat
    Parameter:
        message: a SinglePartMessage with message_type == "text"
    
    Returns: 
        message_dict: a dictionary with key "type" = "text" and text = message value of the message
        {
            'type': 'text',
            'text': "....some string....."
        }
    """
    message_dict = {
                        'type': 'text',
                        'text': message.get_message_value_by_attribute('text')
                    }
    
    return message_dict

def convert_image_url(message: SinglePartMessage):
    """
    Convert a single part message with message_type "image_url" to appropriate dictionary 
    to feed it into chat
    Parameter:
        message: a SinglePartMessage with message_type == "image_url"
    
    Returns: 
        message_dict: a dictionary with following format
        {
            'type': 'image_url',
            'image_url': "some link"
        }
    """

    message_dict = {
                        "type": "image_url",
                        "image_url": {"url": message.get_message_value_by_attribute(key ="url")}
                    }

    return message_dict

def convert_image_base64(message: SinglePartMessage):
    """
    Convert a single part message with message_type "image_base64" to appropriate dictionary 
    to feed it into chat
    Parameter:
        message: a SinglePartMessage with message_type == "image_base64"
    
    Returns: 
        message_dict: a dictionary with following format
        {
            'type': 'image_url',
            'image_url': "data:image/jpeg;base64,...content of base64...."
        }
    """
    message_dict =  {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64," + message.get_message_value()['image_base64'].decode("utf-8")}
                    }
                     
    return message_dict

def convert_image_bytesio(message: SinglePartMessage):
    """
    Convert a single part message with message_type "image_bytesio" to appropriate dictionary 
    to feed it into chat
    Parameter:
        message: a SinglePartMessage with message_type == "image_bytesio"
    
    Returns: 
        message_dict: a dictionary with following format
        {
            'type': 'image_url',
            'image_url': "data:image/jpeg;base64,...content of base64...."
        }
    """
    
    #converting the bytesio to base64 string
    image_base64 = base64.b64encode(message.get_message_value()['image_bytesio']).decode("utf-8")
    
    message_dict =  {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64," + image_base64}
                    }
                     
    return message_dict
 


def convert_file_url(message: SinglePartMessage):
    """
    Method uses convert_file_to_text to get the content of a file through a given url and 
    creates a text-like  message for the chat

    Note: current compatible formats are .docx, .md, .json, .txt, .pdf
    
    Parameter:
        message: a SinglePartMessage with message_type == "file_url"
    
    Returns: 
        message_dict: a dictionary with following format
        {
            'type': 'text',
            'text': "... content of the file ..."
        }
    """

    #getting the url of the file and the mime type of the file 
    url = message.get_message_value()['url']
    mime = message.get_message_value()['mime_type']

    supported_formats = ['.pdf', '.json', '.docx', '.txt', '.md']

    #based on the file type appropriate function from the library convert_file_to_text is used
    if mime == ".pdf":
        text = convert_file_to_text.read_pdf_from_url(url)
    elif mime == ".json":
        text = convert_file_to_text.read_json_from_url(url)
    elif mime == ".docx":
        text = convert_file_to_text.read_docx_from_url(url)
    elif mime == ".txt":
        text = convert_file_to_text.read_txt_from_url(url)
    elif mime == ".md":
        text = convert_file_to_text.read_markdown_from_url(url)
    else:
        # raising error if the file format is not supported
        raise ValueError(f"Unsupported file format: {mime}. Supported formats are: {', '.join(supported_formats)}")
    
    message_dict = {
                        "type": "text",
                        "text": text
                    }

    return message_dict

def convert_file_base64(message: SinglePartMessage):
    """
    Method uses convert_file_to_text to get the content of a file through a given base64 and 
    creates a text-like  message for the chat

    Note: current compatible formats are .docx, .md, .json, .txt, .pdf
    
    Parameter:
        message: a SinglePartMessage with message_type == "file_base64"
    
    Returns: 
        message_dict: a dictionary with following format
        {
            'type': 'text',
            'text': "... content of the file ..."
        }
    """

    #getting the base64 value and the mime type of the file 
    file_base64 = message.get_message_value()['file_base64']
    mime = message.get_message_value()['mime_type']

    supported_formats = ['.pdf', '.json', '.docx', '.txt', '.md']

    #based on the file format appropriate function from the convert_file_to_text is used. 
    if mime == ".pdf":
        text = convert_file_to_text.read_pdf_from_base64(file_base64)
    elif mime == ".json":
        text = convert_file_to_text.read_json_from_base64(file_base64)
    elif mime == ".docx":
        text = convert_file_to_text.read_docx_from_base64(file_base64)
    elif mime == ".txt":
        text = convert_file_to_text.read_txt_from_base64(file_base64)
    elif mime == ".md":
        text = convert_file_to_text.read_markdown_from_base64(file_base64)
    else:
        # raising error if the file format is not supported
        raise ValueError(f"Unsupported file format: {mime}. Supported formats are: {', '.join(supported_formats)}")
    
    
    message_dict = {
                        "type": "text",
                        "text": text
                    }

    return message_dict 

def convert_file_bytesio(message: SinglePartMessage):
    """
    Method uses convert_file_to_text to get the content of a file through a given BytesIO object and 
    creates a text-like message for the chat.

    Note: current compatible formats are .docx, .md, .json, .txt, .pdf
    
    Parameter:
        message: a SinglePartMessage with message_type == "file_bytesio"
    
    Returns: 
        message_dict: a dictionary with the following format
        {
            'type': 'text',
            'text': "... content of the file ..."
        }
    """

    # Getting the BytesIO value and the mime type of the file
    file_bytesio = message.get_message_value()['file_bytesio']
    mime = message.get_message_value()['mime_type']

    supported_formats = ['.pdf', '.json', '.docx', '.txt', '.md']

    # Check if the mime type is supported
    if mime not in supported_formats:
        raise ValueError(f"Unsupported file format: {mime}")

    # Extract content based on the file type
    if mime == '.pdf':
        from convert_file_to_text import read_pdf_from_bytesio
        text = read_pdf_from_bytesio(file_bytesio)
    elif mime == '.json':
        from convert_file_to_text import read_json_from_bytesio
        text = read_json_from_bytesio(file_bytesio)
    elif mime == '.docx':
        from convert_file_to_text import read_docx_from_bytesio
        text = read_docx_from_bytesio(file_bytesio)
    elif mime == '.txt':
        from convert_file_to_text import read_txt_from_bytesio
        text = read_txt_from_bytesio(file_bytesio)
    elif mime == '.md':
        from convert_file_to_text import read_markdown_from_bytesio
        text = read_markdown_from_bytesio(file_bytesio)
    else:
        raise ValueError(f"Unsupported file format: {mime}")

    # Create the message dictionary
    message_dict = {
        "type": "text",
        "text": text
    }

    return message_dict


def audio_transcription(encoded_string, mime_type):
    """
    Method converts the encoded audio to base64 into a transcription using model "gpt-4o-mini-audio-preview"
    Parameters:
        encoded_string: base64 encoded audio form
        mime_type: mime_type of the recording
    
    Returns: 
        text: transcription of the audio
    
    """
    # getting the transcription of the audio through gpt-4o-mini-audio-preview
    completion = client.chat.completions.create(
    model="gpt-4o-mini-audio-preview",
    messages=[
            {
                "role": "user",
                "content": [
                    { 
                        "type": "text",
                        "text": "You are a transcription service. Please transcribe the following audio into text. \
                                Provide only the transcription, without any additional explanations or information."
                    },
                    {
                        "type": "input_audio",
                        "input_audio": {
                            "data": encoded_string,
                            "format": mime_type[1:]     #removing the dot from the mime type
                        }
                    }
                ]
            },
        ]
    )

    text = completion.choices[0].message.content
                    
    return text

def convert_audio_url(message: SinglePartMessage):
    """
    Convert a single part message with message_type "audio_url" to text and then feed it into chat 

    Uses: audio_transcription method to transcribe the audio 

    Parameter:
        message: a SinglePartMessage with message_type == "audio_url"
    
    Returns: 
        message_dict: a dictionary with following format
        {
            'type': 'text',
            'text': "...transcription..."
        }
    """
    url = message.get_message_value()['url']

    #Generating audio content from the url
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.HTTPError as errh: 
        print("HTTP Error") 
        print(errh.args[0]) 
    data = response.content

    #Converting the audio to base64 form
    encoded_string = base64.b64encode(data).decode('utf-8')

    # getting the transcription and converting it to text-based dictionary form for chat
    transcription = audio_transcription(encoded_string, message.get_message_value()['mime_type'])
    message_dict =  {
                        "type": "text",
                        "text": "Here is the audio transcription:\n" +transcription
                    }
                    
    return message_dict


def convert_audio_base64(message: SinglePartMessage):
    """
    Convert a single part message with message_type "audio_base64" to text and then feed it into chat 

    Uses: audio_transcription method to transcribe the audio 

    Parameter:
        message: a SinglePartMessage with message_type == "audio_base64"
    
    Returns: 
        message_dict: a dictionary with following format
        {
            'type': 'text',
            'text': "...transcription..."
        }
    """
    
    encoded_string = message.get_message_value()['audio_base64'].decode('utf-8')

    # getting the transcription and converting it to text-based dictionary form for chat
    transcription = audio_transcription(encoded_string, message.get_message_value()['mime_type'])
    message_dict =  {
                        "type": "text",
                        "text": "Here is the audio transcription:\n" +transcription
                    }
                    
    return message_dict

def convert_audio_bytesio(message: SinglePartMessage):
    """
    Convert a single part message with message_type "audio_bytesio" to text and then feed it into chat 

    Uses: audio_transcription method to transcribe the audio 

    Parameter:
        message: a SinglePartMessage with message_type == "audio_bytesio"
    
    Returns: 
        message_dict: a dictionary with following format
        {
            'type': 'text',
            'text': "...transcription..."
        }
    """
    
    #Converting the audio bytesio to base64 form
    encoded_string = base64.b64encode(message.get_message_value()['audio_bytesio']).decode('utf-8')

    # getting the transcription and converting it to text-based dictionary form for chat
    transcription = audio_transcription(encoded_string, message.get_message_value()['mime_type'])
    message_dict =  {
                        "type": "text",
                        "text": "Here is the audio transcription:\n" +transcription
                    }
                    
    return message_dict


def convert_single_part(message: SinglePartMessage):
    """
    Convert a single part message with different message_types to appropriate dictionary
    to be fed into chat
    Parameter:
        message: a SinglePartMessage 
    
    Returns: 
        message_dict: a dictionary with respective format of the message type
    """

    converted_message = None
    supported_types = ['text', 'image_url', 'image_base64', 'image_bytesio' 'file_url', 'file_base64', 'audio_url', 'audio_base64']
    

    #Given the message_type appropriate method is used to create the dictionary for the chat
    if message.get_message_type() == "text":
        converted_message = convert_text(message)
    elif message.get_message_type() == "image_url":
        converted_message = convert_image_url(message)
    elif message.get_message_type() == "image_base64":
        converted_message = convert_image_base64(message)
    elif message.get_message_type() == "image_bytesio":
        converted_message = convert_image_bytesio(message)
    elif message.get_message_type() == "file_url":
        converted_message = convert_file_url(message)
    elif message.get_message_type() == "file_base64":
        converted_message = convert_file_base64(message)
    elif message.get_message_type() == "file_bytesio":
        converted_message = convert_file_bytesio(message)
    elif message.get_message_type() == "audio_url":
        converted_message = convert_audio_url(message)
    elif message.get_message_type() == "audio_base64":
        converted_message = convert_audio_base64(message)
    elif message.get_message_type() == "audio_bytesio":
        converted_message = convert_audio_bytesio(message)
    else:
        # raising error if the file format is not supported
        
        raise ValueError(f"Unsupported file format: {message.get_message_type()}. Supported formats are: {', '.join(supported_types)}")
    

    return converted_message

def convert_multipart(message: MultiPartMessage):
    """
    Convert a multipart message that is a list of SinglePartMessage to a combined 
    dictionary to be fed into chat
    Parameter:
        message: a MultipartMessage 
    
    Returns: 
        message_dict: a dictionary with respective format of the message type
    """

    messages = message.get_message_list()
    converted_messages = []
    for message in messages:
        converted_message = convert_single_part(message)
        converted_messages.append(converted_message)
    
    return converted_messages