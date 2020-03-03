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

p_con1 = p.Condition("And1")
p1 = p_con1.Process("P1")
p2 = p_con1.Process("P2")
p3 = p_con1.Process("P3")
p_act1 = p1.Action("Action1")

p3.Action("Action42")

p.Action("Action4")

loop = p1.Loop(times=2)
pl1 = loop.Process("process1_1")

l_act3 = pl1.Action("Action111")


# p.Action("Action3")
print(p.get_mxgraph())