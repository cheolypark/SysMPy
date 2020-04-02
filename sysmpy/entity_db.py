import traceback
import os
from sysmpy.util import *

entity_database = []

def store_entity(self):
    """ All entities created are stored """
    entity_database.append(self)

def remove_entity(self):
    # Remove the self from the entity which is using the self
    for name, inv_relations in self.inv_relation.items():
        for rel in inv_relations:
            rel_oposites = rel.start.relation[rel.re_name]
            remove_list = []
            for rel_oposite in rel_oposites:
                if self == rel_oposite.end:
                    remove_list.append(rel_oposite)

            for r in remove_list:
                rel_oposites.remove(r)

    # Remove the self from the entity which is used by the self
    for name, relations in self.relation.items():
        for rel in relations:
            rel_oposites = rel.end.inv_relation[rel.inv_name]
            remove_list = []
            for rel_oposite in rel_oposites:
                if self == rel_oposite.start:
                    remove_list.append(rel_oposite)

            for r in remove_list:
                rel_oposites.remove(r)

    entity_database.remove(self)

def clear_all():
    entity_database.clear()

def get(name_entity, path=None, comparing_method=None):
    """This returns instances of an entity
    There are two ways of finding entities.
    (1) get an object by an entity name, which was created in the same directory
        e.g.,) 'component_name1.item_name2'
    (2) get an object by an entity name, which was created from a different directory
        e.g.,) 'examples.folder.module.component_name1.item_name2'
                [         path        ][      entity name       ]

    :param name_entity: a name that we want to find
    :param path: a path where the object was created
    :return: a founded object or a list of objects
    """

    if path is None:
        # Find a module which is using this get function:
        # - last element ([-1]) is me, the one before ([-2]) is my caller.
        # - The first element in caller's data is the filename
        caller_path = traceback.extract_stack()[-2][0]
        caller, file_extension = os.path.splitext(caller_path)
    else:
        caller = path

    l = name_entity.split('.')

    cur_obj = None
    for i in l:
        if cur_obj is None:
            cur_obj = get_op(comparing_method, i, caller)
        else:
            cur_obj = get_by_relationship(cur_obj, i, 'contains')

    return cur_obj


def get_by_id(id_entity):
    """This returns instances of an entity
    (1) get an object by an instance name
        e.g.,) 'instance_name_id_001'

    :param name_entity: a name that we want to find
    :param path: a path where the object was created
    :return: a founded object or a list of objects
    """

    return get(id_entity, comparing_method='ByID')

def get_by_relationship(obj_parent, name_target, relationship):
    """
    This returns instances of an entity in a parent entity by using the relationship name
    e.g.,)
    cur_obj = Component()
    Entity.get_by_relationship(cur_obj, 'size', 'contains')

    """

    if relationship in obj_parent.relation:
        relations = [x.end for x in obj_parent.relation[relationship]]
        if relations is not None:
            e = [x for x in relations if x.name == name_target]
            if e is None:
                return None
            elif len(e) == 1:
                return e[0]
            elif len(e) == 0:
                return None
            else:
                return e

def get_op(comparing_method, target, caller=None):
    """ This returns instances of an entity by searching in the entity_db"""
    if comparing_method is None:
        if caller is None:
            e = [x for x in entity_database if x.name == target]
        elif caller is not None:
            e = [x for x in entity_database if x.name == target and is_path_same(caller, x.module)]
    elif comparing_method == 'ByID':
        e = [x for x in entity_database if f'ID{id(x)}' == target]

    if e is None:
        return None
    elif len(e) == 1:
        return e[0]
    elif len(e) == 0:
        return None
    else:
        return e


def get_by_type(type_entity):
    """ This returns instances of an entity by the entity type"""
    e = [x for x in entity_database if isinstance(x, type_entity)]
    if e is None:
        return None
    else:
        return e


def is_same(e1, e2):
    """
    Elements in entity can be cloned by a simulation module or viewer module.
    In some cases, their same identity should be checked.
    """
    if e1.name == e2.name and e1.module == e2.module:
        return True
    return False