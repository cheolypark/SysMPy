from sysmpy import *
from examples.script_management.model_hierarchy import *

try:
    # 1 Define actions
    act1_1 = act3.Process("Action1")
    act2_1 = act3.Process("Action2")
    act3_1 = act3.Process("Action3")
except NameError as error:
    # Output expected NameErrors.
    print(error.args)
except Exception as exception:
    print('Output unexpected Exceptions')

print(p)