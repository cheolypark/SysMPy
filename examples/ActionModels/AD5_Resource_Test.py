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
                |    Action1    |-------+
                |               |       | 
                +---------------+       | 
                        |          (Resource1)
                        |               |
                +---------------+       |
                |               |       |
                |    Action2    |<------+
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
print('AD5_Resource_Test')

# 1 Define actions
p = Process("process 1")
act1 = p.Action("Action1")
act2 = p.Action("Action2")

r1 = Resource("Resource1", amount=5)

act1.produces(r1, amount=10)
act2.consumes(r1, amount=10)

###############################################
# 2 run simulation
asyncio.run(p.sim())
print("Process: " + str(p))

