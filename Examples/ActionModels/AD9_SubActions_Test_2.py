from entity import *
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
###############################################
# 1 Define actions
p = Process("process1")
act1 = p.Action("Action1")
act2 = p.Action("Action2")

