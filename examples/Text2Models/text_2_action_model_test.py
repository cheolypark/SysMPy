from sysmpy.entity import *
from script_to_model import SystemModelExtractor
from model_generator import ModelGenerator
from script_generator import ScriptGenerator

texts = ["System should automatically optimize the spatial arrangement of the boxes.",
         "System shall deliver three small products to each green level customer.",
         "System shall deliver two larger products to each gold level customer.",
         "System shall complete all product deliveries between 9PM Dec 24 and 6 AM Dec 25."]

# 1. Perform SystemModelExtractor
for t in texts:
    sp = SystemModelExtractor(t)
    model_info = sp.run()

    # 3. Perform ModelGenerator for action model
    mg = ModelGenerator()
    am = mg.to_action_model(model_info)
    print(am)

# 4. covert the action model in the memory to an action model script
sg = ScriptGenerator()
script = sg.run(am)
print(script)
