import os
import sys 
sys.path.insert(0, os.path.abspath('..\..\..\..\sysmpy'))  
from sysmpy import *

r1 = Requirement("Req 1_1", des="The system shall fit into a size not exceeding 4", range=[1, 2, 3, 4])
p = Process("process")
act1 = p.Action("Action1")
act2 = p.Action("Action2")
act3 = p.Action("Action3")
# Define components
c1 = Component("Com1", des="This is a system")
c1_1 = c1.Component("Com1_1", des="This is another component")
c1_2 = c1.Component("Com1_2", des="This is another component")

# Make relationships between components and processes/actions
c1.performs(p)
c1_1.performs(act1)
c1_2.performs(act2)

# Make properties for components
pro1 = c1.Property("Total size")
pro1_1 = c1_1.Property("Size", range=[1, 2, 3])
pro1_2 = c1_2.Property("Size", range=[1, 2, 3])

# Make relationships between components and requirements
pro1.traced_from(r1)

# Define processes and actions
p_ex = Process("ExSim process 1")
act_ex = p_ex.Action('size calculator')

act_ex.receives(pro1_1)
act_ex.receives(pro1_2)
act_ex.sends(pro1)


# External simulations Script  
def exsim_function1(io):
    i1, i2, out = io.get("Com1.Com1_1.Size"), io.get("Com1.Com1_2.Size"), io.get("Com1.Total size")
    i1_value = i1.get_random_value()
    i2_value = i2.get_random_value()
    
#     print(f"{i1.value}, {i2.value}")

    out.value = i1_value + i2_value

#     print("out: " + str(out.value))
    
# Script end  
act_ex.func(exsim_function1)

# await p_ex.sim(print_out=True)