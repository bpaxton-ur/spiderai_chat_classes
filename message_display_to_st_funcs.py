from datetime import datetime
from message import SinglePartMessage, MultiPartMessage
import random
import helper_functions as hf
import base64

def get_display_info(message):
    """Get display informations for a message
    """
    author = message.get_author()
    author_type = message.get_author_type()
    display_datetime = datetime.fromtimestamp(message.get_updated_at()).strftime("%H:%M:%S %m-%d-%Y")

    return author, author_type, display_datetime

def write_display_info(st, display_info, include_datetime: bool = True):
    """Write author info and optional datetime to streamlit
    """
    author, author_type, display_datetime = display_info
    if include_datetime:
        st.write(f"{author} ({author_type}):\n{display_datetime}")
    else:
        st.write(f"{author} ({author_type})")

def write_single_chat_to_st(message, st, include_datetime: bool = True):
    """Write a single part message to Streamlit as its original element.

    Args:
        message (SinglePartMessage): Message object, Single
        st (_type_): Streamlit
        include_datetime (bool, optional): Defaults to True.

    Raises:
        ValueError: If message type is invalid
    """
    message_type = message.get_message_type()

    # Text message type
    if message_type == "text":
        text = message.get_message_value_by_attribute("text")
        st.write(text)

    # Image message type
    elif message_type in ["image_base64", "image_url"]:
        filename = message.get_message_value_by_attribute("filename")
        image_data = message.get_message_value_by_attribute("image_base64") if message_type == "image_base64" else message.get_message_value_by_attribute("url")
        st.image(image_data, caption=filename, use_container_width=True)

    # File message type (Enable preview + Open in New Tab)
    elif message_type in ["file_base64", "file_url"]:
        filename = message.get_message_value_by_attribute("filename")
        mime_type = message.get_message_value_by_attribute("mime_type")
        
        if message_type == "file_base64":
            file_bytes = message.get_message_value_by_attribute("file_base64")
            file_url = f"data:{mime_type};base64,{file_bytes}"
        else:
            file_data = message.get_message_value_by_attribute("url")
            file_url = file_data  # Direct URL

        # Download button
        st.download_button(
            key=random.randint(1, 10000),
            label=f"Download {filename}",
            data=file_bytes if message_type == "file_base64" else file_data,
            file_name=filename,
            mime=mime_type,
        )

        # File preview (for PDFs & images)
        if mime_type.startswith("image/") or mime_type == "application/pdf":
            st.markdown(f"""
                <iframe src="{file_url}" width="100%" height="500px"></iframe>
            """, unsafe_allow_html=True)

        # Open in new tab option
        st.markdown(f"""
            <a href="{file_url}" target="_blank">🔗 Preview {filename}</a>
        """, unsafe_allow_html=True)

    # Audio message type
    elif message_type in ["audio_base64", "audio_url"]:
        audio_data = message.get_message_value_by_attribute("audio_base64") if message_type == "audio_base64" else message.get_message_value_by_attribute("url")
        st.audio(data=audio_data)

    # Raise error
    else:
        raise ValueError("Invalid Message Type")
        
def write_chat_to_st(message, st, include_datetime: bool = True):
    """Generic display function that can work for both message types

    Args:
        message (SinglePartMessage / MultiPartMessage): The message to be displayed
        st (_type_): Streamlit
        include_datetime (bool, optional): Defaults to True.
    """
    display_info = get_display_info(message)
    author, author_type, display_datetime = display_info

    with st.chat_message(author_type):
        write_display_info(st, display_info, include_datetime)
        if hf.validate_type(message, SinglePartMessage):
            write_single_chat_to_st(message, st, include_datetime)
        else:
            for mes in message.get_message_list():
                write_single_chat_to_st(mes, st, include_datetime)