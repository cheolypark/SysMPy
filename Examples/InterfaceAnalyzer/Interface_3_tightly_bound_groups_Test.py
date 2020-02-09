from entity import *
import asyncio

""" 
                            +---------------+
         +----------------->|               |-------------------+
         |        +-------->|    Action1    |---------+         |
         |        |         |               |         |         |
         |        |         +---------------+         |         |
         |     (Item2)              |              (Item1)      |
         |        |                 |                 |         |    
         |        |         +---------------+         |         |
         |        |         |               |         |         |
         |        +---------|    Action2    |<--------+         |
         |        +-------->|               |---------+         |
         |        |         +---------------+         |         |
         |        |                 |                 |         |
      (Item6)     |                 |                 |      (Item5)
         |        |         +---------------+         |         |
         |        |         |               |         |         |
         |        |         |    Action3    |         |         |
         |        |         |               |         |         |
         |        |         +---------------+         |         |
         |     (Item4)              |              (Item3)      |
         |        |                 |                 |         |
         |        |         +---------------+         |         |
         |        |         |               |         |         |
         |        +---------|    Action4    |<--------+         |
         +------------------|               |<------------------+        
                            +---------------+                    
                             
"""
###############################################
# 1 Define actions
p = Process("process 1")
act1 = p.Action("Action1")
act2 = p.Action("Action2")
act3 = p.Action("Action3")
act4 = p.Action("Action4")

i1 = Item("Item1")
i2 = Item("Item2")
i3 = Item("Item3")
i4 = Item("Item4")
i5 = Item("Item5")
i6 = Item("Item6")
act1.sends(i1)
act1.sends(i5)
act2.sends(i3)
act2.sends(i2)
act4.sends(i4)
act4.sends(i6)
act1.receives(i2)
act1.receives(i6)
act2.receives(i1)
act2.receives(i4)
act4.receives(i3)
act4.receives(i5)

###############################################
# 2 run interface analyzer
p.evaluate_interfaces()


