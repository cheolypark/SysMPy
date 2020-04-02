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
                            |  Condition 1  |                   |
                            |               |                   |
                            +---------------+                   |
                                |       |                       |
                        +--------       --------+               |
                        | process 1             | process 2     |
                        |                       |               |
                +---------------+       +---------------+       |
                |               |       |               |       |
                |    Action 1   |       |    Action 2   |       |
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
                            |    Action 3   |
                            |               |
                            +---------------+
                                    |
                            +---------------+
                            |               |
                            |      End      |
                            |               |
                            +---------------+
                        
                            
"""
print('AD10_Loop_Exit_Test')

###############################################
# 1 Define actions
p = Process("process")

p_loop = p.Loop("process_loop")
p_con = p_loop.Condition("Condition 1")

p1 = p_con.Process("process 1")
p_act1 = p1.Action("Action 1")

p2 = p_con.Process("process 2")
p_act2 = p2.Action("Action 2")

p_exit = p1.ExitLoop()

p.Action("Action 3")

###############################################
# 2 run simulation
asyncio.run(p.sim())
