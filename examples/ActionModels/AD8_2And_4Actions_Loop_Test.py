from sysmpy import *
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
                +---------------+              (L)--------------+
                        |                       |               |
                +---------------+       +------(&)------+       |
                |               |       |proc3          |proc4  |
                |    Action2    |   +-------+       +-------+   |
                |               |   |       |       |       |   |
                +---------------+   |  Act3 |       |  Act4 |   |
                        |           |       |       |       |   |
                        |           +-------+       +-------+   |
                        |               |               |       |
                        |               +------(&)------+       |
                        |                       |               |                                                                                                
                        |                      (L)--------------+
                        |                       |                        
                        +----------(&)----------+
                                    |
                            +---------------+
                            |               |
                            |      End      |
                            |               |
                            +---------------+
"""
print('AD8_2And_4Actions_Loop_Test')

###############################################
# 1 Define actions
p = Process("process")

p_and = p.And()

p1 = p_and.Process("process 1")
p2 = p_and.Process("process 2")
p_act1 = p1.Action("Action 1")
p_act2 = p1.Action("Action 2")

loop = p2.Loop('process1_1')
l_and = loop.And()

l_p1 = l_and.Process("proc3")
l_p2 = l_and.Process("proc4")
p1_act3 = l_p1.Action("Act3")
p2_act4 = l_p2.Action("Act4")


###############################################
# 2 run simulation
asyncio.run(p.sim())
