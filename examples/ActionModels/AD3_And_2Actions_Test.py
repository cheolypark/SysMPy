from sysmpy import *
import asyncio

"""
                            +---------------+
                            |               |
                            |     start     |
                            |               |
                            +---------------+
                                    | process
                        +----------(&)----------+
                        | p1                    | p2
                +---------------+       +---------------+
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
print('AD3_And_2Actions_Test')


###############################################
# 1 Define actions
p = Process("process")
p_and = p.And()
p1 = p_and.Process("p1")
p2 = p_and.Process("p2")

p_act1 = p1.Action("Action1")
p_act2 = p2.Action("Action2")

###############################################
# 2 run simulation
asyncio.run(p.sim())

