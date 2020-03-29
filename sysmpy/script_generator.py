from sysmpy.entity import *
from sysmpy.relationship import *
import sys, inspect


class ScriptGenerator():
    def __init__(self):
        self.script = ''
        self.script_item = ''
        self.id = 0

    def run(self, en):
        self.script = ''
        if inspect.ismodule(en):
            self.to_script_from_module(en, None)
        else:
            self.to_script(en, None)

        self.script = self.script + self.script_item

        return self.script

    def to_script_from_module(self, module, parent_eid):
        for name, obj in inspect.getmembers(module):
            # print(name, obj)
            if isinstance(obj, Process) or isinstance(obj, Item) or isinstance(obj, Component):
                if obj.is_root is True:
                    self.to_script(obj, None)

    def to_script(self, entity, parent_eid):
        name = entity.name
        eid = f'ID{id(entity)}'
        if parent_eid is not None:
            parent = f'{parent_eid}.'
        else:
            parent = ''

        if isinstance(entity, Process):
            self.script += f'{eid} = {parent}Process(\'{name}\')\n'
        elif isinstance(entity, Action):
            self.script += f'{eid} = {parent}Action(\'{name}\')\n'
        elif isinstance(entity, Or):
            self.script += f'{eid} = {parent}Or()\n'
        elif isinstance(entity, And):
            self.script += f'{eid} = {parent}And()\n'
        elif isinstance(entity, END):
            self.script += f'{eid} = {parent}End()\n'
        elif isinstance(entity, ExitLoop):
            self.script += f'{eid} = {parent}ExitLoop()\n'
        elif isinstance(entity, Condition):
            self.script += f'{eid} = {parent}Condition(\'{name}\')\n'
        elif isinstance(entity, Loop):
            self.script += f'{eid} = {parent}Loop(times={entity.end.times})\n'
        elif isinstance(entity, Component):
            self.script_item += f'{eid} = {parent}Component(\'{name}\')\n'
        elif isinstance(entity, Item):
            self.script_item += f'{eid} = {parent}Item(\'{name}\')\n'

            if 'received by' in entity.inv_relation:
                receivers = [r.start for r in entity.inv_relation['received by'] if isinstance(r, Receives)]
                for receiver in receivers:
                    receiver_id = f'ID{id(receiver)}'
                    self.script_item += f'{receiver_id}.receives({eid})\n'

            if 'sent from' in entity.inv_relation:
                senders = [r.start for r in entity.inv_relation['sent from'] if isinstance(r, Sends)]
                for sender in senders:
                    sender_id = f'ID{id(sender)}'
                    self.script_item += f'{sender_id}.sends({eid})\n'

            if 'triggers' in entity.inv_relation:
                triggers = [r.start for r in entity.inv_relation['triggers'] if isinstance(r, Triggered)]
                for trigger in triggers:
                    trigger_id = f'ID{id(trigger)}'
                    self.script_item += f'{trigger_id}.triggered({eid})\n'

        # for all children
        if 'contains' in entity.relation:
            children = [r for r in entity.relation['contains'] if isinstance(r, Contains)]
            for i, c in enumerate(children):
                child = c.end
                self.to_script(child, eid)





