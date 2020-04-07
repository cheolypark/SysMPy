from sysmpy import *
import asyncio
from gui_mxgraph_action_diagram import GuiMXGraphActionDiagram
from gui_mxgraph_block_diagram import GuiMXGraphBlockDiagram
from gui_mxgraph_hierarchy_diagram import GuiMXGraphHierarchyDiagram

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
# Test 1
p = Process("Root Process")
p_act1 = p.Action("Action2")

p1_1 = p_act1.Process("process1.1")
act1_1 = p1_1.Action("Action1.1")

print(GuiMXGraphActionDiagram().get_mxgraph(p))
# print(GuiMXGraphHierarchyDiagram().get_mxgraph(p, type=Process))

# p.get_mx_action_diagram()
# asyncio.run(p.sim())
# asyncio.run(p.sim())
# print(p.get_mx_action_diagram())