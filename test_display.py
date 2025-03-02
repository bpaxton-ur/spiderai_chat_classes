import streamlit as st
import message_display_to_st_funcs as mdf
from message import SinglePartMessage

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
    st.title("Display Test App")

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
    mdf.write_chat_to_st(text_message, st)

    #--------------------------------
    st.subheader("Image Display Test")

    st.write("Base 64")

    image_b64_message = SinglePartMessage.create_message(
        author="Maru",
        author_type="human",
        message_type="image_base64",
        message_value={
            "filename": "maru_cat",
            "image_base64": get_image_bytes("tests/maru_cat.jpg"),
            "mime_type": "image/jpg"
        },
    )

    mdf.write_chat_to_st(image_b64_message, st)

    st.write("URL")

    image_url_message = SinglePartMessage.create_message(
        author="Maru",
        author_type="human",
        message_type="image_url",
        message_value={
            "filename": "marumogu",
            "url": "https://i0.wp.com/cutetropolis.com/wp-content/uploads/2024/01/vW0vwzu__co.jpg?fit=1200%2C675&ssl=1",
            "mime_type": "image/jpg"
        },
    )

    mdf.write_chat_to_st(image_url_message, st)

    #--------------------------------
    st.subheader("File Display Test")

    st.write("Base 64")

    file_b64_message = SinglePartMessage.create_message(
        author="Maru",
        author_type="human",
        message_type="file_base64",
        message_value={
            "filename": "maru_cat.txt",
            "file_base64": get_image_bytes("tests/maru_cat.txt"),
            "mime_type": "text/plain"
        },
    )

    mdf.write_chat_to_st(file_b64_message, st)

    st.write("URL")

    file_url_message = SinglePartMessage.create_message(
        author="Maru",
        author_type="human",
        message_type="file_url",
        message_value={
            "filename": "marumogu",
            "url": "https://catsoftheweb.com/wp-content/uploads/2024/08/maru-cat.jpeg.webp",
            "mime_type": "image/jpg"
        },
    )

    mdf.write_chat_to_st(file_url_message, st)

    #--------------------------------
    st.subheader("Audio Display Test")

    audio_b64_message = SinglePartMessage.create_message(
        author="Maru",
        author_type="human",
        message_type="audio_base64",
        message_value={
            "filename": "test_audio.mp3",
            "audio_base64": get_image_bytes("tests/test_audio.mp3"),
            "mime_type": "audio/mpeg"
        },
    )

    mdf.write_chat_to_st(audio_b64_message, st)

if __name__ == "__main__":
    app()
