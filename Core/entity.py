import asyncio
from relationship import *
import random


class Entity:
    """ LIFECYCLE MODELING LANGUAGE (LML) SPECIFICATION 1.1:
    An entity is something can exist by itself and is uniquely identifiable.
    """

    # This is a database for all entities
    entity_db = []
    _debug_mode = False

    def __init__(self, name, number=None, description=None):
        self.name = name
        self.number = number
        self.description = description
        self.relation = {}      # Relation
        self.inv_relation = {}  # Inverse Relation
        self.decomposition = True

        # All entities created are stored in the static class Entity
        Entity.store_entity(self)

    def __str__(self):
        return "{} decomposes {}".format(self.name, self.relation)

    def set_decomposition(self, dec):
        """
        This sets the decomposition state when simulating
        :param dec: 'True' denotes to execute the simulation of sub-nodes,
                    while 'False' means to skip the sub-nodes simulation.
        """
        self.decomposition = dec

    ########################################################################
    # Class Creation Methods
    # !start with an uppercase letter
    #
    def Property(self, name, range=None, value=None):
        obj = Property(name, range, value)
        Contains(self, obj)
        return obj

    ########################################################################
    # Relationship Methods
    # !start with an lowercase letter
    #
    def decomposes(self, target):
        """
        This makes a 'decomposes' or 'decomposes' relationship between this and a target
        :param target: an entity is decomposed by this
        """
        Decomposes(self, target)

    def traced_from(self, target):
        """
        --
        """
        TracedFrom(self, target)

    def required_by(self, target):
        """
        --
        """
        RequiredBy(self, target)

    ########################################################################
    # Static Methods
    #
    #
    @staticmethod
    def debug_mode(self, b):
        Entity._debug_mode = b

    @staticmethod
    def store_entity(self):
        """ All entities created are stored """
        Entity.entity_db.append(self)

    @staticmethod
    def get(name_entity):
        """ This returns instances of an entity """
        l = name_entity.split('.')

        cur_obj = None
        for i in l:
            if cur_obj is None:
                cur_obj = Entity.get_op(i)
            else:
                cur_obj = Entity.get_by_relationship(cur_obj, i, 'contains')

        return cur_obj

    @staticmethod
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
                else:
                    return e

    @staticmethod
    def get_op(name_entity):
        """ This returns instances of an entity by searching in the entity_db"""
        e = [x for x in Entity.entity_db if x.name == name_entity]
        if e is None:
            return None
        elif len(e) == 1:
            return e[0]
        else:
            return e

    @staticmethod
    def get_by_type(type_entity):
        """ This returns instances of an entity by the entity type"""
        e = [x for x in Entity.entity_db if isinstance(x, type_entity)]
        if e is None:
            return None
        elif len(e) == 1:
            return e[0]
        else:
            return e


########################################################################
# Static Entity
#
#
class StaticEntity(Entity):
    """ This is an abstract class regarding Static Entity"""

    def __init__(self, name):
        super().__init__(name)

    def __str__(self):
        str = self.name
        if 'decomposes' in self.relation:
            rel = [x.end for x in self.relation['decomposes']]
            s = ', '.join([r.name for r in rel])
            str += ": decomposes [{}]".format(s)

        if 'performs' in self.relation:
            rel = [x.end for x in self.relation['performs']]
            s = ', '.join([r.name for r in rel])
            str += ": performs [{}]".format(s)

        if 'traced from' in self.relation:
            rel = [x.end for x in self.relation['traced from']]
            s = ', '.join([r.name for r in rel])
            str += ": traced from [{}]".format(s)

        if 'required by' in self.relation:
            rel = [x.end for x in self.relation['required by']]
            s = ', '.join([r.name for r in rel])
            str += ": required by [{}]".format(s)

        return str


class Property(StaticEntity):
    def __init__(self, name, range=None, value=None):
        """
        :param name: e.g., ) 'X'
        :param range: e.g., ) 'Less(10)', 'More(10)', 'Between(1, 10)',
        [1, 2, 3], ['A', 'B', 'C'], 'Normal(10, 1)', 'Uniform(1, 10)'
        ['Between(1, 10)', 'Between(30, 40)']
        :param value: e.g., ) 'T', 10
        """
        super().__init__(name)
        self.range = range
        self.value = value

    def get_random_value(self):
        if isinstance(self.range, list):
            self.value = random.choice(self.range)
            return self.value


