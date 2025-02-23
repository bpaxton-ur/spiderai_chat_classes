import base64
from datetime import datetime
from io import BytesIO
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

def write_text_to_st(message: SinglePartMessage, st, include_datetime: bool = True):
    """
    Print a text message on the screen with Streamlit
    
    Returns:
        None
    """     
    # Get the information
    author, author_type, display_datetime = get_display_info(message)

    # Display the content
    display_value = message.get_message_value_by_attribute("text")
    if include_datetime:
        st.write(f"{author} ({author_type}):\n{display_value}\n{display_datetime}\n")
    else:
        st.write(f"{author} ({author_type}):\n{display_value}\n")

def write_image_to_st(message: SinglePartMessage, st, include_datetime: bool = True):
    """
    Display an image message from base64 data on Streamlit

    Returns:
        None
    """
    # Get the information
    author, author_type, display_datetime = get_display_info(message)
    
    # Get the image data
    if message.get_message_type() == "image_base64":
        image_data = message.get_message_value_by_attribute("image_base64")
    elif message.get_message_type() == "image_url":
        image_data = message.get_message_value_by_attribute("url")
    else:
        raise ValueError("Error parsing message type: image_base64 or image_url only")
    filename = message.get_message_value_by_attribute("filename")

    # Display the content
    if include_datetime:
        st.write(f"{author} ({author_type}):\n{display_datetime}")
    else:
        st.write(f"{author} ({author_type})")
    st.image(image_data, caption=filename, use_container_width=True)