from entity import *
import asyncio

"""
                            +---------------+
                            |               |
                            |     start     |
                            |               |
                            +---------------+
                                    | p
                        +----------(&)----------+
                        | process 1             | process 2
                +---------------+               |
                |               |               |
                |    Action1    |               |
                |               |               |                  
                +---------------+              (L)----------+
                        |                       |           |
                +---------------+       +---------------+   |
                |               |       |               |   |
                |    Action2    |       |    Action3    |   |
                |               |       |               |   |
                +---------------+       +---------------+   |
                        |                       |           |
                        |                      (L)----------+
                        |                       |                        
                        +----------(&)----------+
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
p_act2 = p1.Action("Action 2")

loop = p2.Loop()
p1_1 = loop.Process("process1_1")

l_act3 = p1_1.Action("action 3")


###############################################
# 2 run simulation
asyncio.run(p.sim())
