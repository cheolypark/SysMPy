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
          (Item1)---------->|   Condition1  |
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
                        |                       |                        
                        +---------(OR)----------+
                                    |
                            +---------------+
                            |               |
                            |      End      |
                            |               |
                            +---------------+
"""
print('AD7_Condition_Test_2')

###############################################
# 1 Define a model
p = Process("process0")

p_con = p.Condition("Condition 1")

i1 = Item("Item1")
i1.Property('attr', [1, 2, 3], 1)

p_con.receives(i1)

p1 = p_con.Process("process 1")
p2 = p_con.Process("process 2")
p_act1 = p1.Action("Action 1")
p_act2 = p2.Action("Action 2")

# Condition Script ######################################
def function1(io):
    # inputs
    i1 = io.get('Item1.attr')
    # outputs
    o1, o2 = io.get('process 1'), io.get('process 2')

    i1.value += 10
    print("Current value: " + str(i1.value))

    if i1.value > 70:
        return o1
    else:
        return o2
# Script end ##################################

p_con.func(function1)

###############################################
# 2 Run a simulation
asyncio.run(p.sim(print_out=True))