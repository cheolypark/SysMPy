from entity import *
from examples.Projects.AD_Folder.AD1 import *
from examples.Projects.BD_Folder.BD1 import *

# Get the 'Action1' entity from 'examples.Projects.AD_Folder.AD1'
a1_from_AD1 = entity_db.get('Action1', path='examples.Projects.AD_Folder.AD1')
print(a1_from_AD1)

# Get the 'Action2' entity from 'examples.Projects.AD_Folder.AD1'
a1_from_AD2 = entity_db.get('Action2', path='examples.Projects.AD_Folder.AD1')
print(a1_from_AD2)

# Get the 'Action1' entity from 'examples.Projects.BD_Folder.BD1'
a2 = entity_db.get('Action1', path='examples.Projects.BD_Folder.BD1')
print(a2)

# Get the 'Action1' entity using a global ID
a3 = entity_db.get_by_id(f'ID{id(a1_from_AD1)}')
print(a3)

# Remove the 'Action1' entity
entity_db.remove_entity(a3)
print(a3)

# Remove the 'process' entity in 'examples.Projects.AD_Folder.AD1'
p1 = entity_db.get('process', path='examples.Projects.AD_Folder.AD1')
entity_db.remove_entity(p1)
print(p1)