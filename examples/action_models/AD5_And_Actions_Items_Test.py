from sysmpy import *
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
print('AD5_And_Actions_Items_Test')

###############################################
# 1 Define a model
p = Process("process")

p1, p2 = p.And("process 1", "process 2")
p_act1 = p1.Action("Action 1")
p_act2 = p2.Action("Action 2")

i1 = Item("Item1")
i2 = Item("Item2")
i3 = Item("Item3")

# p_act1.receives(i1)
p_act1.sends(i2)
p_act2.triggered(i2)
p_act2.sends(i3)

###############################################
# 2 Run a simulation
asyncio.run(p.sim(print_out=True))
