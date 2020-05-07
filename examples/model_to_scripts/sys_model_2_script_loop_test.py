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
                                   (L)----------+
                                    | loop1     |
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
loop = p.Loop('loop1', times=2)
l_act3 = loop.Action("Action1")


###############################################
from script_generator import ScriptGenerator
sg = ScriptGenerator()
sg.run(p)

print(sg.script)