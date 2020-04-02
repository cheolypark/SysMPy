from sysmpy import *
import asyncio
from gui_mxgraph_action_diagram import GuiMXGraphActionDiagram
from gui_mxgraph_block_diagram import GuiMXGraphBlockDiagram
from gui_mxgraph_hierarchy_diagram import GuiMXGraphHierarchyDiagram

p = Process("process1")

# l_act3 = p.Action("Action1")
pl = p.Loop("LOOP", times=2)
l_act3 = pl.Action("Action1")


print(GuiMXGraphActionDiagram().get_mxgraph(p))