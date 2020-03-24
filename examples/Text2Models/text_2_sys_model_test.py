from entity import *
from script_to_model import SystemModelExtractor

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

text = """SAI should automatically optimize the box arrangement"""

# text = "Autonomous cars shift insurance liability toward manufacturers"
# txt = 'I do not know with whom I will go to the prom.'
sp = SystemModelExtractor(text)
sp.print()
print(sp.run())


# 1 Define actions
# p = Process("process")
# act1 = p.Action("Action1")
# act2 = p.Action("Action2")
# act3 = p.Action("Action3")
#hi
# ###############################################
# # 2 run simulation
# # Entity._debug_mode = True
# asyncio.run(p.sim())
#
# print(p.get_action_times())


