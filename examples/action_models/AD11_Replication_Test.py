from sysmpy import *
import asyncio
"""
                            +---------------+
                            |               |
                            |     start     |
                            |               |
                            +---------------+
                                    | process
                                    |
                                    |   3 Replication
                                   (R)----------+
                                    |           |
                            +---------------+   |
                            |               |   |
                            |    Action1    |   |
                            |               |   |
                            +---------------+   |
                                    |           |
                                   (R)----------+
                                    |    
                                    |
                            +---------------+
                            |               |
                            |      End      |
                            |               |
                            +---------------+
"""
print('AD11_Replication_test')

###############################################
# 1 Define a model
p = Process("process")

rep = p.Replication()
rep.times = 3
p1_1 = rep.Process("process1_1")
l_act3 = p1_1.Action("Action1")

###############################################
# 2 Run a simulation
asyncio.run(p.sim(print_out=True))
