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
                            +---------------+
                            |               |
                            |  Condition 1  |
                            |               |
                            +---------------+
                                |       |                                    
                        +--------       --------+
                        | process 1             | process 2
                        |                       |           
                +---------------+       +---------------+   
                |               |       |               |   
                |    Action 1   |       |    Action 2   |   
                |               |       |               |   
                +---------------+       +---------------+   
                        |                       |           
                      (End)                     |                        
                                  (OR)----------+
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
print('AD7_Condition_Test_4')

###############################################
# 1 Define a model
p = Process("process")
p.Action("Act")

p_con = p.Condition("Condition 1")

p1 = p_con.Process("process 1")
p2 = p_con.Process("process 2")
p_act1 = p1.Action("Action 1")
p_act2 = p2.Action("Action 2")
p_end = p1.End()

p_act3 = p.Action("Action 3")

###############################################
# 2 Run a simulation
asyncio.run(p.sim(print_out=True))
