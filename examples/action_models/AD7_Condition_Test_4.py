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
p = Process("myProc1")

p_con = p.Condition("myCondition1")

p1 = p_con.Process("p1")
p2 = p_con.Process("p2")
p_act1 = p1.Action("p1_action")
p_act2 = p2.Action("p2_action")
p_end = p1.End()

# p_act3 = p.Action("Action 3")

###############################################
# 2 Run a simulation
asyncio.run(p.sim(print_out=True))
