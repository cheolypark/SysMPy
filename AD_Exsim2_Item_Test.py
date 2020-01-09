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
                |     Action1   |---->(Item2)
                |               |        |
                +---------------+        |
                        |                |
                +---------------+        |
                |               |        |
                |     Action2   |<-------+
                |               |
                +---------------+
                        |
                        |
                +---------------+
                |               |
                |      End      |
                |               |
                +---------------+
"""
###############################################
# 1 Define actions
p = Process("process 1")
act1 = p.Action("Action1")
act2 = p.Action("Action2")

i2 = Item("Item2")
pro1_1 = i2.Property("input", range=[1, 2, 3], value=1)

act1.sends(i2)
act2.receives(i2)


# External Simulation Script ######################################
def exsim_function1(io):
    out = io.get("Item2.input")
    out.value = random.random()
    print("exsim_function 1: " + str(out.value))

# Script end ##################################
act1.func(exsim_function1)

# External Simulation Script ######################################
def exsim_function2(io):
    input = io.get("Item2.input")
    print("exsim_function 2: " + str(input.value))
# Script end ##################################
act2.func(exsim_function2)

###############################################
# 2 run simulation
asyncio.run(p.sim())
