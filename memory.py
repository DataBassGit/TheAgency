python
"""  
This module is responsible for managing the agent's memory stream.  
"""
from typing import List

class Memory:  
 """  
 This class is responsible for managing the agent's memory stream.  
 """  
def __init__(self):  
 """  
 Initialize an empty memory stream.  
 """  
 self.memory_stream = []  

def get_memory_stream(self) -> List[str]:  
 """  
 Return the memory stream.    
 
 Returns:  
 List[str]: The memory stream.  
 """  
 return self.memory_stream

def add_event_to_memory(self, event: str) -> None:  
 """  
 Add an event to the memory stream.    
 
 Parameters:  
 event (str): The event to add to the memory stream.    
 
 Raises:  
 ValueError: If event is not a string.  
 """  
 # Validate the input is a string  
 if not isinstance(event, str):  
 raise ValueError("Event must be a string.")    
 
 self.memory_stream.append(event)  # Add the event to the memory stream
