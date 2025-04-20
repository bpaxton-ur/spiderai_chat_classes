import requests
import io
import base64
import pdfplumber
import markdown
from bs4 import BeautifulSoup
from docx import Document
import json
import PyPDF2


def read_txt_from_bytesio(text_bytesio):
    """
    Reads a plain text file from a BytesIO object and returns its content.

    Args:
        text_bytesio (io.BytesIO): The BytesIO object containing the text content.

    Returns:
        str: The content of the text file, or an error message if failed.
    """
    try:
        # Read the text content from the BytesIO object
        text_content = text_bytesio.read().decode('utf-8')
        return text_content
    except Exception as e:
        return f"An error occurred: {e}"  # Return error message if there's an issue


def read_txt_from_url(text_url):
    """
    Reads a plain text file from a URL and returns its content.

    Args:
        text_url (str): The URL of the text file.

    Returns:
        str: The content of the text file, or an error message if failed.
    
    Raises:
        HTTPError: If the HTTP request to fetch the text file fails.
    """
    try:
        # Fetch the text file from the URL
        response = requests.get(text_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            return response.text
        else:
            return f"Failed to fetch data. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {e}"  # Return error message if there's an issue


def read_txt_from_base64(base64_string):
    """
    Reads a base64-encoded plain text string and returns its content.

    Args:
        base64_string (str): The base64-encoded text content.

    Returns:
        str: The decoded plain text content, or an error message if failed.
    """
    try:
        # Decode the base64 string into bytes and decode as UTF-8
        text_bytes = base64.b64decode(base64_string)
        text_content = text_bytes.decode('utf-8')

        return text_content  # Return the decoded text content
    except Exception as e:
        return f"An error occurred: {e}"  # Return error message if there's an issue


def read_pdf_from_bytesio(pdf_bytesio):
    """
    Reads a PDF file from a BytesIO object and extracts its text.

    Args:
        pdf_bytesio (io.BytesIO): The BytesIO object containing the PDF content.

    Returns:
        str: The extracted text from the PDF.
    """

    pdf_file = io.BytesIO(pdf_bytesio)

    # Create a PDF reader object from PyPDF2
    pdf_reader = PyPDF2.PdfReader(pdf_file)

    text = ""

    # Extract text from each page
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text() or ""  
    
    return text  # Return the extracted text


def read_pdf_from_url(pdf_url):
    """
    Reads a PDF file from a URL and extracts its text.

    Args:
        pdf_url (str): The URL of the PDF file.

    Returns:
        str: The extracted text from the PDF.
    
    Raises:
        HTTPError: If the HTTP request to fetch the PDF fails.
    """
    # Fetch the PDF file from the provided URL
    response = requests.get(pdf_url)
    response.raise_for_status()  # Raise error if the response was not successful

    # Create an in-memory file object from the PDF content
    pdf_file = io.BytesIO(response.content)
    return read_pdf_from_bytesio(pdf_file.getvalue())  # Use the BytesIO reader to extract text


def read_pdf_from_base64(pdf_base64):
    """
    Reads a PDF file from a base64-encoded string and extracts its text.

    Args:
        pdf_base64 (str): The base64-encoded PDF content.

    Returns:
        str: The extracted text from the PDF.
    """
    # Decode the base64-encoded string into bytes
    pdf_data = base64.b64decode(pdf_base64)
    pdf_file = io.BytesIO(pdf_data)

    return read_pdf_from_bytesio(pdf_file.getvalue())  # Use the BytesIO reader to extract text


############################################################
#       FILE TYPES BELOW REQUIRE TESTING
############################################################
   
def read_docx_from_bytesio(docx_bytesio):
    """
    Reads a DOCX file from a BytesIO object and extracts its text.

    Args:
        docx_bytesio (io.BytesIO): The BytesIO object containing the DOCX content.

    Returns:
        str: The extracted text from the DOCX file.
    """
    # Load the DOCX file from the BytesIO object
    doc = Document(docx_bytesio)

    # Extract text from all paragraphs in the DOCX file
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"

    return text  # Return the extracted text


def read_docx_from_base64(docx_base64):
    """
    Reads a DOCX file from a base64-encoded string and extracts its text.

    Args:
        docx_base64 (str): The base64-encoded DOCX content.

    Returns:
        str: The extracted text from the DOCX file.
    """
    # Decode the base64-encoded DOCX file and load it into memory
    docx_data = base64.b64decode(docx_base64)
    docx_file = io.BytesIO(docx_data)
    return read_docx_from_bytesio(docx_file)  # Use the BytesIO reader to extract text
 

def read_docx_from_url(docx_url):
    """
    Reads a DOCX file from a URL and extracts its text.

    Args:
        docx_url (str): The URL of the DOCX file.

    Returns:
        str: The extracted text from the DOCX file.
    
    Raises:
        HTTPError: If the HTTP request to fetch the DOCX file fails.
    """
    # Fetch the DOCX file from the URL
    response = requests.get(docx_url)
    response.raise_for_status()  # Raise error if the response was not successful

    # Create an in-memory file object from the DOCX content
    docx_file = io.BytesIO(response.content)
    return read_docx_from_bytesio(docx_file)  # Use the BytesIO reader to extract text
    

def read_markdown_from_bytesio(md_bytesio):
    """
    Reads a Markdown file from a BytesIO object, converts it to HTML, and extracts text.

    Args:
        md_bytesio (io.BytesIO): The BytesIO object containing the Markdown content.

    Returns:
        str: The plain text extracted from the Markdown content.
    """
    # Convert the Markdown content to HTML
    md_content = md_bytesio.read().decode('utf-8') 

    # Convert Markdown to HTML
    html_content = markdown.markdown(md_content)
    
    # Parse the HTML content and extract plain text
    soup = BeautifulSoup(html_content, 'html.parser')
    plain_text = soup.get_text()
    
    return plain_text 

def read_markdown_from_url(md_url):
    """
    Reads a Markdown file from a URL, converts it to HTML, and extracts text.

    Args:
        md_url (str): The URL of the Markdown file.

    Returns:
        str: The plain text extracted from the Markdown content.
    
    Raises:
        HTTPError: If the HTTP request to fetch the Markdown file fails.
    """
    # Fetch the Markdown file from the URL
    response = requests.get(md_url)
    response.raise_for_status()  # Raise error if the response was not successful
    
    # Convert the Markdown content to HTML
    html = markdown.markdown(response.text)

    # Use BeautifulSoup to extract text from the HTML
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()

    return text  # Return the extracted text


def read_markdown_from_base64(md_base64):
    """
    Reads a base64-encoded Markdown string and returns its plain text.

    Args:
        md_base64 (str): The base64-encoded Markdown content.

    Returns:
        str: The decoded plain text of the Markdown file.
    """
    # Decode the base64 string to get the Markdown content
    markdown_bytes = base64.b64decode(md_base64)
    markdown_content = markdown_bytes.decode('utf-8')

    return markdown_content  # Return the decoded Markdown content



def read_json_from_bytesio(json_bytesio):
    """
    Reads a JSON file from a BytesIO object and returns it as a formatted string.

    Args:
        json_bytesio (io.BytesIO): The BytesIO object containing the JSON content.

    Returns:
        str: The formatted JSON string, or an error message if failed.
    """
    try:
        # Read the JSON content from the BytesIO object
        json_text = json_bytesio.read().decode('utf-8')

        # Parse and format the JSON data
        json_data = json.loads(json_text)
        formatted_json_text = json.dumps(json_data, indent=4)
        
        return formatted_json_text
    except Exception as e:
        return f"An error occurred: {e}"  # Return error message if there's an issue


def read_json_from_url(json_url):
    """
    Reads a JSON file from a URL and returns it as a formatted string.

    Args:
        json_url (str): The URL of the JSON file.

    Returns:
        str: The formatted JSON string, or an error message if failed.
    
    Raises:
        HTTPError: If the HTTP request to fetch the JSON file fails.
    """
    try:
        # Fetch the JSON file from the URL
        response = requests.get(json_url)
        
        # Check if the request was successful
        if response.status_code == 200:
            json_data = response.json()  # Parse JSON content
            json_text = json.dumps(json_data, indent=4)  # Format JSON as a string
            return json_text
        else:
            return f"Failed to fetch data. Status code: {response.status_code}"
    except Exception as e:
        return f"An error occurred: {e}"  # Return error message if there's an issue


def read_json_from_base64(base64_string):
    """
    Reads a base64-encoded JSON string and returns it as a formatted string.

    Args:
        base64_string (str): The base64-encoded JSON string.

    Returns:
        str: The formatted JSON string, or an error message if failed.
    """
    try:
        # Decode the base64 string into bytes and then decode as a UTF-8 string
        json_bytes = base64.b64decode(base64_string)
        json_text = json_bytes.decode('utf-8')

        # Parse and format the JSON data
        json_data = json.loads(json_text)
        formatted_json_text = json.dumps(json_data, indent=4)
        
        return formatted_json_text
    except Exception as e:
        return f"An error occurred: {e}"  # Return error message if there's an issue

