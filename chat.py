"""
utils/chat_utils/chat.py

This file contains the chat class.

Author: M. Saif Mehkari
Version: 1.0
License Info: See license.txt file
"""

#
# Import the correct packages
#
from pydantic import BaseModel, Field
from typing import Union, Any
from datetime import datetime
from message import SinglePartMessage, MultiPartMessage

#
# Main Chat class
#
class Chat(BaseModel, validate_assignment=True):
    """
    A class to represent a chat. A chat contains a list of chat messages (order matters).

    Attributes:
        title: str: An optional title for the chat. The default is an empty string.
        messages: list[Union[SinglePartMessage, MultiPartMessage]]: A list of all the chat messages in order.
        developer_instructions: str: The developers instructions for how the model should work.
        developer_files: list[dict]: The list of files provided by the developer. Each file must be of the type {"url": url of file} or {"base64": bytes}
        metadata: dict: Any meta data associated with the chat.
        created_at: float: The timestamp the chat was created. 
        updated_at: float: The timestamp the chat message was last updated. 

    Public Instance Methods:
        get_title() -> str        
        get_messages() -> list[Union[SinglePartMessage, MultiPartMessage]]
        get_message_type_list() -> list[str]
        get_developer_instructions() -> str
        get_developer_files() -> list[dict]
        get_metadata() -> dict
        get_metadata_attribute(key: str) -> Any            
        get_created_at() -> float
        get_updated_at() -> float
        to_dict() -> dict

        update_updated_at() -> None

        set_developer_instructions(developer_instructions: str) -> None
        set_developer_files(developer_files: list[dict]) -> None        
        set_metadata(metadata: dict) -> None               
        set_metadata_attribute(attribute_metadata: Any, key: str) -> None               

        append_message(message: Union[SinglePartMessage, MultiPartMessage]) -> None
        append_message_chunk(author: str, author_type: str, message_type: str, message_chunk: dict) -> None
        append_message_chunk_by_attribute(author: str, author_type: str, message_type: str, message_chunk_by_attribute: Any, key: str) -> None
        append_developer_files(developer_file: dict) -> None

    Public Class Method:
        from_dict() -> dict        
    """
    #
    # Attributes:
    #
    title: str = Field(default = "", description = "An optional title for the chat. The default is an empty string.", frozen = True)
    messages: list[Union[SinglePartMessage, MultiPartMessage]] = Field(default_factory=lambda: list(), description = "A list of all the chat messages in order.", validate_assignment=True)
    developer_instructions: str = Field(default="", description = "The developers instructions for how the model should work.", validate_assignment=True)
    developer_files: list[dict] = Field(default_factory=lambda: list(), description = 'The list of files provided by the developer. Each file must be of the type {"url": url of file} or {"base64": bytes}', validate_assignment=True)
    metadata: dict = Field(default_factory = lambda: dict(), description = "Any meta data associated with the chat.") 
    created_at: float = Field(default_factory=lambda: datetime.now().timestamp(), description = "The timestamp the chat was created.", frozen = True)
    updated_at: float = Field(default_factory= lambda: datetime.now().timestamp(), description = "The timestamp the chat was last updated.")

    #
    # Public Instance Methods:
    #
    def get_title(self) -> str:
        """
        Getter for title.
        
        Returns:
            title: str: The title for chat. The default is an empty string.
        """        
        return self.title

    def get_messages(self) -> list[Union[SinglePartMessage, MultiPartMessage]]:
        """
        Getter for messages.
        
        Returns:
            messages: list[Union[SinglePartMessage, MultiPartMessage]]: A list of all the chat messages in order.
        """        
        return self.messages
    
    def get_message_type_list(self) -> list[str]:
        """
        Generates a list of all the types in chat (including within the multipart messages)

        Returns:
            message_type_list: list[str]: A list of all the types in the chat (including within the multipart messages)
        """

        # Get all the types
        message_type_list_int = []
        for message in self.messages:
            if message.get_message_type() == "multipart":
                message_type_list_int = message_type_list_int + message.get_message_type_list() + ["multipart"]
            else:
                message_type_list_int.append(message.get_message_type())

        # Make the list unique
        message_type_list = list(set(message_type_list_int))

        return message_type_list    

    def get_developer_instructions(self) -> str:
        """
        Getter for developer instructionss.
        
        Returns:
            developer_instructions: str: The developers instructions for how the model should work.
        """        
        return self.developer_instructions

    def get_developer_files(self) -> list[dict]:
        """
        Getter for developer files.
        
        Returns:
            developer_files: list[dict]: The list of files provided by the developer. Each file must be of the type {"url": url of file} or {"base64": bytes}
        """        
        return self.developer_files

    def get_metadata(self) -> dict:
        """
        Getter for metadata.

        Returns:
            metadata: dict: Any meta data associated with the chat
        """        
        return self.metadata
        
    def get_metadata_attribute(self, key: str) -> Any:
        """
        Getter for metadata attribute
        
        Args:
            key: str: The key to get from the metadata.

        Returns:
            metadata: Any: Meta data associated with the key.
        """        
        return self.metadata[key]        
    
    def get_created_at(self) -> float:
        """
        Getter for creation timestamp.
        
        Returns:
            created_at_timestamp: float: The timestamp the chat was created.
        """        
        return self.created_at

    def get_updated_at(self) -> float:
        """
        Getter for last updated timestamp.
        
        Returns:
            updated_at_timestamp: float: The timestamp the chat was last updated.
        """        
        return self.updated_at

    def to_dict(self) -> dict:
        """
        Serialize the object instance
        
        Returns:
            serializedObject: dict: The serialized version of the object
        """        
        return self.model_dump()
    
    def update_updated_at(self) -> None:
        """
        Updates the updated at time
        
        Returns:
            None
        """        
        self.updated_at = datetime.now().timestamp()
        return None            

    def set_developer_instructions(self, developer_instructions: str) -> None:
        """
        Setter for developer instructionss.
        
        Args:
            developer_instructions: str: The developers instructions for how the model should work.

        Returns:
            None
        """        
        self.developer_instructions = developer_instructions
        self.update_updated_at()

        return None

    def set_developer_files(self, developer_files: list[dict]) -> None:
        """
        Setter for developer files.
        
        Args:
            developer_files: list[dict]: The list of files provided by the developer. Each file must be of the type {"url": url of file} or {"base64": bytes}

        Returns:
            None            
        """        
        self.developer_files = developer_files
        self.update_updated_at()

        return None
    
    def set_metadata(self, metadata: dict) -> None:
        """
        Setter for metadata.
        
        Args:
            data: dict: Any meta data associated with the chat

        Returns:
            None
        """        
        self.metadata = metadata
        self.update_updated_at()

        return None            
    
    def set_metadata_attribute(self, attribute_metadata: Any, key: str) -> None:
        """
        Setter for metadata.
        
        Args:
            data: Any: Meta data associated with the chat for a particular key.
            key: str: The key to set from the metadata.

        Returns:
            None
        """        
        self.metadata[key] = attribute_metadata            
        self.update_updated_at()

        return None                
    
    def append_message(self, message: Union[SinglePartMessage, MultiPartMessage]) -> None: 
        """
        Add a message to the messages list, including multipart if from the same author/author_type.

        Args:
            message: Union[SinglePartMessage, MultiPartMessage]: The value of the message.
        
        Returns:
            None
        """                

        # If no messages or new author/author_type then add to the message list 
        if (len(self.messages) == 0) or (message.get_author() != self.messages[-1].get_author()) and (message.get_author_type() != self.messages[-1].get_author_type()):
            self.messages.append(message)
        
        # Else add to a multipart message
        else:
            # If multipart already exists, augment it
            if self.messages[-1].get_message_type() == "multipart":
                self.messages[-1].append_message(message = message)

            # Else create a multipart and augment it
            else:
                new_message = MultiPartMessage.create_message(author = message.get_author(), author_type = message.get_author_type(), message_list = [self.messages[-1], message])
                self.messages[-1] = new_message
            

        self.update_updated_at()

        return None
   
    def append_message_chunk(self, author: str, author_type: str, message_type: str, message_chunk: dict) -> None:
        """
        Augment the message list with the provided message chunk.

        Args:
            author: str: The author of the message.
            author_type: Literal["genai", "human", "developer"]: The author type can be a genai, human, or developer.
            message_type: str: The type of the message which should always be one of the SinglePartMessage types.
            message_chunk: Any: Chunk to augment the message dict by.
            start_new_message: bool: Should a new message be started      

        Returns:
            None
        """                

        # If no messages or new author/author_type then add to the message list 
        if (len(self.messages) == 0) or (author != self.messages[-1].get_author()) or (author_type != self.messages[-1].get_author_type()):
            message = SinglePartMessage.create_message(author = author, author_type = author_type, message_type = message_type, message_value = message_chunk)
            self.messages.append(message)     

        # If the author is the same and author_type is the same
        elif (author == self.messages[-1].get_author()) and (author_type == self.messages[-1].get_author_type()):
            
            # Then if message type is the same then you just augment the message
            if (message_type == self.messages[-1].get_message_type()):
                self.messages[-1].append_message_chunk(message_chunk = message_chunk)

            # Then if the previous message type is not same (but not multipart) then you create a multipart message and add this
            elif ("multipart" != self.messages[-1].get_message_type()):
                new_message1 = SinglePartMessage.create_message(author = author, author_type = author_type, message_type = message_type, message_value = message_chunk)
                new_message2 = MultiPartMessage.create_message(author = author, author_type = author_type, message_list = [self.messages[-1], new_message1])
                self.messages[-1] = new_message2

            # Then if the previous message type is not same (but multipart) then you augment the multipart message
            elif ("multipart" == self.messages[-1].get_message_type()):
                self.messages[-1].append_message_chunk(message_type = message_type, message_chunk = message_chunk)     

        self.update_updated_at()

        return None
    
    def append_message_chunk_by_attribute(self, author: str, author_type: str, message_type: str, message_chunk_by_attribute: dict, key: str) -> None:
        """
        Augment the message list with the provided message chunk attribute.

        Args:
            author: str: The author of the message.
            author_type: Literal["genai", "human", "developer"]: The author type can be a genai, human, or developer.
            message_type: str: The type of the message which should always be one of the SinglePartMessage types.
            message_chunk_by_attribute: Any: Chunk to augment the message value attribute by.
            key: str: The key to set the message value. 
            start_new_message: bool: Should a new message be started      

        Returns:
            None
        """                

        # If no messages or new author/author_type then add to the message list (we will create an empty message and augment)
        if (len(self.messages) == 0) or (author != self.messages[-1].get_author()) or (author_type != self.messages[-1].get_author_type()):
            message = SinglePartMessage.create_empty_message(author = author, author_type = author_type, message_type = message_type)
            message.append_message_chunk_by_attribute(message_value_by_attribute = message_chunk_by_attribute, key = key)
            self.messages.append(message)     

        # If the author is the same and author_type is the same
        elif (author == self.messages[-1].get_author()) and (author_type == self.messages[-1].get_author_type()):
            
            # Then if message type is the same then you just augment the message
            if (message_type == self.messages[-1].get_message_type()):
                self.messages[-1].append_message_chunk_by_attribute(message_value_by_attribute = message_chunk_by_attribute, key = key)

            # Then if the previous message type is not same (but not multipart) then you create a multipart message and add this (we will create an empty message and augment)
            elif ("multipart" != self.messages[-1].get_message_type()):
                new_message1 = SinglePartMessage.create_empty_message(author = author, author_type = author_type, message_type = message_type)
                new_message1.append_message_chunk_by_attribute(message_value_by_attribute = message_chunk_by_attribute, key = key)                
                new_message2 = MultiPartMessage.create_message(author = author, author_type = author_type, message_list = [self.messages[-1], new_message1])
                self.messages[-1] = new_message2

            # Then if the previous message type is not same (but multipart) then you augment the multipart message
            elif ("multipart" == self.messages[-1].get_message_type()):
                self.messages[-1].append_message_chunk_by_attribute(message_type = message_type, message_value_by_attribute = message_chunk_by_attribute)     

        # Update the time
        self.update_updated_at()

        return None    

    def append_developer_files(self, developer_file: dict) -> None:
        """
        Augment the list of developer files.
        
        Args:
            developer_file: dict: The file must be of the type {"url": url of file} or {"base64": bytes}

        Returns:
            None            
        """                
        self.developer_files.append(developer_file)
        self.update_updated_at()

        return None

    #
    # Public Class Methods:
    #    
    @classmethod
    def from_dict(cls, serializedObject) -> dict:
        """
        Serialize the object instance
        
        Returns:
            message: any of the message types: The created message
        """        
        return cls.model_validate(serializedObject)        