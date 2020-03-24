from entity import *
import asyncio

""" 
                +---------------+
                |               |
                |    Action1    |
                |               | 
                +---------------+ 
                        |             (Item1)
                        |                       (Item2)   
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

i1 = Item("Item1")
i2 = Item("Item2")


###############################################
# 2 run code_gui analyzer
p.evaluate_interfaces()


