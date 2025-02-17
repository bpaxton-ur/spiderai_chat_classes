"""
utils/chat_utils/helper_functions.py

This file contains some helper functions for the chat class.

Functions contained here include:
- timestamp_to_datetimestr(timestamp: float, format: str = "%I:%M %p, %B %d, %Y") -> str: Function to convert a timestamp into a string with a given format.
- validate_type(value, expected_type) -> bool: Function to validate types against a type hint

Author: M. Saif Mehkari
Version: 1.0
License Info: See license.txt file
"""

from typing import get_origin, get_args, Literal, Union, List, Dict, Tuple
from datetime import datetime 

def timestamp_to_datetimestr(timestamp: float, format: str = "%I:%M %p, %B %d, %Y") -> str:
    """
    Converts a timestamp to a string of a given format
    
    Args:
        timestamp: float: The timestamp
        format: str: The format to convert the timestamp to
        
    Returns:
        datetimestr: str: the timestamp converted to a string of a given format
    """

    return datetime.fromtimestamp(timestamp).strftime(format)

def validate_type(value, expected_type) -> bool:
    """
    Validates if a value matches an expected type hint.
    
    Args:
        value: The value to validate.
        expected_type: The expected type hint.
        
    Returns:
        bool: True if the value matches the expected type hint, False otherwise.
    """
    
    origin = get_origin(expected_type)  # Extract the origin type (e.g., list, dict, etc.)
    args = get_args(expected_type)      # Extract type arguments (e.g., types in List[int])

    # Handle simple types
    if origin is None:
        return isinstance(value, expected_type)

    # Handle Union
    if origin is Union:
        return any(validate_type(value, arg) for arg in args)

    # Handle Literal
    if origin is Literal:
        return value in args

    # Handle List
    if origin is list:
        return all(validate_type(item, args[0]) for item in value) if args else isinstance(value, list)

    # Handle Dict
    if origin is dict:
        key_type, value_type = args
        return all(
            validate_type(k, key_type) and validate_type(v, value_type) for k, v in value.items()
        )

    # Handle Tuple
    if origin is tuple:
        # Support both fixed-length tuples and variable-length tuples
        if len(args) == 2 and args[1] is Ellipsis:
            return all(validate_type(item, args[0]) for item in value)
        return len(value) == len(args) and all(validate_type(v, t) for v, t in zip(value, args))

    # Handle other generic types
    if isinstance(value, origin):
        return True

    return False