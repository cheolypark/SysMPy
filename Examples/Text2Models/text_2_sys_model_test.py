from entity import *


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
                |     Action1   |
                |               |        
                +---------------+        
                        |
                        |
                +---------------+
                |               |
                |     Action2   |
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
print('text to system models')

text = """
When constructing an architectural model, SAI should automatically optimize the spatial arrangement of the boxes and lines that make up the model in the modeling window by pressing the 'Model Space Optimization Button' to improve readability.
"""


# 1 Define actions
p = Process("process")
act1 = p.Action("Action1")
act2 = p.Action("Action2")
act3 = p.Action("Action3")

###############################################
# 2 run simulation
# Entity._debug_mode = True
asyncio.run(p.sim())

print(p.get_action_times())


