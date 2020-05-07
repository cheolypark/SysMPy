from sysmpy import *
from script_generator import ScriptGenerator

import examples.action_models.AD5_Item_Flow_Test_2 as ad5

#########################################################

sg = ScriptGenerator()
sg.run(ad5)

print(sg.script)
