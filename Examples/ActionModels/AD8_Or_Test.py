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
                        +---------(OR)----------+
                        | process 1             | process 2
                        |                       |           
                +---------------+       +---------------+   
                |               |       |               |   
                |    Action1    |       |    Action2    |   
                |               |       |               |   
                +---------------+       +---------------+   
                        |                       |           
                        |                       |                        
                        +---------(OR)----------+
                                    |
                            +---------------+
                            |               |
                            |      End      |
                            |               |
                            +---------------+
"""
print('AD8_Or_Test')

###############################################
# 1 Define actions
p = Process("process")

p_or = p.Or()

p1 = p_or.Process("process 1")
p2 = p_or.Process("process 2")

# Script ######################################
def function(p1, p2):
    import random
    if random.random() < 0.5:
        return p1
    else:
        return p2
# Script end ##################################

p_or.function = function(p1, p2)

print(p_or.function.name)

p_act1 = p1.Action("Action 1")
p_act2 = p2.Action("Action 2")


###############################################
# 2 run simulation
asyncio.run(p.sim())
