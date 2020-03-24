from entity import *
import asyncio

""" 
                +---------------+
                |               |
      +-------->|    Action1    |---------+
      |         |               |         | 
      |         +---------------+         | 
   (Item2)              |              (Item1)
      |                 |                 |
      |         +---------------+         |
      |         |               |         |
      +---------|    Action2    |<--------+
      +-------->|               |---------+        
      |         +---------------+         |
      |                 |                 |
      |                 |                 |
      |         +---------------+         |
      |         |               |         |  
      |         |    Action3    |         |
      |         |               |         | 
      |         +---------------+         | 
   (Item4)              |              (Item3)
      |                 |                 |
      |         +---------------+         |
      |         |               |         |
      +---------|    Action4    |<--------+
                |               |        
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
act1.sends(i1)
act2.sends(i3)
act2.sends(i2)
act4.sends(i4)
act1.receives(i2)
act2.receives(i1)
act2.receives(i4)
act4.receives(i3)

###############################################
# 2 run gui analyzer
p.evaluate_interfaces()