class Item(StaticEntity):
    def __init__(self, name):
        super().__init__(name)
        self.attr = {}


class Conduit(StaticEntity):
    """
    Conduit is a kind of link or interface.
    Conduit is associated with items.
    """

    def __init__(self, name):
        super().__init__(name)
        self._capacity = 1
        self._delay = 0

    ########################################################################
    # Relationship Methods
    # !start with an lowercase letter
    #
    def transfers(self, item):
        """
        This makes a relationship between this and an item
        :param item: an item is transferred by this conduit
        """
        Transfers(self, item)

    def delay(self, delay):
        """
        This represents the time required to transmit an item over this Conduit.
        :param delay:
        """
        self._delay = delay

    def capacity(self, capacity):
        """
        This represents the maximum rate supported by the Conduit.
        :param capacity:
        """
        self._capacity = capacity


class Resource(StaticEntity):
    def __init__(self, name, amount=5, minimum=1, maximum=10, units=None):
        super().__init__(name)
        self.amount = amount
        self.minimum = minimum
        self.maximum = maximum
        self.units = units


class Requirement(Property):
    def __init__(self, name, range=None, value=None, **kwargs):
        super().__init__(name, range, value)
        self.kwargs = kwargs

    def check_property(self):
        if 'traced to' in self.inv_relation:
            rel = [x.start for x in self.inv_relation['traced to']]
            l = {r.name:r.value for r in rel}
            is_passed = 'passed' if rel[0].value in self.range else 'failed'
            str = f'{self.name} Range is {self.range}: {l} {is_passed}'
            print(str)

    def __str__(self):
        """Overriding StaticEntity.__str__ so that it prints kwargs as well (useful for debugging).
        :return: super().__str__ appended with self.kwargs
        """
        ret = super(Requirement, self).__str__()
        ret += " " + str(self.kwargs)
        return ret

class Component(StaticEntity):
    def __init__(self, name, **kwargs):
        super().__init__(name)
        self.kwargs = kwargs

    ########################################################################
    # Relationship Methods
    # !start with an lowercase letter
    #
    def performs(self, target):
        Performs(self, target)


