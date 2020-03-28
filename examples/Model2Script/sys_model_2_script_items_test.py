from entity import *
from script_generator import ScriptGenerator

import examples.ActionModels.AD5_Item_Flow_Test_2 as ad5

#########################################################

sg = ScriptGenerator()
sg.run(ad5)

print(sg.script)
