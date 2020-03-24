from entity import *
import asyncio

"""
                            +---------------+
                            |               |
                            |     start     |
                            |               |
                            +---------------+
                                    | process1
                                    |
                                   (L)----------+
                                    |           |
                            +---------------+   |
                            |               |   |
                            |    Action1    |   |
                            |               |   |
                            +---------------+   |
                                    |           |
                                   (L)----------+
                                    |   2 times
                                    |
                            +---------------+
                            |               |
                            |    Action2    |
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
print('AD6_Loop_Test_2')

###############################################
# 1 Define actions
p = Process("process1")

loop = p.Loop(times=2)
p1_1 = loop.Process("process1_1")

l_act1 = p1_1.Action("Action1")

p.Action("Action2")

###############################################
# 2 run simulation
asyncio.run(p.sim())
