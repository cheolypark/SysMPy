from sysmpy import *
from script_generator import ScriptGenerator

import examples.block_models.BD1_Two_Blocks_Test as b1

#########################################################

sg = ScriptGenerator()
sg.run(b1)

print(sg.script)
