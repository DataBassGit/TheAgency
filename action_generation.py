python
"""  
This module is responsible for generating the agent's actions.  
"""  
import requests
import json  
import os
import logging  
from memory import Memory  
from environment import Environment

logging.basicConfig(level=logging.INFO)  

API_KEY = os.environ.get("CLAUDE_API_KEY")   
 
def generate_action(summary_description: str, memory: Memory, environment: Environment) -> str:  
 """  
 Generate an action by querying the Claude API.    
 
 Parameters:  
 summary_description (str): The agent's summary description.  
 memory (Memory): The agent's memory.   
 environment (Environment): The agent's environment.  
 
 Returns:   
 - The generated action if successful   
 - None if an error occurs  
 """   
 
 if API_KEY is None:  
 raise ValueError("API Key not found. Please set the environment variable 'CLAUDE_API_KEY'.")    
 
 logging.info("Request sent to API")    
 prompt = f"You are currently at {' > '.join(environment.get_location_path())}. Given everything you currently know, including: \\n \\n"    
 prompt += summary_description + "\\n \\n"      

 try:             
 response = requests.post("https://api.anthropic.com/v1/complete", headers=headers, json=data)             
 if response.ok:                      
 completion = response.json().get("completion")                      
 if completion:                         
 next_action = completion                         
 memory.add_event_to_memory(f'Action: {next_action}')                         
 return next_action                      
 else:                      
 logging.exception(f"Error generating action: Expected key 'completion' not found in {response.json()}")                      
 return None             
 else:             
 logging.exception(f"Error generating action: {response.status_code} Response")             
 return None  
 except Exception as e:         
 logging.exception(f"Error generating action: {e}")             
 return None    
