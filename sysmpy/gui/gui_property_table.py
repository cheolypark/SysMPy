from sysmpy.entity import *
from sysmpy.relationship import *
from sysmpy.gui.gui_mxgraph import GuiMXGraph


class GuiPropertyTable():
    def __init__(self):
        pass

    def get_chart_info(self, proc_en, width, height):
        # Copy a new process entity using the original process entity
        new_en = deepcopy(proc_en)

        # Set this with a root process flag
        new_en.is_root = True
        new_en.end.is_root = True

        # get list of properties which are updated by the simulation
        new_en.properties, _ = new_en.search(words_search=[Property])

        if new_en.properties is not None:
            property_list = [f"'{x.get_name_with_parent()}':0" for x in new_en.properties]
            prop_str = '{' + ", ".join(property_list) + '}'
            return prop_str

        return ''
