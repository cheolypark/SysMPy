from entity import *
from relationship import *


class GuiManagerMXgraph:
    def __init__(self):
        """
        """
        # mxGraph variables
        self.mx_nodes = []


    ########################################################################
    # Graphic Methods
    #
    def safe_name(self, name):
        return name.replace(" ", "_")

    def make_node(self, name, x, y):
        # var v1 = graph.insertVertex(parent, null, 'Hello,', 20, 20, 80, 30) \\n
        node = ''
        s_name = self.safe_name(name)
        if s_name not in self.mx_nodes:
            self.mx_nodes.append(s_name)
            node = f"var {s_name} = graph.insertVertex(parent, null, '{name}', {x}, {y}, 80, 30) /n "
        # print(node)
        return node

    def make_edge(self, s, e, point=None):
        # var e1 = graph.insertEdge(parent, null, '', v1, v2)\\n
        s = self.safe_name(s)
        e = self.safe_name(e)
        # edge = f"var {s}_{e} = graph.insertEdge(parent, null, '', {s}, {e}, 'verticalAlign=top') /n "
        edge = f"var {s}_{e} = graph.insertEdge(parent, null, '', {s}, {e}) /n "
        # edge += f'{s}_{e}.geometry.points = [new mxPoint({s}.geometry.x + 10, 10)]/n'

        if point is not None:
            edge += f'{s}_{e}.geometry.points = [new mxPoint( {point}, 0 )]/n'
        # e = graph.insertEdge(lane2a, null, 'No', step444, end3, 'verticalAlign=top');
        # e.geometry.points = [new mxPoint(step444.geometry.x + step444.geometry.width / 2,
        #                                  end3.geometry.y + end3.geometry.height / 2)];

        # print(edge)
        return edge

    def get_mxgraph_string(self, entity, entities):
        str = ''
        flows = [r for r in entity.relation['flows'] if isinstance(r, Flow)]
        for i, f in enumerate(flows):
            str += self.make_node(f.start.name, f.start.center_x, f.start.center_y)
            str += self.make_node(f.end.name, f.end.center_x, f.end.center_y)
            str += self.make_edge(f.start.name, f.end.name)

        for e in entities:
            if 'flows' in e.relation:
                flows = [r for r in e.relation['flows'] if isinstance(r, Flow)]
                for i, f in enumerate(flows):
                    str += self.make_node(f.start.name, f.start.center_x, f.start.center_y)
                    str += self.make_node(f.end.name, f.end.center_x, f.end.center_y)
                    if isinstance(f.start, Loop_END) and isinstance(f.end, Loop):
                        str += self.make_edge(f.start.name, f.end.name, f.start.center_x+f.start.node_width+20)
                        # str += self.make_edge(f.start.name, f.end.name, 150)
                    else:
                        str += self.make_edge(f.start.name, f.end.name)

        return str

    def get_mxgraph(self, entity):

        # 1. Find size and root_x of nodes
        self.find_size_and_root_x(entity)

        # 2. Find center_x and center_y
        self.find_center(entity, None, 0, 0)

        self.mx_nodes = []
        sim_network = []

        # get flows from the relation 'flow' or 'contains'
        entity.get_flows(sim_network)

        # print out control flows of UC
        return self.get_mxgraph_string(entity, sim_network)

    def find_size_and_root_x(self, entity):
        # print(f'{entity.name}')

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

    def find_center(self, entity, parent, pre_edge_x, pre_edge_y):
        # print(f'{entity.name}')

        # find center_x and center_y
        if isinstance(entity, Action):
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

                child_x, child_y = self.find_center(child, entity, pre_edge_x, pre_edge_y)

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

