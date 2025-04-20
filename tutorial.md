---markdown file starts here---
# 🧠 Chat System User Guide

This markdown file documents how to use the chat system provided in the Python codebase. It supports multimodal input including text, images, PDFs, audio files, and more.

---

## 📦 Setup

```python
from chat import Chat
from message import SinglePartMessage
import implementation_helper as helper
import get_chat_input

#Note: Your get_chat_input should have access to the API.
```

---

## 💬 Text Interaction

```python
# Creating a chat instance
chat = Chat(title="Simple Chat")

# Adding a text message to the chat instance
chat.append_message_chunk_by_attribute(
    author="Alice",
    author_type="human",
    message_type="text",
    message_chunk_by_attribute="Write a poem about the ocean.",
    key="text"
)

# Generating response using the API
get_chat_input.generate_response(chat)

# Note: At this point your chat is automatically updated with the new messages from chat-gpt.
# Look at the code below to learn how to visualize the messages of the chat
```

---

## 🖼️ Working with Images

### Image from URL

```python
# Another way to append message to chat is by first creating an instance SinglePartMessage
message_image = SinglePartMessage.create_message("Alice", "human", "image_url")
message_image.set_message_value_by_attribute("https://example.com/image.jpeg", key="url")
chat.append_message(message_image)
```

### Image from BytesIO

```python
chat.append_message_chunk_by_attribute(
    author="Alice",
    author_type="human",
    message_type="image_bytesio",
    message_chunk_by_attribute=helper.image_bytesio,
    key="image_bytesio"
)
```

### Image from Base64

```python
chat.append_message_chunk_by_attribute(
    author="Alice",
    author_type="human",
    message_type="image_base64",
    message_chunk_by_attribute=helper.image_base64,
    key="image_base64"
)
```

Note: All messages must be added using either `append_message()` or `append_message_chunk_by_attribute()`.

---

## 📄 PDF Handling

### From URL

```python
message_pdf_url = SinglePartMessage.create_message("Alice", "human", "file_url")
message_pdf_url.set_message_value_by_attribute("https://example.com/sample.pdf", key="url")
message_pdf_url.set_message_value_by_attribute(".pdf", key="mime_type")
chat.append_message(message_pdf_url)
```

### From BytesIO

```python
message_pdf_bytesio = SinglePartMessage.create_message("Alice", "human", "file_bytesio")
message_pdf_bytesio.set_message_value_by_attribute(helper.pdf_bytesio, key="file_bytesio")
message_pdf_bytesio.set_message_value_by_attribute(".pdf", key="mime_type")
chat.append_message(message_pdf_bytesio)
```

### From Base64

```python
message_pdf_base64 = SinglePartMessage.create_message("Alice", "human", "file_base64")
message_pdf_base64.set_message_value_by_attribute(helper.pdf_base64, key="file_base64")
message_pdf_base64.set_message_value_by_attribute(".pdf", key="mime_type")
chat.append_message(message_pdf_base64)
```

---

## 📝 Text File Handling

### From URL

```python
message_txt_url = SinglePartMessage.create_message("Alice", "human", "file_url")
message_txt_url.set_message_value_by_attribute(helper.text_url, key="url")
message_txt_url.set_message_value_by_attribute(".txt", key="mime_type")
chat.append_message(message_txt_url)
```

### From BytesIO

```python
message_txt_bytes = SinglePartMessage.create_message("Alice", "human", "file_bytesio")
message_txt_bytes.set_message_value_by_attribute(helper.text_bytes_io, key="file_bytesio")
message_txt_bytes.set_message_value_by_attribute(".txt", key="mime_type")
chat.append_message(message_txt_bytes)
```

### From Base64

```python
message_txt_base64 = SinglePartMessage.create_message("Alice", "human", "file_base64")
message_txt_base64.set_message_value_by_attribute(helper.text_base64_content, key="file_base64")
message_txt_base64.set_message_value_by_attribute(".txt", key="mime_type")
chat.append_message(message_txt_base64)
```

Note: You can similarly work with other file formats: docs, md and json. But they have not been thoroughly tested yet. Check out the implementation at `convert_file_to_text.py`. File-types to work for future can be csv and pptx. 

---

## 🔊 Audio Handling
The way audio handling actually works is the audio is transcribed using a model. More details on `convert_messages_to_dict.py`. And the transcription is fed into the chat as text values. This is similar to how the file handling works.  

### From URL

```python
audio_msg = SinglePartMessage.create_message("Alice", "human", "audio_url")
audio_msg.set_message_value_by_attribute("https://example.com/audio.mp3", key="url")
audio_msg.set_message_value_by_attribute(".mp3", key="mime_type")
chat.append_message(audio_msg)
```

### From BytesIO

```python
audio_bytes_msg = SinglePartMessage.create_message("Alice", "human", "audio_bytesio")
audio_bytes_msg.set_message_value_by_attribute(helper.audio_bytesio, key="audio_bytesio")
audio_bytes_msg.set_message_value_by_attribute(".mp3", key="mime_type")
chat.append_message(audio_bytes_msg)
```

### From Base64

```python
audio_b64_msg = SinglePartMessage.create_message("Alice", "human", "audio_base64")
audio_b64_msg.set_message_value_by_attribute(helper.audio_base64, key="audio_base64")
audio_b64_msg.set_message_value_by_attribute(".mp3", key="mime_type")
chat.append_message(audio_b64_msg)
```

---

## 🌊 Streaming Mode
It is currently not working. Under maintenance.
```python
stream_chat = Chat(title="Stream Chat")
stream_chat.append_message_chunk_by_attribute(
    author="Alice",
    author_type="human",
    message_type="text",
    message_chunk_by_attribute="Tell me a story about dragons.",
    key="text"
)

get_chat_input.generate_response(stream_chat, stream=True)
```

---

## 🖨️ Displaying the Chat Messages

```python
def print_message(messages):
    if messages.get_message_type() == "multipart":
        for msg in messages.get_message_list():
            print_message(msg)
    else:
        print("="*50)
        print("New Message Type:", messages.get_message_type())
        for key, val in messages.get_message_value().items():
            print(f"{key}: {val[:100]}..." if isinstance(val, str) and len(val) > 100 else f"{key}: {val}")
        print("Author:", messages.get_author())
        print("Author Type:", messages.get_author_type())

def display_chat_messages(chat: Chat):
    for msg in chat.get_messages():
        print_message(msg)
```

---
Happy coding! 🎉
