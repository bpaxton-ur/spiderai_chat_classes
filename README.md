# SpiderAI Chat Classes

This repository contains the implementation and resources for the **SpiderAI Chat Classes** project, developed as part of AI research at the University of Richmond.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [File Descriptions](#file-descriptions)

## Overview
The SpiderAI Chat Classes project focuses on building intelligent chat-based systems for educational purposes. It leverages advanced AI techniques to create interactive and adaptive learning experiences.

## Features
- AI-powered chat interactions.
- Modular and extensible architecture.
- Support for multiple class types and topics.
- Easy integration with other systems.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/spiderai_chat_classes.git
    ```
2. Navigate to the project directory:
    ```bash
    cd spiderai_chat_classes
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```


## File Descriptions

### Core Files
- **`chat.py`**: Implements the `Chat` class, which represents a chat session. It manages messages, metadata, and developer instructions. It interacts with `SinglePartMessage` and `MultiPartMessage` from `message.py`.
- **`message.py`**: Contains the `BaseMessageClass` and its derived classes `SinglePartMessage` and `MultiPartMessage`. These classes represent individual messages and multipart messages in a chat.
- **`message_types.py`**: Defines the structure and attributes of different message types (e.g., text, image, audio). Used by `message.py` to validate message content.

### Utility Files
- **`convert_file_to_text.py`**: Provides functions to extract text from various file formats (e.g., PDF, DOCX, Markdown, JSON) using URLs or base64-encoded content.
- **`convert_messages_to_dict.py`**: Converts `SinglePartMessage` and `MultiPartMessage` objects into dictionaries suitable for feeding into the chat system. 'MulitPartMessage' are a list of 'SinglePartMessage' and 'SinglePartMessage' consists of 
- **`get_chat_input.py`**: Handles the interaction with the OpenAI API. Converts chat messages into the required format, sends them to the model, and processes the responses. The method `generate_response(chat: Chat, stream: bool)` is the main method in the file that either returns a Chat or returns a yield value which adds additional information from the stream in each iteration. The model that we use to generate such response will have to be amended within the file. At the moment, it is hard-coded to 'gpt-o4'
- **`helper_functions.py`**: Contains utility functions, such as timestamp formatting and type validation, used across the project.

### Display and Testing
- **`message_display_to_st_funcs.py`**: Provides functions to display messages (text, images, files, audio) in a Streamlit application.
- **`test_display.py`**: A Streamlit app for testing the display of different message types using `message_display_to_st_funcs.py`.

### Data and Examples
- **`chatCompletion_vs_response.txt`**: Ignored by `.gitignore`. Likely used for storing temporary or experimental data.
- **`tests/maru_cat.txt`**: A sample text file used for testing file-related functionality.

### Documentation
- **`README.md`**: Provides an overview of the project, installation instructions, usage guidelines, and file descriptions.
