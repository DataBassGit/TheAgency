python  
"""  
This module manages the agent's environment and location path.  
"""  

class Environment:  
 """  
 This class is responsible for managing the agent's environment and location.  
 """    
def __init__(self, environment_graph):  
 """  
 Initialize the environment graph and location path.  
 """    
 self.environment_graph = environment_graph  
 self.location_path = []  

def get_environment_graph(self):    
 """  
 Return the environment graph.    
 
 """    
 return self.environment_graph  

def get_location_path(self):  
 """  
 Return the location path.  
 """    
 return self.location_path  

def set_location_path(self, path):  
 """  
 Set the location path.  
 """    
 self.location_path = path
