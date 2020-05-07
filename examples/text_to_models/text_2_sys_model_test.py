from script_to_model import SystemModelExtractor
from model_generator import ModelGenerator

print('text to system models')

# text = "Autonomous cars shift insurance liability toward manufacturers"
# text = "System should automatically optimize the spatial arrangement of the boxes."
# text = "System shall deliver three small products to each green level customer."
text = "System shall deliver two larger products to each gold level customer."
# text = "System shall complete all product deliveries between 9PM Dec 24 and 6 AM Dec 25."

# 1. Perform SystemModelExtractor
sp = SystemModelExtractor(text)
model_info = sp.run()
print(model_info)

# 2. Perform ModelGenerator for requirement
mg = ModelGenerator()
req = mg.to_requirement(model_info)
print(req)

# # 3. Perform ModelGenerator for action model
# am = mg.to_action_model(model_info)
# print(am)
#
# # 4. covert the action model in the memory to an action model script
# sg = ScriptGenerator()
# script = sg.run(am)
# print(script)
