from entity import *
from script_generator import ScriptGenerator

import AD5_Item_Flow_Test_2

#########################################################

sg = ScriptGenerator()
sg.run(AD5_Item_Flow_Test_2)

print(sg.script)
