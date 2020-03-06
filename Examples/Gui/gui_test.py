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

p_con1 = p.And()

for i in range(3):
    p2 = p_con1.Process(f"P{i}")

    p_con2 = p2.Condition(f"condition{i}_2")
    p21 = p_con2.Process(f"P{i}_1")
    p22 = p_con2.Process(f"P{i}_2")

    for j in range(2):
        p21.Action(f"Action{i}_{j}")

p.get_mxgraph()
asyncio.run(p.sim())
asyncio.run(p.sim())
# print(p.get_mxgraph())