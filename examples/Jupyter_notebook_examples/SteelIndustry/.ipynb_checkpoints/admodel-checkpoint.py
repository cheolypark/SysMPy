import os
import sys 
sys.path.insert(0, os.path.abspath('..\..\..\..\sysmpy'))  
from sysmpy import *

p = Process("Car")
p_or = p.Or()
p1 = p_or.Process("p1")
p2 = p_or.Process("p2")
p_act1 = p1.Action("Action1")
p_act2 = p2.Action("Action2")
