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
                |    Action1    |-------+
                |               |       | 
                +---------------+       | 
                        |             (Item1)
                        |               |
                +---------------+    (Trigger)
                |               |       |
                |    Action2    |<------+
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
p = Process("process 1")
act1 = p.Action("Action1")
act2 = p.Action("Action2")

i1 = Item("Item1")
act1.sends(i1)
act2.triggered(i1)

###############################################
# 2 run simulation
asyncio.run(p.sim())

