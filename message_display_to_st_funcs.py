from datetime import datetime
from message import SinglePartMessage

def get_display_info(message: SinglePartMessage):
    """Get display informations for a message

    Args:
        message (SinglePartMessage): The message to extract information from

    Returns: tuple of
        author (str): The author of the message
        author_type (str) : The author type
        display_datetime (str) : Time to display
    """
    author = message.get_author()
    author_type = message.get_author_type()
    display_datetime = datetime.fromtimestamp(message.get_updated_at()).strftime("%H:%M:%S %m-%d-%Y")

    return author, author_type, display_datetime

def write_display_info(st, display_info, include_datetime: bool = True):
    author, author_type, display_datetime = display_info
    if include_datetime:
        st.write(f"{author} ({author_type}):\n{display_datetime}")
    else:
        st.write(f"{author} ({author_type})")

def write_single_chat_to_st(message: SinglePartMessage, st, include_datetime: bool = True):
    """Write a single part message to streamlit

    Args:
        message (SinglePartMessage): Message object, Single
        st (_type_): Streamlit
        include_datetime (bool, optional): _description_. Defaults to True.

    Raises:
        ValueError: If message type is invalid
    """
    display_info = get_display_info(message)
    author, author_type, display_datetime = display_info
    write_display_info(st, display_info, include_datetime)
    
    with st.chat_message(author_type):
        message_type = message.get_message_type()
        if message_type == "text":
            text = message.get_message_value_by_attribute("text")
            st.write(text)
        elif message_type == "image_base64" or message_type == "image_url":
            filename = message.get_message_value_by_attribute("filename")
            if message_type == "image_base64":
                image_data = message.get_message_value_by_attribute("image_base64")
            else:
                image_data = message.get_message_value_by_attribute("url")
            st.image(image_data, caption=filename, use_container_width=True)
        elif message_type == "file_base64" or message_type == "file_url":
            filename = message.get_message_value_by_attribute("filename")
            mime_type = message.get_message_value_by_attribute("mime_type")
            if message_type == "file_base64":
                file_data = message.get_message_value_by_attribute("file_base64")
            else:
                file_data = message.get_message_value_by_attribute("url")
            st.download_button(label=f"Download {filename}", data=file_data, file_name=filename, mime=mime_type)
        elif message_type == "audio_base64" or message_type == "audio_url":
            if message_type == "audio_base64":
                audio_data = message.get_message_value_by_attribute("audio_base64")
            else:
                audio_data = message.get_message_value_by_attribute("url")
            st.audio(data=audio_data)
        else:
            raise ValueError("Invalid Message Type")