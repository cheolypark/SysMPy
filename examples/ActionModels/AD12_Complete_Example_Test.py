from entity import *
import asyncio
"""
                            +---------------+
                            |               |
                            |     start     |
                            |               |
                            +---------------+
                                    | process
                                    |
                                    ...
                                    ...
                                    ..
                                    |    
                                    |
                            +---------------+
                            |               |
                            |      End      |
                            |               |
                            +---------------+
"""
print('AD12_Complete_Example_Test')

###############################################
# 1 Define actions
p = Process("p1")
and_1 = p.And()
p1_1 = and_1.Process("p1.1")
p1_2 = and_1.Process("p1.2")
p1_3 = and_1.Process("p1.3")

or_1_1 = p1_1.Or()
p1_1_1 = or_1_1.Process("p1.1.1")
p1_1_2 = or_1_1.Process("p1.1.2")

func_1_1_1_1 = p1_1_1.Action("Function")
func_1_1_1_2 = p1_1_1.Action("Function")
func_1_1_2_1 = p1_1_2.Action("Function")

loop_proc = p1_2.Loop('loop_proc')
con_1_2 = loop_proc.Condition("Function")
p1_2_1 = con_1_2.Process("p1.2.1")
p1_2_2 = con_1_2.Process("p1.2.2")

p1_2_1.ExitLoop()
p1_2_2.Action("Function")

con_1_3 = p1_3.Condition("Function")
p1_3_1 = con_1_3.Process("p1.3.1")
p1_3_2 = con_1_3.Process("p1.3.2")
p1_3_3 = con_1_3.Process("p1.3.3")
p1_3_1.End()
act1_3_2_1 = p1_3_2.Action("Function")
act1_3_2_1 = p1_3_2.Action("Function")
act1_3_3_1 = p1_3_3.Action("Function")

r1_3_1 = Resource("Resource")

act1_3_3_1.seizes(r1_3_1)

r1_1_1 = Resource("Resource")

func_1_1_1_1.seizes(r1_1_1)

# i1_1_1 = Resource("Item")
# i1_1_2 = Resource("Item")

# func_1_1_1_1.sends(i1_1_1)
# func_1_1_1_2.triggered(i1_1_1)
# func_1_1_1_2.sends(i1_1_2)

asyncio.run(p.sim())