########################################################################
# Dynamic Entity
#
#
class DynamicEntity(Entity):
    """ This is an abstract class regarding Dynamic Entity"""

    def __init__(self, name, duration=0):
        super().__init__(name)
        self.duration = duration
        self.time = 0
        self.total_time = 0
        self.waiting = False
        self.is_root = False
        self.function = None

    def reset(self):
        self.waiting = False

    ########################################################################
    # Relationship Methods
    # !start with an lowercase letter
    #
    def seizes(self, resource, amount=10):
        """
        This make a relation 'seizes' between this DEntity and the target resource
        The DEntity will fire, when the target resource are available

        :param
        resource: The target resource
        amount: The amount that will be taken
        """
        Seizes(self, resource, amount)

    def consumes(self, resource, amount=10):
        """
        This make a relation 'consumes' between this DEntity and the target resource
        The DEntity will fire, when the target resource are available

        :param
        resource: The target resource
        amount: The amount that will be taken
        """
        Consumes(self, resource, amount)

    def produces(self, resource, amount=10):
        """
        This make a relation 'produces' between this DEntity and the target resource
        The DEntity will fire, when the target resource are available

        :param
        resource: The target resource
        amount: The amount that will be produced
        """
        Produces(self, resource, amount)

    def flow(self, e):
        """
        This make a relation 'flow' between actions
        The relation 'flow' is used to represent a control flow between dynamic entities (e.g., Process A to Action B)

        :param
        e: The target dynamic entity of this dynamic entity
        """
        Flow(self, e)

    def receives(self, item):
        """
        This make a relation 'receives' between this action and an input trigger item
        The input trigger item differs from the input item that does not influence this action

        :param
        item: The input trigger item
        """
        Receives(self, item)

    def triggered(self, item):
        """
        This make a relation 'triggered' between this action and an input trigger item
        The input trigger item differs from the input item that does not influence this action

        :param
        item: The input trigger item
        """
        Triggered(self, item)

    def sends(self, item, amount=10):
        """
        This make a relation 'sends' between this DEntity and the target item
        The DEntity will fire, when the target resource are available

        :param
        item: The target item
        amount: The amount that will be sent
        """
        Sends(self, item, amount)

    def func(self, function):
        self.function = function

    ########################################################################
    # Simulation Methods
    #
    #
    def get_flows(self, entities):
        """
        This finds all flow nodes used in Simulation
        The returning list acts will have flow nodes which are activated by Python Asyncio

        :param
        entities: All entities that will be accumulated
        """

        if 'contains' in self.relation:
            contains = [x.end for x in self.relation['contains']]
            if contains is not None:
                entities += contains
                cur_e = None
                last_e = []
                for e in contains:

                    if isinstance(self, And) or isinstance(self, Or) or isinstance(self, Condition):
                        # If e is not 'or' or 'and', then make a parallel flow
                        self.flow(e)
                        last_e.append(e)
                    else:
                        # If e is not 'or' or 'and', then make a serial flow

                        if cur_e is None:
                            # e.g.,) (self)Process1->(e)Action1
                            self.flow(e)
                        else:
                            if hasattr(cur_e, 'end') and cur_e.decomposition:
                                # 1. 'cur_e.decomposition' is checked for skipping the decomposition of sub-nodes
                                # Especially, 'Action' can be decomposed.
                                # 2. This 'cur_e' decomposes the node 'end'
                                # This means that the next node 'e' should be connected to the node 'end'
                                # e.g.,) (cur_e)Loop->Action1->Loop_END->Action2
                                # 'Action2' is linked to 'Loop_END', but not 'Loop'
                                cur_e.end.flow(e)
                            else:
                                cur_e.flow(e)

                        cur_e = e

                    # if this entity does not allow the decomposition, don't make any sub-flows for simulation
                    if e.decomposition:
                        e.get_flows(entities)

                ######################################################################
                # Concatenate this node to the 'END' node
                #
                if cur_e is not None:
                    last_e.append(cur_e)

                if self.end is not None:
                    for e in last_e:
                        if not isinstance(e, Action):
                            # If e decomposes the node 'end' (e.g., 'Loop' and 'Action' containing 'process')
                            # This means there is the 'End' pair for this
                            # This 'End' pair is used for flowing to the current 'End' pair
                            e.end.flow(self.end)
                        else:
                            # If e does not have the node 'end' (e.g., 'Action')
                            # This means it doesn't have any pair
                            e.flow(self.end)

                    entities.append(self.end)
        elif isinstance(self, Process):   # This is likely to be an empty process (no 'contains' key)
            # Just let this root process to flow directly to the end
            self.flow(self.end)
            # Make sure the list contains the end node
            entities.append(self.end)


    def print_flows(self, entities):
        """
        This prints out the control flows of UC
        :param entities: the flow list generated from 'get_flows()'
        """
        flows = [r for r in self.relation['flows'] if isinstance(r, Flow)]
        for f in flows:
            print(f)

        for e in entities:
            flows = [r for r in e.relation['flows'] if isinstance(r, Flow)]
            for f in flows:
                print(f)

    async def run(self):
        """
        This is a core function that performs all operation about simulation
        Each DynamicEntity uses this function 'run' to do its own simulation

        There are two phases
            Phase 1: Check Activating Conditions, so that this can enter the activation stage of simulation
            Phase 2: Perform Action in which all defined activities are performed
        """
        while Process.activated:
            # Info is used to store any information in this process and be printed out by 'Process.store_data()'
            info = ''

            ##################################################################################
            #
            #       Phase 1: Check Activating Conditions
            #
            ##################################################################################

            ########################################################################
            # Check 1: Check waiting state
            # Any process can be waiting, if there is no event to this process
            if self.waiting is False:
                Process.store_data(self, 'was waiting')
                self.waiting = True

            # Reset all fire states
            # If all of these are true, then this process will fire all events to the child processes
            b_flow_fire = False
            b_consumes_fire = False
            b_seizes_fire = False
            b_triggered_fire = False

            ########################################################################
            # Check 2: Input Control Flows
            # This is receiving control flows
            # Non input flows mean that this is a root node
            # Such root node is just firing all events regardless any conditions
            flowed_from = None
            flows_true = None

            # Take a list for the relationship 'flowed from'
            if 'flowed from' in self.inv_relation:
                flowed_from = [r for r in self.inv_relation['flowed from'] if isinstance(r, Flow)]

            if flowed_from is None:
                # No flowed_from means there are no input events for this node
                b_flow_fire = True
            else:
                # Having flowed_from means there are input events for this node
                flows_true = [r for r in flowed_from if r.sent is True]

                # Check whether all input events are set to 'sent=True'
                # This means this node now can fire its output event
                if len(flowed_from) == len(flows_true) and len(flowed_from) > 0:
                    b_flow_fire = True

                # If this self is 'or_END' and decomposes one true inputting event
                # Then this node now can fire its output event
                if isinstance(self, Or_END) and len(flows_true) >= 1:
                    b_flow_fire = True

                # If this self is 'Condition_END' and decomposes one true inputting event
                # Then this node now can fire its output event
                if isinstance(self, Condition_END) and len(flows_true) >= 1:
                    b_flow_fire = True

                # If this self is 'Process_END' and decomposes one true inputting event
                # Then this node now can fire its output event
                if isinstance(self, Process_END) and len(flows_true) >= 1:
                    b_flow_fire = True

                # If this self is 'Loop_END' and decomposes one true inputting event
                # Then this node now can fire its output event
                if isinstance(self, Loop_END) and len(flows_true) >= 1:
                    b_flow_fire = True

                # If this self is 'loop' and decomposes one true inputting event
                # Then this node now can fire its output event
                if isinstance(self, Loop) and len(flows_true) >= 1:
                    b_flow_fire = True

                # If this flow should be fired,
                # All process which sent were reset to 'sent = False'
                if b_flow_fire:
                    for r in flows_true:
                        r.sent = False

                    # Set a new start time for this process by checking the times of the previous flow entities
                    max_time = max([r.start.time for r in flowed_from])
                    self.time = max_time
                    info += 'Fired from: ' + ', '.join([r.start.name for r in flows_true])

            ########################################################################
            # Check 3: Resources Consumes
            consumes = None
            consumes_true = None

            # Take a list for the relationship 'consumes'
            if 'consumes' in self.relation:
                consumes = [r for r in self.relation['consumes'] if isinstance(r, Consumes)]

            if consumes is None:
                # No seizes means there are no resource events for this node
                b_consumes_fire = True
            else:
                # Having seizes means there are resource events for this node
                consumes_true = [r for r in consumes if r.amount <= r.end.amount]

                # Check whether all input events are set to 'sent=True'
                # This means this node now can fire its output event
                if len(consumes) == len(consumes_true) and len(consumes) > 0:
                    b_consumes_fire = True

            ########################################################################
            # Check 3: Resources Seizes
            seizes = None
            seizes_true = None

            # Take a list for the relationship 'seizes'
            if 'seizes' in self.relation:
                seizes = [r for r in self.relation['seizes'] if isinstance(r, Seizes)]

            if seizes is None:
                # No seizes means there are no resource events for this node
                b_seizes_fire = True
            else:
                # Having seizes means there are resource events for this node
                seizes_true = [r for r in seizes if r.amount <= r.end.amount]

                # Check whether all input events are set to 'True'
                # This means this node now can fire its output event
                if len(seizes) == len(seizes_true) and len(seizes) > 0:
                    b_seizes_fire = True

            ########################################################################
            # Check 4: Triggered Item

            triggered = None
            triggered_true = None

            # Take a list for the relationship 'triggered by'
            if 'triggered by' in self.relation:
                triggered = [r for r in self.relation['triggered by'] if isinstance(r, Triggered)]

            if triggered is None:
                # No receives means there are no triggering events for this node
                b_triggered_fire = True
            else:
                # Having receives means there are triggering events for this node
                triggered_true = [r for r in triggered if r.trigger is True]

                # Check whether all input events are set to 'trigger=True'
                # This means this node now can fire its output event
                if len(triggered) == len(triggered_true) and len(triggered) > 0:
                    b_triggered_fire = True

                    for r in triggered_true:
                        r.trigger = False

                    # Set a new start time for this process by checking the times from the process that triggered
                    #----------------------------------------------------
                    # Warning: This can make an error. We need to check only triggered items, but not common items.
                    pre_actions = [r.end.inv_relation['sent from'] for r in triggered_true]
                    max_time = max([r.start.time for r in pre_actions[0]])
                    self.time = max(max_time, self.time)
                    info += ' triggered from: ' + ', '.join([r.end.name for r in triggered_true])

                    # If this is associated with conduits, the times for conduits should be applied
                    # Calculate the conduit times
                    conduits = [r.end.inv_relation['transferred by'] for r in triggered_true]
                    max_delay = max([r.start._delay  for r in conduits[0]])
                    max_capacity = max([r.start._capacity for r in conduits[0]])
                    max_size = max([r.end._size for r in conduits[0]])
                    max_conduits_time = max_delay + max_size/max_capacity

                    Process.store_data(self, 'triggered', info=f'After conduit flows, '
                                                               f'a time {max_conduits_time} was added')

                    # Apply the conduit times to this process time
                    self.time += max_conduits_time

            ##################################################################################
            #
            #       Phase 2: Perform Action
            #
            ##################################################################################
            if b_flow_fire and b_seizes_fire and b_consumes_fire and b_triggered_fire:

                ########################################################################
                # Check 1: Activate this action
                Process.store_data(self, 'was activated', info=info)
                self.waiting = False

                ########################################################################
                # Check 2: Check global time
                Process.global_time = max(Process.global_time, self.time)
                if Process.global_time >= Process.global_max:
                    Process.activated = False

                ########################################################################
                # Check 3: Resources Seizes
                # Seizes all related resources
                if seizes_true is not None:
                    for r in seizes_true:
                        r.end.amount -= r.amount
                        s = ''
                        s += ' Resources(' + ', '.join([r.end.name for r in seizes_true])+')'
                        s += ' Taking Amounts(' + ', '.join([str(r.amount) for r in seizes_true])+')'
                        s += ' Result Amounts(' + ', '.join([str(r.end.amount) for r in seizes_true])+')'
                        Process.store_data(self, 'seizes resources', info=f'[{s}]')

                ########################################################################
                # Check 4: Sends Item
                # Note that 'Sends Item' is for trigger items, but not common items
                # Because the simulation uses only the trigger items
                # Later we may be able to use the common items in some purposes
                if 'sends' in self.relation:
                    sends = [x for x in self.relation['sends'] if isinstance(x, Sends)]
                    for r in sends:
                        r.trigger = True
                        # Check all send relations associated with the item of this relation r
                        sent_from_for_item = [x for x in r.end.inv_relation['sent from'] if isinstance(x, Sends)]
                        sent_from_for_item_true = [x for x in sent_from_for_item if x.trigger is True]

                        if len(sent_from_for_item) == len(sent_from_for_item_true):
                            # All relations 'sent from' were set to 'True'
                            # Then we can fire the related trigger items.
                            # So, set all relation 'triggered' in this item as 'True',
                            # if it decomposes the relation 'triggered'
                            if 'triggers' in r.end.inv_relation:
                                triggered_for_item = [x for x in r.end.inv_relation['triggers'] if isinstance(x, Triggered)]
                                for r2 in triggered_for_item:
                                    r2.trigger = True

                                s = ''
                                s += 'To : ' + ', '.join([r.end.name for r in triggered_for_item])
                                Process.store_data(self, 'sends', info=f'[{s}]')

                ########################################################################
                # Check 5: Produces Resources
                if 'produces' in self.relation:
                    produces = [x for x in self.relation['produces'] if isinstance(x, Produces)]
                    for r in produces:
                        r.end.amount += r.amount
                        Process.store_data(self, 'produces resources', info=f'[New resources({r.amount}) '
                                                                            f'Total resources({r.end.amount})]')

                ########################################################################
                # Check 6: Resources Consumes
                if consumes_true is not None:
                    for r in consumes_true:
                        r.end.amount -= r.amount
                        s = ''
                        s += ' Consumes resources(' + ', '.join([r.end.name for r in consumes_true]) + ')'
                        s += ' Taking Amounts(' + ', '.join([str(r.amount) for r in consumes_true]) + ')'
                        s += ' Result Amounts(' + ', '.join([str(r.end.amount) for r in consumes_true]) + ')'
                        Process.store_data(self, 'consumes resources', info=f'[{s}]')

                ########################################################################
                # Check 7: Input Control Flows
                # Send all output events
                if 'flows' in self.relation:
                    flows = [x for x in self.relation['flows'] if isinstance(x, Flow)]

                    if isinstance(self, Action):
                        if self.function is not None:
                            # Perform a function script for selection
                            selected = self.function(Entity)

                    if isinstance(self, Or):
                        selected = random.choice(flows)
                        Process.store_data(self, 'selects ' +selected.end.name)
                        selected.sent = True
                    elif isinstance(self, Condition):
                        if self.function is not None:
                            # Perform a function script for selection
                            selected = self.function(Entity)
                            selected_flows = [r for r in flows if r.end is selected]
                            Process.store_data(self, 'selects ' + ', '.join([r.end.name for r in selected_flows]))
                            for r in selected_flows:
                                r.sent = True
                        else:
                            # Perform uniformly random selection for the branches
                            selected = random.choice(flows)
                            Process.store_data(self, 'selects ' + selected.end.name)
                            selected.sent = True
                    elif isinstance(self, Loop_END):
                        exit_loop = [x for x in flows_true if isinstance(x.start, ExitLoop)]

                        if self.count >= self.times-1 or len(exit_loop) > 0:
                            Process.store_data(self, 'finished repetition')
                            self.reset()
                            loops = [x for x in self.relation['flows'] if not isinstance(x.end, Loop)]
                            for x in loops:
                                x.sent = True
                        else:
                            self.count += 1
                            Process.store_data(self, 'repeats '+ str(self.count))
                            loops = [x for x in self.relation['flows'] if isinstance(x.end, Loop)]
                            for x in loops:
                                x.sent = True

                    elif isinstance(self, Process_END) and self.is_root:
                        self.reset()
                        for x in flows:
                            x.sent = True
                    else:
                        for x in flows:
                            x.sent = True

                ########################################################################
                # Check 8: Complete this process
                self.time += self.duration
                self.total_time += self.duration
                Process.store_data(self, 'was completed', info='')

                ########################################################################
                # Check 9: Resources Seizes
                # Release all seized resources
                if seizes_true is not None:
                    for r in seizes_true:
                        r.end.amount += r.amount
                        s = ''
                        s += ' Resources(' + ', '.join([r.end.name for r in seizes_true]) + ')'
                        s += ' Taking Amounts(' + ', '.join([str(r.amount) for r in seizes_true]) + ')'
                        s += ' Result Amounts(' + ', '.join([str(r.end.amount) for r in seizes_true]) + ')'
                        Process.store_data(self, 'releases resources', info=f'[{s}]')

                ########################################################################
                # Check 10: One iteration of the root process was done
                if isinstance(self, Process_END) and self.is_root:
                    Process.store_data(self, 'decomposes done as the root process', info='')
                    Process.store_data(self, "deactivating root process now", info='')
                    Process.activated = False

            else:
                ########################################################################
                # Waiting all action internal operations
                await asyncio.sleep(0)


