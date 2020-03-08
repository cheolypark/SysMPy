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
                                    | process1_1|
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
                            |      End      |
                            |               |
                            +---------------+
"""
print('AD6_Loop_Test_1')

###############################################
# 1 Define actions
p = Process("process1")

loop = p.Loop(times=2)
pl = loop.Process("process1_1")

l_act3 = pl.Action("Action1")


###############################################
# 2 run simulation
asyncio.run(p.sim())
