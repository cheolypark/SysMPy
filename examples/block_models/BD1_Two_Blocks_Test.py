from sysmpy import *


"""
                +---------------+
                |               |
                |    System 1   |
                |               |
                +---------------+
                        O
                        | 
                        +---------------------+
                        |                     |
                +---------------+     +---------------+
                |               |     |               |  
                |  Component 1  |     |  Component 1  |  
                |               |     |               |
                +---------------+     +---------------+
"""

# Define components
c1 = Component("System 1", des="This is a system")
c1_1 = c1.Component("Component 1", des="This is another component")
c1_2 = c1.Component("Component 1", des="This is another component")

print(c1)
