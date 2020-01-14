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
                |     Action3   |
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

# 1 Define actions
p = Process("process")
act1 = p.Action("Action1")
act2 = p.Action("Action2")
act3 = p.Action("Action3")

###############################################
# 2 run simulation
# Entity._debug_mode = True
asyncio.run(p.sim())

actions = Process.get_by_type(Action)
e = {x.name:x.total_time for x in actions}
print(e)

# for name in dir():
#     if not name.startswith('_'):
#         del globals()[name]
#
# from entity import *
# import asyncio
#
# p = Process("process")
# act1 = p.Action("Action1")
# act2 = p.Action("Action2")
# act3 = p.Action("Action3")
#
# asyncio.run(p.sim())

