import streamlit as st
import message_display_to_st_funcs as mdf
from datetime import datetime
from message import SinglePartMessage
from io import BytesIO
import base64

def get_image_bytes(image_path):
    """
    Reads an image file and returns its content as bytes.

    Args:
        image_path (str): The path to the image file.

    Returns:
        bytes: The content of the image file as bytes, or None if an error occurs.
    """
    try:
        with open(image_path, "rb") as file:
            image_bytes = file.read()
        return image_bytes
    except FileNotFoundError:
        print(f"Error: File not found at path: {image_path}")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def app():
    st.title("Display Test")

    #--------------------------------
    st.subheader("Text Display Test")

    # Message instance
    text_message = SinglePartMessage.create_message(
        author="Sam",
        author_type="human",
        message_type="text",
        message_value={"text": "Hello World"},
    )
    
    # Call display function
    mdf.write_text_to_st(text_message, st)

    #--------------------------------
    st.subheader("Image Display Test")

    st.write("Base 64")

    image_b64_message = SinglePartMessage.create_message(
        author="Sam",
        author_type="human",
        message_type="image_base64",
        message_value={
            "filename": "test_image.png",
            "image_base64": get_image_bytes("tests/test_image.png"),
            "mime_type": "image/png"
        },
    )

    mdf.write_image_to_st(image_b64_message, st)

    st.write("URL")

    image_url_message = SinglePartMessage.create_message(
        author="Sam",
        author_type="human",
        message_type="image_url",
        message_value={
            "filename": "test_image_url",
            "url": "https://pethelpful.com/.image/w_3840,q_auto:good,c_fill,ar_4:3/MTk2Nzg5NTQzNDM1NzcyOTkw/cat-got-your-tongue-common-and-cute-cat-expressions.jpg",
            "mime_type": "image/png"
        },
    )

    mdf.write_image_to_st(image_url_message, st)

if __name__ == "__main__":
    app()
