from sysmpy.entity import *
from sysmpy.relationship import *
from sysmpy.gui.gui_mxgraph import GuiMXGraph


class GuiMXGraphBlockDiagram(GuiMXGraph):
    def __init__(self):
        super().__init__()

    ########################################################################
    # Graphic Methods
    #
    def init_graphic_variables(self, entity):
        entity.margin_x = 40
        entity.margin_y = 6
        entity.node_width = 80
        entity.node_height = 30

        # if isinstance(entity, Action) or isinstance(entity, Condition):
        #     entity.margin_y = 6
        #     entity.node_height = 60

        # if isinstance(entity, Process) or isinstance(entity, Process_END):
        #     if entity.is_root is False:
        #         entity.margin_x = 40
        #         entity.margin_y = 5
        #         entity.node_width = 80
        #         entity.node_height = 10

        entity.boundary_width = 0
        entity.boundary_height = 0
        entity.boundary_x = 0
        entity.boundary_y = 0
        entity.width_half = (entity.node_width + entity.margin_x * 2) / 2
        entity.height_half = (entity.node_height + entity.margin_y * 2) / 2
        entity.width = entity.node_width + entity.margin_x * 2
        entity.height = entity.node_height + entity.margin_y * 2
        entity.center_x = 0
        entity.center_y = 0
        entity.root_x = 0

    def make_node(self, en, x=None, y=None):
        # var v1 = graph.insertVertex(parent, null, 'Hello,', 20, 20, 80, 30) \\n
        if x is None:
            x = en.center_x
        if y is None:
            y = en.center_y

        node_width = en.node_width
        node_height = en.node_height
        label = en.name
        name = en.get_numbered_name()

        if isinstance(en, Action) or isinstance(en, Condition):
            node_width = en.node_width
            node_height = en.node_height
        elif isinstance(en, And) or isinstance(en, And_END) or isinstance(en, Condition_END) or \
                isinstance(en, Loop) or isinstance(en, Loop_END) or \
                isinstance(en, Or) or isinstance(en, Or_END):
            node_width = en.node_height
            node_height = en.node_height
        elif isinstance(en, Process) or isinstance(en, Process_END):
            if en.is_root is True:
                node_width = en.node_height
                node_height = en.node_height
            else:
                node_width = 0
                node_height = 0
        elif isinstance(en, Item) or isinstance(en, Resource):
            node_width = en.node_width - 18
            node_height = en.node_height - 10

        if isinstance(en, Process):
            label = ''
        if isinstance(en, Process_END):
            label = ''
        elif isinstance(en, And):
            label = 'A'
        elif isinstance(en, Or) or isinstance(en, Or_END) or isinstance(en, Condition_END) or isinstance(en, And_END):
            label = 'OR'
        elif isinstance(en, Loop) or isinstance(en, Loop_END):
            label = 'L'

        # compensate the node position after resizing
        x += (en.node_width - node_width)/2
        y += (en.node_height - node_height)/2

        node = ''
        s_name = self.safe_name(name)
        if s_name not in self.mx_nodes:
            self.mx_nodes.append(s_name)
            node = f"var {s_name} = graph.insertVertex(parent, '{name}', '{label}', {x}, {y}, {node_width}, {node_height}, '{type(en).__name__}') /n "
            # node += f"{s_name}.geometry.alternateBounds = new mxRectangle(0, 0, 60, 30) /n "
        #     v2.geometry.alternateBounds = new mxRectangle(0, 0, 80, 30);
        # print(node)

        return node

    def make_edge(self, s, e, point=None):
        # var e1 = graph.insertEdge(parent, null, '', v1, v2)\\n
        s_name = self.safe_name(s.get_numbered_name())
        e_name = self.safe_name(e.get_numbered_name())
        # edge = f"var {s}_{e} = graph.insertEdge(parent, null, '', {s}, {e}, 'verticalAlign=top') /n "
        # edge += f'{s}_{e}.geometry.points = [new mxPoint({s}.geometry.x + 10, 10)]/n'

        if s.is_root is True or e.is_root is True:
            edge_style = 'Arrow_Edge_Process'
        elif isinstance(s, Item):
            edge_style = 'Arrow_Edge_Item'
        elif isinstance(e, Item):
            edge_style = 'Edge_Item'
        elif isinstance(s, Resource):
            edge_style = 'Arrow_Edge_Resource'
        elif isinstance(e, Resource):
            edge_style = 'Edge_Resource'
        elif isinstance(s, Loop_END) and isinstance(e, Loop):
            edge_style = 'Arrow_Edge_Loop'
        else:
            edge_style = None

        if edge_style is not None:
            edge = f"var {s_name}_{e_name} = graph.insertEdge(parent, null, '', {s_name}, {e_name}, '{edge_style}' ) /n "
        else:
            edge = f"var {s_name}_{e_name} = graph.insertEdge(parent, null, '', {s_name}, {e_name} ) /n "

        if point is not None:
            edge += f'{s_name}_{e_name}.geometry.points = [new mxPoint( {point}, 0 )]/n'
        # e = graph.insertEdge(lane2a, null, 'No', step444, end3, 'verticalAlign=top');
        # e.geometry.points = [new mxPoint(step444.geometry.x + step444.geometry.width / 2,
        #                                  end3.geometry.y + end3.geometry.height / 2)];

        # 'shape=link;labelBackgroundColor=#FFFFFF;'

        # print(edge)
        return edge

    def get_mxgraph_string(self, entity, entities, list_actions):
        str = ''
        flows = [r for r in entity.relation['flows'] if isinstance(r, Flow)]
        for i, f in enumerate(flows):
            str += self.make_node(f.start)
            str += self.make_node(f.end)
            str += self.make_edge(f.start, f.end)

        for e in entities:
            if 'flows' in e.relation:
                flows = [r for r in e.relation['flows'] if isinstance(r, Flow)]
                for i, f in enumerate(flows):
                    str += self.make_node(f.start)
                    str += self.make_node(f.end)
                    if isinstance(f.start, Loop_END) and isinstance(f.end, Loop):
                        str += self.make_edge(f.start, f.end, point=f.start.center_x+f.start.node_width+20)
                    else:
                        str += self.make_edge(f.start, f.end)

        # For items
        for action in list_actions:
            receiving_items = []

            if 'receives' in action.relation:
                receiving_items += [r.end for r in action.relation['receives'] if isinstance(r, Receives)]

            if 'consumes' in action.relation:
                receiving_items += [r.end for r in action.relation['consumes'] if isinstance(r, Consumes)]

            y_pos = 0
            for item in receiving_items:
                self.init_graphic_variables(item)

                if 'sent from' in item.inv_relation:
                    sender = item.inv_relation['sent from'][0].start

                if 'produced by' in item.inv_relation:
                    sender = item.inv_relation['produced by'][0].start

                direction = action.center_x - sender.center_x
                if direction > 10:
                    item.center_x = action.center_x - action.boundary_width/2
                elif direction < -10:
                    item.center_x = action.center_x + action.boundary_width/2
                else:
                    item.center_x = action.center_x - action.boundary_width/2

                item.center_y = action.center_y

                str += self.make_node(item, item.center_x, item.center_y + y_pos)
                str += self.make_edge(sender, item)
                str += self.make_edge(item, action)

                y_pos -= item.height_half

        return str

    def find_size_and_root_x(self, entity):
        # Init Graphic variables
        self.init_graphic_variables(entity)
        if hasattr(entity, 'end'):
            self.init_graphic_variables(entity.end)

        # Set Graphic variables
        largest_child_width = entity.width # The default size is its size
        largest_child_height = entity.height
        largest_root_x = entity.width_half
        first_root_x = 0
        last_root_x = 0
        all_child_width = 0
        all_child_height = 0

        if 'contains' in entity.relation:
            children = [r for r in entity.relation['contains'] if isinstance(r, Contains)]
            for i, c in enumerate(children):
                child = c.end
                self.find_size_and_root_x(child)

                # get children's size information
                largest_child_width = max(child.boundary_width, largest_child_width)
                largest_child_height = max(child.boundary_height, largest_child_height)
                largest_root_x = max(child.root_x, largest_root_x)
                all_child_width += child.boundary_width
                all_child_height += child.boundary_height
                if i == 0:
                    first_root_x = child.root_x
                elif i == (len(children)-1):
                    last_root_x = child.root_x

        # find boundary size and root X
        if isinstance(entity, Action):
            entity.boundary_width = entity.width
            entity.boundary_height = entity.height
            entity.root_x = entity.boundary_width/2
        elif isinstance(entity, And) or isinstance(entity, Condition) or isinstance(entity, Or):
            entity.boundary_width = all_child_width
            entity.boundary_height = largest_child_height + (entity.height)*2 # itself and its End pair
            entity.root_x = (all_child_width - last_root_x - first_root_x)/2 + first_root_x
        elif isinstance(entity, Process) or isinstance(entity, Loop):
            entity.boundary_width = largest_child_width
            entity.boundary_height = all_child_height + (entity.height)*2 # itself and its End pair
            entity.root_x = largest_root_x

        # print(f'{entity.name} boundary_width[{entity.boundary_width}] boundary_height[{entity.boundary_height}] root_x[{entity.root_x}]')

    def find_center(self, entity, parent, pre_edge_x, pre_edge_y, list_actions):
        # print(f'{entity.name}')

        # find center_x and center_y
        if isinstance(entity, Action):
            if 'receives' or 'triggered by' or 'consumes' or 'seizes' in entity.relation:
                list_actions.append(entity) # list_actions is used for item positioning later

            entity.center_x = parent.center_x
            entity.center_y = pre_edge_y + entity.height_half
        elif isinstance(entity, And) or isinstance(entity, Condition) or isinstance(entity, Or):
            entity.center_x = parent.center_x
            entity.center_y = pre_edge_y + entity.height_half
        elif isinstance(entity, Loop):
            entity.center_x = parent.center_x
            entity.center_y = pre_edge_y + entity.height_half#parent.center_y + entity.height
        elif isinstance(entity, Process):
            if isinstance(parent, And) or isinstance(parent, Condition) or isinstance(parent, Or) or isinstance(parent, Loop):
                entity.center_x = parent.boundary_x + pre_edge_x + entity.root_x
            else:
                entity.center_x = pre_edge_x + entity.root_x

            if parent is not None:
                entity.center_y = parent.center_y + entity.height
            else:
                entity.center_y = entity.height

        entity.boundary_x = entity.center_x - entity.root_x
        pre_edge_x = 0
        pre_edge_y = entity.center_y + entity.height_half

        if 'contains' in entity.relation:
            children = [r for r in entity.relation['contains'] if isinstance(r, Contains)]
            for i, c in enumerate(children):
                child = c.end

                child_x, child_y = self.find_center(child, entity, pre_edge_x, pre_edge_y, list_actions)

                # pre_y += child.center_y
                pre_edge_x += child.boundary_width
                pre_edge_y = child_y

        # If there is an End pair.
        if 'pairs' in entity.relation:
            end_entity = entity.relation['pairs'][0].end
            end_entity.center_x = entity.center_x
            if isinstance(parent, And) or isinstance(parent, Condition) or isinstance(parent, Or):
                end_entity.center_y = parent.center_y + parent.boundary_height - parent.height - end_entity.height
            else:
                end_entity.center_y = entity.center_y + entity.boundary_height - end_entity.height

            pre_edge_y = end_entity.center_y + end_entity.height_half
            # print(end_entity.name, end_entity.center_x, end_entity.center_y)

        # print(entity.name, entity.center_x, entity.center_y)
        return pre_edge_x, pre_edge_y

    def get_mxgraph(self, entity):
        entity.numbering('A')

        # Set this with a root process flag
        entity.is_root = True
        entity.end.is_root = True

        # 1. Find size and root_x of nodes
        self.find_size_and_root_x(entity)

        # 2. Find center_x and center_y for dynamic entity (e.g., Process, Action, and Condition)
        list_actions = [] # This is used for item positioning
        self.find_center(entity, None, 0, 0, list_actions)

        self.mx_nodes = []

        # get flows from the relation 'flow' or 'contains'
        entity.init_sim_network()

        # print out control flows of UC
        return self.get_mxgraph_string(entity, entity.sim_network, list_actions)