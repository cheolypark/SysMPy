from sysmpy.entity import *
from script_to_model import SystemModelExtractor
from model_generator import ModelGenerator
from script_generator import ScriptGenerator

print('text to system models')

text = "System should automatically optimize the spatial arrangement of the boxes."

# 1. Perform SystemModelExtractor
sp = SystemModelExtractor(text)
model_info = sp.run()
print(model_info)

# 2. Perform ModelGenerator for requirement
mg = ModelGenerator()
req = mg.to_requirement(model_info)
print(req)

# 3. Perform ModelGenerator for action model
am = mg.to_action_model(model_info)
print(am)

# 4. covert the action model in the memory to an action model script
sg = ScriptGenerator()
script = sg.run(am)
print(script)
