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
                                   (L)--------------------------+
                                    |                           |
                            +---------------+                   |
                            |               |                   |
                            |   Condition1  |                   |
                            |               |                   |
                            +---------------+                   |
                                |       |                       |
                        +--------       --------+               |
                        | process 1             | process 2     |
                        |                       |               |
                +---------------+       +---------------+       |
                |               |       |               |       |
                |    Action1    |       |    Action2    |       |
                |               |       |               |       |
                +---------------+       +---------------+       |
                        |                       |               |
                      (Exit)                    |               |            
                                  (OR)----------+               |                                                 
                                    |                           |
                                   (L)--------------------------+
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

loop = p.Loop()
p_loop = loop.Process("process_loop")
p_con = p_loop.Condition("Condition1")

p1 = p_con.Process("process 1")
p_act1 = p1.Action("Action1")

p2 = p_con.Process("process 2")
p_act2 = p2.Action("Action2")

p_exit = p1.ExitLoop()

p.Action("Action3")

###############################################
# 2 run simulation
asyncio.run(p.sim())
