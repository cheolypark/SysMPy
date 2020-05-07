from sysmpy import *
import asyncio

"""
                            +---------------+
                            |               |
                            |     start     |
                            |               |
                            +---------------+
                                    | process
                        +---------(XO)----------+
                        | p1                    | p2
                +---------------+       +---------------+
                |               |       |               |
                |    Action1    |       |    Action2    |
                |               |       |               |
                +---------------+       +---------------+
                        |                       |
                        +---------(XO)----------+
                                    |
                            +---------------+
                            |               |
                            |      End      |
                            |               |
                            +---------------+
"""
###############################################
# 1 Define a model
p = Process("process")
p_or = p.XOr()
p1 = p_or.Process("p1")
p2 = p_or.Process("p2")
p_act1 = p1.Action("Action1")
p_act2 = p2.Action("Action2")
