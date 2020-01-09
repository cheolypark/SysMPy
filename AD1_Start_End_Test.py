from entity import *
import asyncio

"""
                +---------------+
                |               |
                |     start     |
                |               |
                +---------------+
                        | process1
                        |
                +---------------+
                |               |
                |      End      |
                |               |
                +---------------+
"""

# 1 Define actions
p = Process("process1")

###############################################
# 2 run simulation
asyncio.run(p.sim())
