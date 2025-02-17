from datetime import datetime

def display_text_to_st_func(self, st, include_datetime: bool = True):
    """
    Print a text message on the screen
    
    Returns:
        None
    """     
    
    # Get the information
    author = self.get_author()
    author_type = self.get_author_type()
    display_datetime =  datetime.fromtimestamp(self.get_last_updated_timestamp()).strftime("%H:%M:%S %m-%d-%Y")

    # Display the content
    display_value = self.get_message_value_attribute("text")
    st.write(f"{author} ({author_type}):\n{display_value}\n{display_datetime}\n")    