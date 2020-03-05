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
                |     Action1   |
                |               |        
                +---------------+        
                        |
                        |
                +---------------+
                |               |
                |     Action2   |
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

p = Process("process")

p_con1 = p.Or()
p1 = p_con1.Process("P1")
p2 = p_con1.Process("P2")
p3 = p_con1.Process("P3")

act1 = p1.Action("Action1")
act2 = p3.Action("Action2")

i1 = Item("Item1")
act1.sends(i1, act2)
i3 = Item("Item2")
act1.sends(i3, act2)
i2 = Item("Item3")
act1.sends(i2, act2)

# p.Action("Action3")
print(p.get_mxgraph())