from datetime import datetime
from io import BytesIO
from message import BaseMessageClass

def get_display_info(message : BaseMessageClass):
    """Get display informations for a message

    Args:
        message (BaseMessageClass): The message to extract information from

    Returns: tuple of
        author (str): The author of the message
        author_type (str) : The author type
        display_datetime (str) : Time to display
    """
    author = message.get_author()
    author_type = message.get_author_type()
    display_datetime = datetime.fromtimestamp(message.get_updated_at()).strftime("%H:%M:%S %m-%d-%Y")

    return author, author_type, display_datetime

def write_text_to_st(message, st, include_datetime: bool = True):
    """
    Print a text message on the screen with streamlit
    
    Returns:
        None
    """     
    # Get the information
    author, author_type, display_datetime = get_display_info(message)

    # Display the content
    display_value = message.get_message_value_attribute("text")
    if include_datetime:
        st.write(f"{author} ({author_type}):\n{display_value}\n{display_datetime}\n")
    else:
        st.write(f"{author} ({author_type}):\n{display_value}\n")