from entity import *
import asyncio


"""
                                      +---------------+
                                      |               |
                                      |     start     |
                                      |               |
                                      +---------------+
                                              | process
                        +--------------------(&)--------------------+
                        | process 1                                 | process 2
                +---------------+                           +---------------+
                |               |                           |               |
     (Item1)--->|    Action1    |---->(Item2)--(Trigger)--->|    Action2    |---->(Item3)
                |               |                           |               |
                +---------------+                           +---------------+
                        |                                           |
                        +--------------------(&)--------------------+
                                              |
                                      +---------------+
                                      |               |
                                      |      End      |
                                      |               |
                                      +---------------+
"""
###############################################
# 1 Define actions
p = Process("process")

p_and = p.And()

p1 = p_and.Process("process 1")
p2 = p_and.Process("process 2")
p_act1 = p1.Action("Action 1")
p_act2 = p2.Action("Action 2")

i1 = Item("Item1")
i2 = Item("Item2")
i3 = Item("Item3")
i2.size(1)

# define Conduit for the item 2
con1 = Conduit("Conduit 1")
con1.transfers(i2)
con1.delay(7)
con1.capacity(1)

p_act1.receives(i1)
p_act1.sends(i2)
p_act2.triggered(i2)
p_act2.sends(i3)

###############################################
# 2 run simulation
asyncio.run(p.sim(until=15))
