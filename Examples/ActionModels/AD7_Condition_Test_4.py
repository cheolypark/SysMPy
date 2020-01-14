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
                            +---------------+
                            |               |
                            |   Condition1  |
                            |               |
                            +---------------+
                                |       |                                    
                        +--------       --------+
                        | process 1             | process 2
                        |                       |           
                +---------------+       +---------------+   
                |               |       |               |   
                |    Action1    |       |    Action2    |   
                |               |       |               |   
                +---------------+       +---------------+   
                        |                       |           
                      (End)                     |                        
                                  (OR)----------+
                                    |
                            +---------------+
                            |               |
                            |    Action3    |
                            |               |
                            +---------------+
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

p_con = p.Condition("Condition 1")

p1 = p_con.Process("process 1")
p2 = p_con.Process("process 2")
p_act1 = p1.Action("Action 1")
p_end = p1.End()
p_act2 = p2.Action("Action 2")


###############################################
# 2 run simulation
asyncio.run(p.sim())
