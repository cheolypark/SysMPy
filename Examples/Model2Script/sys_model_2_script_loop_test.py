from entity import *
import asyncio
from entity import *


"""
                            +---------------+
                            |               |
                            |     start     |
                            |               |
                            +---------------+
                                    | process1
                                    |
                                   (L)----------+
                                    | process1_1|
                            +---------------+   |
                            |               |   |
                            |    Action1    |   |
                            |               |   |
                            +---------------+   |
                                    |           |
                                   (L)----------+
                                    |   2 times
                                    |
                            +---------------+
                            |               |
                            |      End      |
                            |               |
                            +---------------+
"""
print('system models to scripts')

###############################################
# 1 Define actions
p = Process("process")

p_and = p.And()

p1 = p_and.Process("process 1")
p2 = p_and.Process("process 2")
p_act1 = p1.Action("Action 1")
p_act2 = p1.Action("Action 2")

loop = p2.Loop(times=2)
p1_1 = loop.Process("process1_1")

l_act3 = p1_1.Action("action 3")


###############################################
from script_generator import ScriptGenerator
sg = ScriptGenerator()
sg.run(p)

print(sg.script)