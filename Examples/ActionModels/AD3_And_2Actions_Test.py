from entity import *
import asyncio

"""
                            +---------------+
                            |               |
                            |     start     |
                            |               |
                            +---------------+
                                    | p0
                        +----------(&)----------+
                        | p1                    | p2
         (i)    +---------------+       +---------------+
                |               |       |               |
                |    Action1    |       |    Action2    |
                |               |       |               |
                +---------------+       +---------------+
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
p = Process("p0")
p_and = p.And()
p1 = p_and.Process("p1")
p2 = p_and.Process("p2")

p_act1 = p1.Action("Action1")
p_act2 = p2.Action("Action2")

###############################################
# 2 run simulation
asyncio.run(p.sim())
