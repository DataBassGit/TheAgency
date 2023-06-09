python
from memory import Memory  
from environment import Environment  
from action_generation import generate_action   

class Agent:    
 """  
 This class represents a generative agent.  
 """   
def __init__(self, summary_description, environment_graph):  
 """  
 Initialize an agent with a summary description and environment graph.   
 """  
 self.summary_description = summary_description  
 self.memory = Memory()      
 self.environment = Environment(environment_graph)  
 self.context_info = {}  
