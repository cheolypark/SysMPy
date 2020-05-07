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
p = Process('main process')
b, r, a, e = p.And('가열로', '압연기', '냉각기', '교정기')
act_init_roll = b.Action('가열')
act_perf_roll = r.Action('압연')
act_perf_agc = a.Action('냉각')
act_eval_rslt = e.Action('교정')

# b.Property('온도', range=[10, 20])

i_init_roll = Item('슬라브')
i_init_roll.Property('Thickness', range=Normal(10, 1))

# i_act_perf_roll = Item('슬라브2')
# i_act_perf_roll.Property('Thickness', range=[10, 20])
# i_act_perf_roll.Property('Width', range=[10, 11, 12])
# i_act_perf_roll.Property('Length', range=[10, 20])
# i_act_perf_roll.Property('Temperature', range=[10, 11, 12])
#
# i_act_perf_agc = Item('슬라브3')
# i_act_perf_agc.Property('Thickness', range=[10, 20])
# i_act_perf_agc.Property('Width', range=[10, 11, 12])
# i_act_perf_agc.Property('Length', range=[10, 20])
# i_act_perf_agc.Property('Temperature', range=[10, 11, 12])

act_init_roll.sends(i_init_roll)
act_perf_agc.triggered(i_init_roll)
# act_perf_agc.sends(i_act_perf_agc)
# act_perf_roll.triggered(i_act_perf_agc)
# act_perf_roll.sends(i_act_perf_roll)
# act_eval_rslt.triggered(i_act_perf_roll)
###############################################
# 2 run simulation


# print(GuiMXGraphActionDiagram().get_mxgraph(p))
# print(GuiMXGraphBlockDiagram().get_mxgraph(p, width=500, height=1000))
# print(GuiMXGraphHierarchyDiagram().get_mxgraph(p, type=Process))

# p.get_mx_action_diagram()
# asyncio.run(p.sim(print_out=True))
asyncio.run(p.sim())
# asyncio.run(p.sim())
# print(p.get_mx_action_diagram())