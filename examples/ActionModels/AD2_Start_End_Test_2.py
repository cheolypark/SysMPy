from sysmpy import Process
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
print('AD2_Start_End_Test_2')

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


