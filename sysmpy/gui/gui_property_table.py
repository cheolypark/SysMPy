from sysmpy.entity import *
from copy import deepcopy


class GuiPropertyTable():
    def __init__(self):
        pass

    def get_chart_info(self, proc_en, width=700, height=600):
        # Copy a new process entity using the original process entity
        new_en = deepcopy(proc_en)

        # Set this with a root process flag
        new_en.is_root = True
        new_en.end.is_root = True

        # 1. Include properties for the table variables
        # get list of properties which are updated by the simulation
        new_en.properties, _ = new_en.search(words_search=[Property])

        property_list = None
        if new_en.properties is not None:
            property_list = [f"'{x.hierarchical_name}':0" for x in new_en.properties]

        # 2. Include requirement properties for the table variables
        requirements, _ = new_en.search(words_search=[Requirement])
        for requirement in requirements:
            if 'traced to' in requirement.inv_relation:
                rel = [x.start for x in requirement.inv_relation['traced to']]
                if len(rel) > 0:
                    property_list.append(f"'{requirement.hierarchical_name}':'Passed'")

        if property_list is not None:
            prop_str = '{' + ", ".join(property_list) + '}'
            return prop_str

        return ''
