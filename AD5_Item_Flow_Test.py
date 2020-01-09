from entity import *
import asyncio

"""
                +---------------+
                |               |
                |     start     |
                |               |
                +---------------+
                        | process
                        |
                +---------------+
                |               |
     (Item1)--->|    Action1    |
                |               | 
                +---------------+ 
                        |        
                        |        
                +---------------+
                |               |
                |    Action2    |
                |               |        
                +---------------+        
                        | 
                        |
                +---------------+
                |               |
                |      End      |
                |               |
                +---------------+
"""

# 1 Define actions
p = Process("process")
box1 = p.Action("Action1")
act2 = p.Action("Action2")

i1 = Item("Item1")
box1.receives(i1)

###############################################
# 2 run simulation
asyncio.run(p.sim())