class Action(DynamicEntity):
    """
    Action Dynamic Entity
    """
    def __init__(self, name, duration=1):
        super().__init__(name, duration)

    ########################################################################
    # Class Creation Methods
    # !start with an uppercase letter
    #
    def Process(self, name):
        obj = Process(name)
        Contains(self, obj)

        # This action decomposes a sub-process
        # Consequently, this action will have the 'Action_end'
        self.end = Action_END(self.name + '_END')

        # Link this and the end using the relation 'Pairs'
        Pairs(self, self.end)

        return obj


class Action_END(DynamicEntity):
    def __init__(self, name):
        super().__init__(name)


class And(DynamicEntity):
    """
    And Dynamic Entity
    """
    def __init__(self, name='and'):
        super().__init__(name)

        # This decomposes a pair dynamic entity called 'end' or name+'_END'
        self.end = Or_END(name + '_END')

        # Link this and the end using the relation 'Pairs'
        Pairs(self, self.end)

    ########################################################################
    # Class Creation Methods
    # !start with an uppercase letter
    #
    def Process(self, name):
        obj = Process(name)
        Contains(self, obj)
        return obj


class And_END(DynamicEntity):
    def __init__(self, name):
        super().__init__(name)


class Or(DynamicEntity):
    """
    Or Dynamic Entity
    """
    def __init__(self, name='or'):
        super().__init__(name)

        # This decomposes a pair dynamic entity called 'end' or name+'_END'
        self.end = Or_END(name + '_END')

        # Link this and the end using the relation 'Pairs'
        Pairs(self, self.end)

    ########################################################################
    # Class Creation Methods
    # !start with an uppercase letter
    #
    def Process(self, name):
        obj = Process(name)
        Contains(self, obj)
        return obj


