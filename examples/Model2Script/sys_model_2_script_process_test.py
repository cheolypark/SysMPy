from entity import *
from script_generator import ScriptGenerator


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
print('system models to scripts')

# 1 Define actions
p = Process("process")
act1 = p.Action("Action1")
act2 = p.Action("Action2")

# p.init_sim_network()

sg = ScriptGenerator()
sg.run(p)

print(sg.script)
