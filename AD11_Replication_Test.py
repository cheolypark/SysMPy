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
###############################################
# 1 Define actions
p = Process("process")

rep = p.Replication()
rep.times = 3
p1_1 = rep.Process("process1_1")
l_act3 = p1_1.Action("Action1")

###############################################
# 2 run simulation
asyncio.run(p.sim())