class Or_END(DynamicEntity):
    def __init__(self, name):
        super().__init__(name)


class Process(DynamicEntity):
    """
    Process Dynamic Entity
    """

    # 'activated' is used to denote Simulation's activation. False means 'stop simulation'
    activated = False
    # 'global_time' is used to denote Simulation's global time
    global_time = 0
    # 'global_max' is used to denote when Simulation will stop
    global_max = 0

    def __init__(self, name):
        super().__init__(name)

        # This decomposes a pair dynamic entity called 'end' or name+'_END'
        self.end = Process_END(name + '_END')

        # Link this and the end using the relation 'Pairs'
        Pairs(self, self.end)

        # AsyncIO workers are used to be performed as computing threads
        self.workers = []

    @staticmethod
    def store_data(act, event, info=''):
        if Entity._debug_mode:
            if len(info) == 0:
                print(f'T: {act.time}, N: {act.name}, E: {event}')
            else:
                print(f'T: {act.time}, N: {act.name}, E: {event}, I: {info}')
        else:

            if isinstance(act, And) or \
               isinstance(act, And_END) or \
               isinstance(act, Loop) or \
               isinstance(act, Loop_END) or \
               isinstance(act, Condition) or \
               isinstance(act, Condition_END) or \
               isinstance(act, END) or \
               isinstance(act, ExitLoop) or \
               isinstance(act, Process) or \
               isinstance(act, Or) or \
               isinstance(act, Or_END):
                return

            if isinstance(act, Process_END):
                if event != 'was waiting' and \
                   event != 'was activated' and \
                   event != 'was completed' :
                    print(f'At Time {act.time}, {act.name} {event}.')
            else:
                if event != 'was waiting':
                    print(f'At Time {act.time}, {act.name} {event}.')

    async def sim(self, until=5):
        """
        This triggers the simulation.

        :param
        until: The maximum time, modeled in the process flows, for simulation run
        """


        # The function sim is called, which means this is a root process
        self.is_root = True
        self.end.is_root = True

        # The root process is linked to 'process_END' using the relation 'flow'
        # 'process_END' -> 'process'
        self.end.flow(self)

        # For the relation 'process_END' -> 'process', set 'sent = true' to activate the root process
        flowed_from = [r for r in self.inv_relation['flowed from'] if isinstance(r, Flow)]
        flowed_from[0].sent = True

        # Find other flows and set them into asyncio
        if 'flows' or 'contains' in self.relation:
            # Reset all global variables regarding simulation
            Process.global_time = 0
            Process.activated = True
            Process.global_max = until
            d_entities = []

            # get flows from the relation 'flow' or 'contains'
            self.get_flows(d_entities)

            # print out control flows of UC
            # self.print_flows(d_entities)

            workers = [x.run() for x in d_entities]
            workers.append(self.run())
            # await asyncio.gather(*self.workers)
            try:
                res = await asyncio.gather(*workers)
            except asyncio.CancelledError:
                print('CancelledError')
                res = None

    def find_root(self):
        """
        This finds a root process.
        :return:
        A root process
        """
        if 'contained in' not in self.inv_relation:
            return self

        r = [x for x in self.inv_relation['contained in']]
        if r is None:
            return
        else:
            for x in r:
                root = x.start.find_root()
        return root

    def find_all_nodes(self, class_type, ret_list):
        """
        This finds all nodes specified in the input 'rel_type'
        :return:
        A list of all nodes created from the class rel_type
        """

        if 'contained in' not in self.inv_relation:
            return

        found = [x for x in self.inv_relation['contained in'] if isinstance(x.start, class_type)]
        ret_list += found

        r = [x for x in self.inv_relation['contained in']]
        if r is None:
            return
        else:
            for x in r:
                x.start.find_all_nodes(class_type, ret_list)

    def find_loop_end(self):
        """
        This returns a first Loop-End node
        """
        ret = []
        self.find_all_nodes(Loop, ret)
        return ret[0].start.end

    ########################################################################
    # Class Creation Methods
    # !start with an uppercase letter
    #
    def Action(self, name, duration=1):
        """
        :param name:
        :param duration: The time modeled in the process flows
        :return:
        """
        obj = Action(name, duration)
        Contains(self, obj)
        return obj

    def And(self):
        obj = And()
        Contains(self, obj)
        return obj

    def Or(self):
        obj = Or()
        Contains(self, obj)
        return obj

    def Process(self, name):
        obj = Process(name)
        Contains(self, obj)
        Decomposes(self, obj)
        return obj

    def Loop(self, times=2):
        obj = Loop(name='loop', times=times)
        Contains(self, obj)
        return obj

    def Condition(self, name):
        obj = Condition(name=name)
        Contains(self, obj)
        return obj

    def End(self, name='END'):
        obj = END(name=name)
        Contains(self, obj)
        root_process = obj.find_root()
        # 'loop' is linked to 'loop_END' using the relation 'flow'
        # 'loop_END' -> 'loop'
        obj.flow(root_process.end)
        return obj

    def ExitLoop(self, name='ExitLoop'):
        obj = ExitLoop(name=name)
        Contains(self, obj)
        loop_end = obj.find_loop_end()
        # 'loop' is linked to 'loop_END' using the relation 'flow'
        # 'loop_END' -> 'loop'
        obj.flow(loop_end)
        return obj


