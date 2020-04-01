class Relationship:
    """ LIFECYCLE MODELING LANGUAGE (LML) SPECIFICATION 1.1:
    A relationship connects entities to each other.
    """

    def __init__(self, re_name, inv_name, start, end, number=None, description=None):
        self.number = number
        self.description = description
        self.re_name = re_name
        self.inv_name = inv_name
        self.start = start
        self.end = end

        # Add new relation for the starting entity
        if re_name in start.relation:
            rel = start.relation[re_name]
            rel.append(self)
        else:
            rel = []
            start.relation[re_name] = rel
            rel.append(self)

        # Add new inverse relation for the ending entity
        if inv_name in end.inv_relation:
            rel = end.inv_relation[inv_name]
            rel.append(self)
        else:
            rel = []
            end.inv_relation[inv_name] = rel
            rel.append(self)

    def reset_sim_status(self):
        pass

    def __str__(self):
        s = '[{}] {} [{}]'.format(self.start.name, self.re_name, self.end.name)
        return s


class Flow(Relationship):
    """
    'Flow' is used to send control flows between dynamic entities for simulation.
    e.g.,) When a simulation of 'Action 1' is completed, 'Flow 1' is sent to 'Action 2' from 'Action 1'
    """
    def __init__(self, start, end):
        super().__init__('flows', 'flowed from', start, end)
        self.sent = False

    def reset_sim_status(self):
        super().reset_sim_status()
        self.sent = False

class Sends(Relationship):
    """
    'Sends' is used to represent a sending item flow.
    e.g.,) 'Action 1' sends 'Item 1' using this relationship
    """
    def __init__(self, start, end, size=10):
        super().__init__('sends', 'sent from', start, end)
        self.size = size
        self.trigger = False

    def reset_sim_status(self):
        super().reset_sim_status()
        self.trigger = False


class Receives(Relationship):
    """
    'Receives' is used to represent a receiving item flow.
    e.g.,) 'Action 1' receives 'Item 1' from 'Action 0'
    """
    def __init__(self, start, end):
        super().__init__('receives', 'received by', start, end)


class Triggered(Relationship):
    """
    'Triggered' is used to represent a triggering item flow.
    e.g.,) 'Action 1' is triggered by 'Item 1' from 'Action 0'
    """
    def __init__(self, start, end):
        super().__init__('triggered by', 'triggers', start, end)
        self.trigger = False

    def reset_sim_status(self):
        super().reset_sim_status()
        self.trigger = False

class Produces(Relationship):
    """
    'Produces' is used to produce a resource.
    e.g.,) 'Action 1' produces 'Resource 1'
    """
    def __init__(self, start, end, amount=10):
        super().__init__('produces', 'produced by', start, end)
        self.default_amount = amount
        self.amount = self.default_amount

    def reset_sim_status(self):
        super().reset_sim_status()
        self.amount = self.default_amount


class Seizes(Relationship):
    """
    'Seizes' is used to represent for capturing a resource.
    e.g.,) 'Action 1' seizes 'Resource 1'. After seizing, 'Resource 1' is released.
    """
    def __init__(self, start, end, amount=10):
        super().__init__('seizes', 'seized by', start, end)
        self.default_amount = amount
        self.amount = self.default_amount

    def reset_sim_status(self):
        super().reset_sim_status()
        self.amount = self.default_amount

class Consumes(Relationship):
    """
    'Consumes' is used to represent for consuming a resource.
    e.g.,) 'Action 1' consumes 'Resource 1'. After consuming, the amount of 'Resource 1' is reduced.
    """
    def __init__(self, start, end, amount=10):
        super().__init__('consumes', 'consumed by', start, end)
        self.default_amount = amount
        self.amount = self.default_amount

    def reset_sim_status(self):
        super().reset_sim_status()
        self.amount = self.default_amount


class Decomposes(Relationship):
    """
    'Decomposes' is used to represent for decomposition of an entity.
    e.g.,) 'Action 1' is decomposed into 'Acton 1.1' and 'Acton 1.2'.
    """
    def __init__(self, start, end):
        super().__init__('decomposes', 'decomposed by', start, end)


class Contains(Relationship):
    """
    'Contains' is used to represent for a subset of an entity.
    'Contains' represents the relationship 'aggregation' 1 to n
    e.g.,) 'Process 1' contains 'Action 1' and 'Action 2'.
    """
    def __init__(self, start, end):
        super().__init__('contains', 'contained in', start, end)


class Pairs(Relationship):
    """
    'Pairs' represents a pair relationship.
    e.g.,) 'Process 1' is paired with 'Process 1_END'.
    """
    def __init__(self, start, end):
        super().__init__('pairs', 'paired with', start, end)


class Performs(Relationship):
    """
    'Performs' represents a performing relationship.
    e.g.,) 'Component A' performs 'Process 1' or 'Action 2'.
    """
    def __init__(self, start, end):
        super().__init__('performs', 'performed by', start, end)


class RequiredBy(Relationship):
    """
    'RequiredBy' represents a requiring relationship.
    e.g.,) 'Component A' requires 'Component B', so that 'Component A' can depend on 'Component B'.
    This relationship is used for a physical simulation in which components are physically dependent on each other.
    """
    def __init__(self, start, end):
        super().__init__('required by', 'requires', start, end)


class TracedFrom(Relationship):
    """
    'TracedFrom' represents a tracing relationship.
    e.g.,) 'Component A' is traced from 'Requirement 1'.
    """
    def __init__(self, start, end):
        super().__init__('traced from', 'traced to', start, end)


class Relates(Relationship):
    """
    Not yet used
    """
    def __init__(self, start, end):
        super().__init__('relates', 'related to', start, end)



# Relationship for static entity

class Transfers(Relationship):
    """
    'Transfers' is used ...
    """
    def __init__(self, start, end):
        super().__init__('transfers', 'transferred by', start, end)

