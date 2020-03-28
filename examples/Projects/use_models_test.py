from entity import *
from examples.Projects.AD_Folder.AD1 import *
from examples.Projects.BD_Folder.BD1 import *

a1 = entity_db.get('Action1', path='examples.Projects.AD_Folder.AD1')
print(a1)

a2 = entity_db.get('Action1', path='examples.Projects.BD_Folder.BD1')
print(a2)

a3 = entity_db.get_by_id(f'ID{id(a1)}')
print(a3)
