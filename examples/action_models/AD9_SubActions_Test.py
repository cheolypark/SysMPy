from sysmpy import *
import asyncio
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
print('AD9_SubActions_Test')

###############################################
# 1 Define a model
p = Process("process1")
act1 = p.Action("Action1")

act1.set_decomposition(False)

p1_1 = act1.Process("process1.1")
act1_1 = p1_1.Action("Action1.1")

act2 = p.Action("Action2")

###############################################
# 2 Run a simulation
asyncio.run(p.sim(print_out=True))
