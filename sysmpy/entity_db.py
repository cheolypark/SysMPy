import traceback
import os
from sysmpy.util import *
from copy import deepcopy


class EntityDB():
    def __init__(self):
        self.entity_database = {}

    def store_entity(self, en):
        """ All entities created are stored """
        if hasattr(en, 'module'):
            if en.module not in self.entity_database:
                self.entity_database[en.module] = []

            self.entity_database[en.module].append(en)

    def get(self, name, path=None):
        """
        The ways getting entity objects
        (1) By class types
            get([Action, Item])
        (2) By relation types
            get_relation([sends, receives])
        (3) By entity names
            get(['action1')
        (4) By id
            get(['ID902342'])
        """

        is_Ipython = False

        if path is None:
            path, _ = os.path.splitext(traceback.extract_stack()[-2][0])

            # Check Ipython
            if 'ipython-input' in path:
                is_Ipython = True

        e = []
        for file, entities in self.entity_database.items():
            if file == path or is_Ipython is True:
                for entity in entities:
                    e1, _ = entity.search(words_search=[name])
                    e += e1

        # make unique elements
        e = list(set(e))

        if len(e) == 1:
            return e[0]
        elif len(e) == 0:
            return None
        else:
            return e

    def get_by_relationship(self, obj_parent, name_target, relationship):
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

    def get_op(self, comparing_method, target, caller=None):
        """ This returns instances of an entity by searching in the entity_db"""
        if comparing_method is None:
            if caller is None:
                e = [x for x in self.entity_database if x.name == target]
            elif caller is not None:
                e = [x for x in self.entity_database if x.name == target and is_path_same(caller, x.module)]
        elif comparing_method == 'ByID':
            e = [x for x in self.entity_database if f'ID{id(x)}' == target]

        if e is None:
            return None
        elif len(e) == 1:
            return e[0]
        elif len(e) == 0:
            return None
        else:
            return e

    def remove_entity(self, en, path=None):
        # Disconnect this from which entities related to this on the inverse relation
        for name, inv_relations in en.inv_relation.items():
            for rel in inv_relations:
                rel_oposites = rel.start.relation[rel.re_name]
                remove_list = []
                for rel_oposite in rel_oposites:
                    if en == rel_oposite.end:
                        remove_list.append(rel_oposite)

                for r in remove_list:
                    rel_oposites.remove(r)

        # Disconnect this from which entities related to this on the relation
        for name, relations in en.relation.items():
            for rel in relations:
                rel_oposites = rel.end.inv_relation[rel.inv_name]
                remove_list = []
                for rel_oposite in rel_oposites:
                    if en == rel_oposite.start:
                        remove_list.append(rel_oposite)

                for r in remove_list:
                    rel_oposites.remove(r)

        if path is None:
            path, _ = os.path.splitext(traceback.extract_stack()[-2][0])

        entities = self.entity_database[path]
        if en in entities:
            entities.remove(en)

    def is_same(self, e1, e2):
        """
        Elements in entity can be cloned by a simulation module or viewer module.
        In some cases, their same identity should be checked.
        """
        if e1.name == e2.name and e1.module == e2.module:
            return True
        return False

    def get_clone_db(self, path=None):
        if path in self.entity_database:
            en = self.entity_database[path]
            clone_db = deepcopy(en)

        return clone_db


edb = EntityDB()