"""
utils/chat_utils/message.py

This file contains the BaseMessageClass along with the two inherited classes of SinglePartMessage and MultiPartMessage

Author: M. Saif Mehkari
Version: 1.0
License Info: See license.txt file
"""

#
# Import the correct packages
#
from pydantic import BaseModel, Field, model_validator
from typing import Literal, Any, final, Tuple
import message_types
from helper_functions import validate_type
from datetime import datetime

##############################################
# Base Message Content Class
##############################################
class BaseMessageClass(BaseModel, validate_assignment=True):
    """
    A base class to represent a chat message each belonging to a unique user. Inhereted classes are either single part or multipart.

    Attributes:
        author: str: The author of the message (fixed at creation).
        author_type: Literal["genai", "human", "developer"]: The author type can be a genai, human, or developer  (fixed at creation).
        message_type: str: The type of the message  (fixed at creation).
        metadata: dict: Any meta data associated with the message.
        created_at: float: The timestamp the chat message was created  (fixed at creation). 
        updated_at: float: The timestamp the chat message was last updated. 

    Public Instance Methods:
        get_author() -> str        
        get_author_type() -> str
        get_message_type() -> str
        get_metadata() -> dict
        get_metadata_attribute(key: str) -> Any        
        get_created_at() -> float
        get_updated_at() -> float
        to_dict() -> dict

        update_updated_at() -> None

        set_metadata(metadata: dict) -> None               
        set_metadata_attribute(attribute_metadata: Any, key: str) -> None            
            
    Public Class Method:
        from_dict() -> dict
    
    """    
    #
    # Attributes:
    #
    author: str = Field(description = "The author of the message.", frozen = True)
    author_type: Literal["genai", "human", "developer"] = Field(description = "The author can be a genai, human, or developer.", frozen = True)
    message_type: str = Field(default = "None", description = "The type of the message.", frozen = True)
    metadata: dict = Field(default_factory = lambda: dict(), description = "Any meta data associated with the message.") 
    created_at: float = Field(default_factory=lambda: datetime.now().timestamp(), description = "The timestamp the chat message was created.", frozen = True)
    updated_at: float = Field(default_factory= lambda: datetime.now().timestamp(), description = "The timestamp the chat message was last updated.")

    #
    # Public Instance Methods:
    #
    def get_author(self) -> str:
        """
        Getter for author.
        
        Returns:
            author: str: The author of the message.
        """        
        return self.author

    def get_author_type(self) -> str:
        """
        Getter for author type.
        
        Returns:
            author_type: str: The author type can be a genai, human, or developer.
        """        
        return self.author_type

    def get_message_type(self) -> str:
        """
        Getter for message type.
        
        Returns:
            message_type: str: The type of the message.
        """        
        return self.message_type
            
    def get_metadata(self) -> dict:
        """
        Getter for metadata.

        Returns:
            metadata: dict: Any meta data associated with the message
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
            created_at: float: The timestamp the chat message was created.
        """        
        return self.created_at

    def get_updated_at(self) -> float:
        """
        Getter for last updated timestamp.
        
        Returns:
            updated_at: float: The timestamp the chat message was last updated.
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
    
    def set_metadata(self, metadata: dict) -> None:
        """
        Setter for metadata.
        
        Args:
            data: dict: Any meta data associated with the message

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
            data: Any: Meta data associated with the message for a particular key.
            key: str: The key to set from the metadata.

        Returns:
            None
        """        
        self.metadata[key] = attribute_metadata            
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
    
#
#
#
# SINGLE PART MESSAGES
#
#
#

@final
class SinglePartMessage(BaseMessageClass, validate_assignment=True):
    """
    An inherited base class to represent a single part message. Inhereted classes include different types of content.

    Attributes:
        message_value: dict: A dictionary containing all the message content. 
        message_value_keys: set: The set of keys for the message value (fixed at creation).
        message_value_attribute_types: dict: The types for all the message value attributes (fixed at creation).

    Public Instance Methods:
        get_message_value() -> dict
        get_message_value_by_attribute(key: str) -> Any
        get_message_value_keys() -> set
        get_message_value_attribute_types() -> dict

        set_message_value(message_value: dict) -> None
        set_message_value_by_attribute(message_value_by_attribute: Any, key: str) -> None

        append_message_chunk(message_chunk: dict) -> None    
        append_message_chunk_by_attribute(message_chunk_by_attribute: Any, key: str) -> None      

    Public Class Methods:
        create_message(author: str, author_type: str, message_type: str, message_value: Any = None, metadata: dict = {})
        create_empty_message(author: str, author_type: str, message_type: str)                      

    Private Methods:
         __check_message_value_keys(message_value: dict, message_value_keys: set) -> Tuple[bool, str]
         __check_single_message_value_attribute_type(message_value_by_attribute: Any, key: str, message_value_attribute_types: dict) -> Tuple[bool, str]
         __check_all_message_value_attribute_types(message_value: dict, message_value_keys: set, message_value_attribute_types: dict) -> Tuple[bool, str]
         __check_message_value_structure(message_value: dict, message_value_keys: set, message_value_attribute_types: dict) -> Tuple[bool, str]

    Model Validator:         
        validate_message_value()
    """ 
    #
    # Attributes:
    #
    message_value: dict = Field(default_factory = lambda: dict(), description = "A dictionary containing all the message content.")   
    message_value_keys: set = Field(default_factory = lambda: set(), description = "The set of keys for the message value.", frozen = True)   
    message_value_attribute_types: dict = Field(default_factory = lambda: dict(), description = "The types for all the message value attributes.", frozen = True)   

    #
    # Additional validation
    #
    @model_validator(mode='after')
    def validate_message_value(self):        

        # Check the message value structure and raise errors if not correct
        valid_message, error_string = self.__check_message_value_structure(self.message_value, self.message_value_keys, self.message_value_attribute_types)
        if not(valid_message):
            raise ValueError(error_string)

        return self
    
    #
    # Public Instance Methods:
    #
    def get_message_value(self) -> dict:
        """
        Getter for message value.
        
        Returns:
            message_value: dict: A dictionary containing all the message content. 
        """        
        return self.message_value

    def get_message_value_by_attribute(self, key: str) -> Any:
        """
        Getter for message value attribute.
        
        Args:
            key: str: The key to get the message value. 

        Returns:
            message_value_by_attribute: Any: The value of the message associated with the appropriate key.
        """        
        return self.message_value[key]  

    def get_message_value_keys(self) -> set:
        """
        Getter for message value keys.
        
        Returns:
            message_value_keys: set: The set of keys for the message value. 
        """                
        return self.message_value_keys   
    
    def get_message_value_attribute_types(self) -> dict:
        """
        Getter for the types for all the message value attributes.
        
        Returns:
            message_value_attribute_types: dict: The types for all the message value attributes.
        """                
        return self.message_value_attribute_types  

    def set_message_value(self, message_value: dict) -> None:
        """
        Setter for message value.

        Args:
            message_value: Any: A dictionary containing all the message content.

        Returns:
            None
        """               

        # Before setting the value, check the message value structure and raise errors if not correct       
        valid_message, error_string = self.__check_message_value_structure(self.message_value, self.message_value_keys, self.message_value_attribute_types)
        if not(valid_message):
            raise ValueError(error_string)
        
        else:        
            # Update the message
            self.message_value = message_value
            self.update_updated_at()

        return None
    
    def set_message_value_by_attribute(self, message_value_by_attribute: Any, key: str) -> None:
        """
        Setter for message value attribute.

        Args:
            message_value_by_attribute: Any: The value of the message value attribute.
            key: str: The key to set the message value. 
        
        Returns:
            None
        """                

        # Before setting the value, check the type and if incorrect raise an error
        valid_type, error_string = self.__check_single_message_value_attribute_type(message_value_by_attribute, key, self.message_value_attribute_types)
        if not(valid_type):
            raise ValueError(error_string)       
        
        else:
            # Update the message
            self.message_value[key] = message_value_by_attribute
            self.update_updated_at()

        return None    

    def append_message_chunk(self, message_chunk: dict) -> None:
        """
        Chunk setter for message value.

        Args:
            message_chunk: Any: A dictionary containing a chunk of the message content.

        Returns:
            None
        """               

        # Before setting the value, check the message value structure and raise errors if not correct       
        valid_message, error_string = self.__check_message_value_structure(self.message_value, self.message_value_keys, self.message_value_attribute_types)
        if not(valid_message):
            raise ValueError(error_string) 

        else:       
            # Update the message
            for key in self.message_value_keys:
                self.append_message_chunk_attribute(message_chunk[key], key)

            self.update_updated_at()

        return None

    def append_message_chunk_by_attribute(self, message_value_by_attribute: Any, key: str) -> None:
        """
        Chunk setter for message value attribute.

        Args:
            message_value_by_attribute: Any: The chunk value of the message value attribute.
            key: str: The key to set the message value. 
        
        Returns:
            None
        """     
        # Before appending the value, check the type and if incorrect raise an error
        valid_type, error_string = self.__check_single_message_value_attribute_type(message_value_by_attribute, key, self.message_value_attribute_types)
        if not(valid_type):
            raise ValueError(error_string)           
       
        else:
            # Update the message
            self.message_value[key] = self.get_message_value_by_attribute(key) + message_value_by_attribute
            self.update_updated_at()

        return None    

    #
    # Public Class Methods:
    #    
    @classmethod    
    def create_message(cls, author: str, author_type: str, message_type: str, message_value: Any = None, metadata: dict = {}): 
        """
        Function to create a single part message

        Args:
            author: str: The author of the message.
            author_type: Literal["genai", "human", "developer"]: The author type can be a genai, human, or developer.
            message_type: str: The type of the message.
            message_value: Any: The value of the message. Defaults to none to create an empty message.
            metadata: dict: Any meta data associated with the message.

        Return:
            message: any of the message types: The created message
        """

        # Make sure this is a valid message type and if not raise an error
        if message_type not in message_types.message_types.keys():
            raise ValueError("Unknown message type.")    

        # If no message value then get the empty message value
        if not(message_value):
            message_value = message_types.message_types[message_type]["empty_message_value"]    

        # Create the message
        message = SinglePartMessage(author = author,
                                    author_type = author_type,
                                    message_type = message_type,
                                    message_value = message_value,
                                    message_value_keys = message_types.message_types[message_type]["message_value_keys"],
                                    message_value_attribute_types = message_types.message_types[message_type]["message_value_attribute_types"],
                                    metadata = metadata)

        return message
    
    @classmethod    
    def create_empty_message(cls, author: str, author_type: str, message_type: str): 
        """
        Function to create a single part message

        Args:
            author: str: The author of the message.
            author_type: Literal["genai", "human", "developer"]: The author type can be a genai, human, or developer.
            message_type: str: The type of the message.

        Return:
            message: any of the message types: The created message
        """

        # Make sure this is a valid message type and if not raise an error
        if message_type not in message_types.message_types.keys():
            raise ValueError("Unknown message type.")    

        # Create the message
        message = SinglePartMessage(author = author,
                                    author_type = author_type,
                                    message_type = message_type,
                                    message_value = message_types.message_types[message_type]["empty_message_value"]    ,
                                    message_value_keys = message_types.message_types[message_type]["message_value_keys"],
                                    message_value_attribute_types = message_types.message_types[message_type]["message_value_attribute_types"],
                                    metadata = {})

        return message    

    #
    # Private Methods:
    # 
    def __check_message_value_keys(self, message_value: dict, message_value_keys: set) -> Tuple[bool, str]:        
        """
        Checks if the message value has all the required keys
        
        Args:
            message_value: dict: A dictionary containing all the message content. 
            message_value_keys: set: The set of keys for the message value.    

        Returns:
            valid_keys: bools: True if all the required keys are present.
            error_string: str: The string with the error if any
        """     
        if set(message_value.keys()) == message_value_keys:
            valid_keys = True
            error_string = ""
        else:
            valid_keys = False
            error_string = "message_value does not have all the required keys."

        return valid_keys, error_string

    def __check_single_message_value_attribute_type(self, message_value_by_attribute: Any, key: str, message_value_attribute_types: dict) -> Tuple[bool, str]:        
        """
        Checks if one of message value attributes has the correct type.
        
        Args:
            message_value_by_attribute: Any: The value of the message attribute
            key: str: The key of the attribute
            message_value_attribute_types: dict: The types for all the message value attributes (fixed at creation).    

        Returns:
            valid_type: bools: True if the type for the attribute given by key is correct.
            error_string: str: The string with the error if any
        """     

        if validate_type(message_value_by_attribute, message_value_attribute_types[key]):
            valid_type = True
            error_string = ""
        else:
            valid_type = False
            error_string = f"The key: {key} does not have the correct type."

        return valid_type, error_string
            
    def __check_all_message_value_attribute_types(self, message_value: dict, message_value_keys: set, message_value_attribute_types: dict) -> Tuple[bool, str]:        
        """
        Checks if all the message value attributes have the correct type.
        
        Args:
            message_value: dict: A dictionary containing all the message content. 
            message_value_keys: set: The set of keys for the message value (fixed at creation).
            message_value_attribute_types: dict: The types for all the message value attributes (fixed at creation).   

        Returns:
            valid_types: bool: True if all the attributes have the correct type.
            error_string: str: The string with the error if any
        """     
        valid_types = True
        error_string_list = []
        for message_value_key in message_value_keys:
            valid_type, error_string = self.__check_single_message_value_attribute_type(message_value[message_value_key], message_value_key, message_value_attribute_types)
            if not(valid_type):
                valid_types = False
                error_string_list.append(error_string)

        return valid_types, ";".join(error_string_list)
    
    def __check_message_value_structure(self, message_value: dict, message_value_keys: set, message_value_attribute_types: dict) -> Tuple[bool, str]:       
        """
        Checks if the message value attributes has the correct structure and if not raise errors
        
        Args:
            message_value: dict: A dictionary containing all the message content. 
            message_value_keys: set: The set of keys for the message value (fixed at creation).
            message_value_attribute_types: dict: The types for all the message value attributes (fixed at creation).   

        Returns:
            valid_message: bool: True if all the attributes have the correct type.
            error_string: str: The string with the error if any
        """     

        valid_message = True
        error_string_list = []

        # Make sure the message value being created has all the required keys
        valid_keys, error_string = self.__check_message_value_keys(message_value, message_value_keys)
        if not(valid_keys):
            valid_message = False
            error_string_list.append(error_string)

        # Check if the message_value attribute types are correct:
        valid_types, error_string = self.__check_all_message_value_attribute_types(message_value, message_value_keys, message_value_attribute_types)
        if not(valid_types):
            valid_message = False
            error_string_list.append(error_string)
                         
        return valid_message, ";".join(error_string_list)


#
#
#
# MULTIPART MESSAGES
#
#
#

@final
class MultiPartMessage(BaseMessageClass, validate_assignment=True):
    """
    A class to store a multi part message. 

    Attributes:
        message_type: str: The type of the message which in this case is multipart.
        message_list: list: The parts of a multipart message.

    Public Instance Methods:
        get_message_list() -> list[SinglePartMessage]
        get_message(index: int) -> SinglePartMessage
        get_message_type_list() -> list[str]

        set_message_list(message_list: list[SinglePartMessage]) -> None
        set_message(index: int, message: SinglePartMessage) -> None
        
        append_message(message: SinglePartMessage) -> None
        append_message_chunk(message_type: str, message_chunk: dict) -> None 
        append_message_chunk_by_attribute(message_type: str, message_chunk_by_attribute: Any, key: str) -> None 
      
    """    
    #
    # Attributes:
    #
    message_type: str = Field(default = "multipart", description = "The type of the message which in this case is multipart.", frozen = True)
    message_list: list[SinglePartMessage] = Field(default_factory = lambda: list(), description = "The parts of a multipart message.", validate_assignment=True)

    #
    # Public Instance Methods:
    #
    def get_message_list(self) -> list[SinglePartMessage]:
        """
        Getter for the message list.

        Returns:
            message_list: list: A list of all the parts of the multipart message.
        """
        return self.message_list

    def get_message(self, index: int) -> SinglePartMessage:
        """
        Getter for a specific message in the message list.

        Args:
            index: int: The index of the message in the list.

        Returns:
            message: SinglePartMessage: The requested message.
        """
        return self.message_list[index]
   
    def get_message_type_list(self) -> list[str]:
        """
        Generates a list of all the types in the multipart messages

        Returns:
            message_type_list: list[str]: A list of all the types in the multipart message
        """

        # Get all the types
        message_type_list_int = []
        for message in self.message_list:
            message_type_list_int.append(message.get_message_type())

        # Make the list unique
        message_type_list = list(set(message_type_list_int))
        
        return message_type_list

    def set_message_list(self, message_list: list[SinglePartMessage]) -> None:
        """
        Setter for the message list.

        Args:
            message_list: list: The new message list.

        Returns:
            None
        """
        self.message_list = message_list
        self.update_updated_at()

        return None

    def set_message(self, index: int, message: SinglePartMessage) -> None: 
        """
        Setter for a specific message in the message list.

        Args:
            index: int: The index of the message to update.
            message: SinglePartMessage: The new message.

        Returns:
            None
        """
        self.message_list[index] = message
        self.update_updated_at()

        return None

    def append_message(self, message: SinglePartMessage) -> None:
        """
        Append a new message to the message list.

        Args:
            message: SinglePartMessage: The message to add.

        Returns:
            None
        """       
        self.message_list.append(message)
        self.update_updated_at()

        return None

    def append_message_chunk(self, message_type: str, message_chunk: dict) -> None: 
        """
        Add a chunk value to the last message in the message list or if not appropriate create a new message.

        Args:
            message_type: str: The type of the message which in this case is singlepart.
            message_chunk: Any: Chunk to augment the message dict by.

        Returns:
            None
        """

        # Make sure the chunk_value type is not multipart as a multipart cannot contain another multipart message.
        if "multipart" == message_type:
            raise ValueError("Chunk dict message type cannot be a multipart type (or anything inherited from it).")

        # If previous message type is not same then you create a new message and add this
        elif (message_type != self.message_list[-1].get_message_type()):
            message = SinglePartMessage.create_message(author = self.author, author_type = self.author_type, message_type = message_type, message_value = message_chunk)
            self.message_list.append(message)     

        # If message type is the same as the last message in the multipart, then augment the message
        elif (message_type == self.message_list[-1].get_message_type()):
            self.message_list[-1].append_message_chunk(message_chunk = message_chunk)

        # Update the time
        self.update_updated_at()

        return None       

    def append_message_chunk_by_attribute(self, message_type: str, message_chunk_by_attribute: Any, key: str) -> None: 
        """
        Add a chunk value attribute to the last message in the message list or if not appropriate create a new message.

        Args:
            message_type: str: The type of the message which in this case is singlepart.
            message_chunk_by_attribute: Any: Chunk to augment the message value attribute by.
            key: str: The key to set the message value. 
            start_new_message: bool: Should a new message be started      

        Returns:
            None
        """

        # Make sure the chunk_value type is not multipart as a multipart cannot contain another multipart message.
        if "multipart" == message_type:
            raise ValueError("Chunk dict message type cannot be a multipart type (or anything inherited from it).")
        
        # If previous message type is not same then you create a new message and add this (we will create an empty message and augment)
        elif (message_type != self.message_list[-1].get_message_type()):
            message = SinglePartMessage.create_empty_message(author = self.author, author_type = self.author_type, message_type = message_type)
            message.append_message_chunk_by_attribute(message_chunk_attribute = message_chunk_by_attribute, key = key)
            self.message_list.append(message)     

        # If message type is the same as the last message in the multipart, then augment the message
        elif (message_type == self.message_list[-1].get_message_type()):
            self.message_list[-1].append_message_chunk_by_attribute(message_chunk_attribute = message_chunk_by_attribute, key = key)

        # Update the time
        self.update_updated_at()

        return None        

    #
    # Public Class Methods:
    #    
    @classmethod    
    def create_message(cls, author: str, author_type: str, message_list: list[SinglePartMessage], metadata: dict = {}): 
        """
        Function to create a single part message

        Args:
            author: str: The author of the message.
            author_type: Literal["genai", "human", "developer"]: The author type can be a genai, human, or developer.
            message_list: list[SinglePartMessage]: The parts of a multipart message.
            metadata: dict: Any meta data associated with the message.

        Return:
            message: any of the message types: The created message
        """

        message = MultiPartMessage(author = author,
                                   author_type = author_type,
                                   message_list = message_list,
                                   metadata = metadata)

        return message