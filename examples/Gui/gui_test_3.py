from sysmpy import *
import asyncio
from gui_mxgraph_action_diagram import GuiMXGraphActionDiagram
from gui_mxgraph_block_diagram import GuiMXGraphBlockDiagram
from gui_mxgraph_hierarchy_diagram import GuiMXGraphHierarchyDiagram

main_p = Process('process')
p = main_p.Loop('p1', times=2)
p1, p2, p3, p4 = p.And('가열로', '압연', '냉각', '교정')
ht = p1.Action('가열')
rm = p2.Action('압연')
cl = p3.Action('냉각')
md = p4.Action('교정')

print(GuiMXGraphActionDiagram().get_mxgraph(p))