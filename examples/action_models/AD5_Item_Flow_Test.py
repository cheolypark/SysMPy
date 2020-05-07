from sysmpy import *
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

print('AD5_Item_Flow_Test')

###############################################
# 1 Define a model
p = Process("process")
box1 = p.Action("Action1")
act2 = p.Action("Action2")

i1 = Item("Item1")
box1.receives(i1)

###############################################
# 2 Run a simulation
asyncio.run(p.sim(print_out=True))

