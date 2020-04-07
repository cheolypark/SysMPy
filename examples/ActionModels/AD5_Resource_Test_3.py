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
                |    Action1    | 
                |               |         
                +---------------+        
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

print('AD5_Resource_Test_2')

# 1 Define actions
p = Process("process 1")
act1 = p.Action("Action1")
act2 = p.Action("Action2")

r1 = Resource("Resource1", amount=20)

# act1.produces(r1, amount=10)
act2.seizes(r1, amount=5)

###############################################
# 2 run simulation
asyncio.run(p.sim(until=10))

