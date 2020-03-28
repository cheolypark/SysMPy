from entity import *
from script_to_model import SystemModelExtractor
from model_generator import ModelGenerator

"""
                +---------------+
                |               |
                |     start     |
                |               |
                +---------------+
                        | process
                        |
                +---------------+
                |               |
                |     Action1   |
                |               |        
                +---------------+        
                        |
                        |
                +---------------+
                |               |
                |     Action2   |
                |               |        
                +---------------+        
                        |
                        | 
                +---------------+
                |               |
                |      End      |
                |               |
                +---------------+
"""
print('text to system models')

text = """
When constructing an architectural model, SAI should automatically optimize the spatial arrangement of the boxes and lines that make up the model in the modeling window by pressing the 'Model Space Optimization Button' to improve readability.
"""

text = """SAI should automatically optimize the box arrangement"""

# text = "Autonomous cars shift insurance liability toward manufacturers"
# txt = 'I do not know with whom I will go to the prom.'
sp = SystemModelExtractor(text)
# sp.print()
model_info = sp.run()
print(model_info)

mg = ModelGenerator()
req = mg.to_requirement(model_info)
print(req)

import pathlib
print(pathlib.Path().absolute())
print(pathlib.Path(__file__).parent.absolute())

p = Process("process")


req = Requirement('sys')

# en = entity_database.get('sys')
# print(en)