class Process_END(DynamicEntity):
    def __init__(self, name):
        super().__init__(name)


class Loop(Process):
    """
    Loop Dynamic Entity
    """

    def __init__(self, name='loop', times=2):
        super().__init__(name)

        # This decomposes a pair dynamic entity called 'end' or name+'_END'
        self.end = Loop_END(name + '_END', times=times)

        # Link this and the end using the relation 'Pairs'
        Pairs(self, self.end)

        # 'loop' is linked to 'loop_END' using the relation 'flow'
        # 'loop_END' -> 'loop'
        self.end.flow(self)

    ########################################################################
    # Class Creation Methods
    # !start with an uppercase letter
    #
    def Process(self, name):
        obj = Process(name)
        Contains(self, obj)
        return obj


class Loop_END(Process):
    def __init__(self, name, times):
        super().__init__(name)

        # 'loop_END' is set with the looping times
        self.times = times
        self.count = 0

    def reset(self):
        super().reset()
        self.count = 0


class Condition(Process):
    """
    Condition Dynamic Entity
    """

    def __init__(self, name):
        super().__init__(name)

        # This decomposes a pair dynamic entity called 'end' or name+'_END'
        self.end = Condition_END(name + '_END')

        # Link this and the end using the relation 'Pairs'
        Pairs(self, self.end)


class Condition_END(Process):
    def __init__(self, name):
        super().__init__(name)

    def reset(self):
        super().reset()


class END(Process):
    """
    END Dynamic Entity
    """

    def __init__(self, name):
        super().__init__(name)

    def reset(self):
        super().reset()


class ExitLoop(Process):
    def __init__(self, name):
        super().__init__(name)

    def reset(self):
        super().reset()
