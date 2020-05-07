from sysmpy import *
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
# 1 Define a model
p = Process("process1")

pl = p.Loop("process1_1", times=2)

l_act3 = pl.Action("Action1")

###############################################
# 2 Run a simulation
asyncio.run(p.sim(print_out=True))
