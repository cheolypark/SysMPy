from sysmpy import *
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

Entity._debug_mode = True

###############################################
# 2 Run a simulation
asyncio.run(p.sim(print_out=True))
