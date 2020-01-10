from entity import *
import asyncio

"""
1. Define a simple system requirement 
"""
# Define requirements
r1 = Requirement("Req 1_1", des="The system shall fit into a size not exceeding 4", range=[1, 2, 3, 4])

"""
2. Define an action model 
                +---------------+
                |               |
                |     start     |
                |               |
                +---------------+
                        | process 1
                        |
                +---------------+
                |               |
                |   Action1_1   |
                |               |        
                +---------------+        
                        |
                        |
                +---------------+
                |               |
                |   Action1_2   |
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
# Define processes and actions
p = Process("process 1")
act1 = p.Action('action 1_1')
act2 = p.Action('action 1_2')


"""
3. Define a physical model (i.e., Block Diagram)
                +---------------+
                |               |
                |     Com1      |
                |               |
                +---------------+
                        O
                        | 
                        +-----------------------+
                        |                       |
                +---------------+       +---------------+
                |               |       |               |
                |    Com1_1     |       |    Com1_2     |
                |               |       |               |
                +---------------+       +---------------+
"""
# Define components
c1 = Component("Com1", des="This is a component")
c1_1 = Component("Com1_1", des="This is another component")
c1_2 = Component("Com1_2", des="This is another component")
c1.decomposes(c1_1)
c1.decomposes(c1_2)

# Make relationships between components and processes
c1.performs(p)
c1_1.performs(act1)
c1_2.performs(act2)

# Make properties for components
pro1 = c1.Property("Total size")
pro1_1 = c1_1.Property("Size", range=[1, 2, 3])
pro1_2 = c1_2.Property("Size", range=[1, 2, 3])


"""
4. Define a link between components and requirements
                +---------------+
                |               |
                |     Com1      |
                |               |
                +---------------+
                        O
                        |  
                        |                      
                +---------------+        
                |               |       
                |    Req 1_1    |       
                |               |        
                +---------------+       
"""
# Make relationships between components and requirements
pro1.traced_from(r1)

"""
5. Perform ExSim (i.e., model center)
                    +---------------+   
                    |               |
                    |    Com 1_1    |
                    |               |
                    +---------------+
                    |     Size      |
                    +---------------+          
                                   \
                                    \
        +---------------+            +--------------------+            +---------------+
        |               |            |       Action       |            |               |
        |     Start     |----------->|        for         |----------->|      End      |
        |               |            |  size calculation  |            |               |
        +---------------+            +--------------------+            +---------------+
                                    /                      \   
                                   /                        \
                    +---------------+                       +---------------+
                    |               |                       |               |
                    |    Com 1_2    |                       |     Com 1     |
                    |               |                       |               |
                    +---------------+                       +---------------+
                    |     Size      |                       |   Total size  |
                    +---------------+                       +---------------+
"""
# Define processes and actions
p_ex = Process("ExSim process 1")
act_ex = p_ex.Action('size calculator')

act_ex.receives(pro1_1)
act_ex.receives(pro1_2)
act_ex.sends(pro1)

# External Simulation Script ######################################
def exsim_function1(io):
    i1, i2, out = io.get("Com1_1.Size"), io.get("Com1_2.Size"), io.get("Com1.Total size")
    i1_value = i1.get_random_value()
    i2_value = i2.get_random_value()

    print(f"{i1.value}, {i2.value}")

    out.value = i1_value + i2_value

    print("out: " + str(out.value))


# Script end ##################################
act_ex.func(exsim_function1)

###############################################
# 2 run simulation
asyncio.run(p_ex.sim())

"""
6. Check requirements with the simulation results
"""
r1.check_property()
