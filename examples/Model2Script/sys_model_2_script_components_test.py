from entity import *
from script_generator import ScriptGenerator

import BD1_Two_Blocks_Test

#########################################################

sg = ScriptGenerator()
sg.run(BD1_Two_Blocks_Test)

print(sg.script)
