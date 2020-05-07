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
                |    Action1    |-------+
                |               |       | 
                +---------------+       | 
                        |             (Item1)
                        |               |
                +---------------+    (Trigger)
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
print('This requires a gui web server.')
print('Execute the gui web server using the file "run_gui_server_test.py" in the gui directory')

###############################################
# 1 Define a model
p = Process("process 1")
act1 = p.Action("Action1")
act2 = p.Action("Action2")

i1 = Item("Item1")
i1.Property('Size', range=[1, 2, 3])
i1.Property('Weight', range=[1, 2, 3])
act1.sends(i1)
act2.triggered(i1)

###############################################
# 2 Run a simulation
asyncio.run(p.sim(until=100, property_view=True, print_out=True))
