from sysmpy import *
from examples.script_management.AD_Folder.AD1 import *
from examples.script_management.BD_Folder.BD1 import *

# 1 Define actions
p_1 = Process("process")
act1_1 = p_1.Action("Action1")
act2_1 = p_1.Action("Action2")
act3_1 = p_1.Action("Action3")

edb.get_cloned_db(path='E:\SW-SysMPy\SysMPy\examples\script_management\AD_Folder\AD1')

# Get the 'Action1' entity
a1 = edb.get('Action1')
print(a1)

# Get the 'Action1' entity from 'examples.script_management.AD_Folder.AD1'
a1_from_AD1 = edb.get('Action1', path='E:\SW-SysMPy\SysMPy\examples\script_management\AD_Folder\AD1')
print(a1_from_AD1)

clone_db = edb.get_cloned_db(path='E:\SW-SysMPy\SysMPy\examples\script_management\AD_Folder\AD1')

# Get the 'Action1' entity using a global ID
a3 = edb.get(f'ID{id(a1)}')
print(a3)

# Get entity by the hierarchical name
en = edb.get('process.Action3')
print(en)

# Remove the 'Action1' entity
edb.remove_entity(a3)
print(a3)

# Remove the 'process' entity in 'examples.script_management.AD_Folder.AD1'
p1 = edb.get('process')
edb.remove_entity(p1)
print(p1)