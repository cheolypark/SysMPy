from entity import *
import asyncio

""" 
                +---------------+
                |               |
                |    Action1    | 
                |               |         
                +---------------+         
                        |              
                        |                
                +---------------+        
                |               |        
                |    Action2    | 
                |               |        
                +---------------+   
"""
###############################################
# 1 Define actions
p = Process("process 1")
act1 = p.Action("Action1")
act2 = p.Action("Action2")

###############################################
# 2 run interface analyzer
p.evaluate_interfaces()


