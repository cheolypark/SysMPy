import asyncio
from sysmpy import *
"""
                            +---------------+        /   +---------------+
                            |               |       /    |               |
                            |     start     |      /     |     start     |
                            |               |     /      |               |
                            +---------------+    /       +---------------+
                                    | process1  /                | process1.1
                                    |          /                 | 
                            +---------------+            +---------------+    
                            |               |            |               |    
                            |    Action1    |            |   Action1.1   |    
                            |             |||            |               |    
                            +---------------+            +---------------+    
                                    |          \                 |          
                                    |           \                |
                            +---------------+    \       +---------------+
                            |               |     \      |               |
                            |    Action2    |      \     |      End      |
                            |               |       \    |               |
                            +---------------+        \   +---------------+
                                    |
                                    |
                            +---------------+
                            |               |
                            |      End      |
                            |               |
                            +---------------+ 
"""
print('AD9_SubActions_Test_3')
from examples.action_models.AD9_SubActions_Test_2 import p
import examples.action_models.AD9_SubActions_Test_2 as super

###############################################
# 1 Define a model
p1_1 = super.act1.Process("process1.1")
act1_1 = p1_1.Action("Action1.1")

###############################################
# 2 Run a simulation
asyncio.run(p.sim(print_out=True))
