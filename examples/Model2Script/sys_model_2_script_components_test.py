from entity import *
from script_generator import ScriptGenerator

import examples.BlockModels.BD1_Two_Blocks_Test as b1

#########################################################

sg = ScriptGenerator()
sg.run(b1)

print(sg.script)
