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






#
#
#
# # 1 Define blocks
# p = Process("process 1")
#
# # print(__file__)
# # print(p.__class__.__name__)
# # print(sys._getframe().f_code.co_name)
# import inspect
#
# ###############################################
# # Return a source file path
# print(inspect.getfile(p.__class__))
#
# ###############################################
# # Return a source file path
# print(inspect.getsourcefile(Process))
#
# ###############################################
# # Return a source code for a class
# print(inspect.getsourcelines(Process))
#
# ###############################################
# # Return a source code for a class
# print(inspect.getsource(Process))
#
# ###############################################
# # Return a module from an object
# print(inspect.getmodule(p))
#
#
# ##############################################################################################
# # Classes and functions
#
# ###############################################
# # Return a module from an object
# print(inspect.getclasstree(Process))





