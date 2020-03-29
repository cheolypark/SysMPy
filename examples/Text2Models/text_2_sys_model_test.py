from sysmpy.entity import *
from script_to_model import SystemModelExtractor
from model_generator import ModelGenerator
from script_generator import ScriptGenerator

print('text to system models')

text = """
When constructing an architectural model, SAI should automatically optimize the spatial arrangement of the boxes and lines that make up the model in the modeling window by pressing the 'Model Space Optimization Button' to improve readability.
"""

text = """SAI should automatically optimize the box arrangement"""

# text = "Autonomous cars shift insurance liability toward manufacturers"
# txt = 'I do not know with whom I will go to the prom.'

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

