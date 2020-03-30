from sysmpy.entity import *
from sysmpy.relationship import *
import sys, inspect


class ModelGenerator():
    def __init__(self):
        pass

    def get_requirement_text(self, m):
        text = f"{m['WHO']} shall {m['VERB']} {m['WHAT']}"
        return text

    def to_requirement(self, model_info, parent_req=None):
        text = self.get_requirement_text(model_info)
        system = f"{model_info['WHO']}"

        if parent_req is not None:
            req = parent_req.Requirement(system, des=text)
        else:
            req = Requirement(system, des=text)

        return req

    def to_action_model_op(self, model_info, parent=None):
        p, a, i = None, None, None
        for k, v in model_info.items():
            v = str(v)
            if k == 'WHO':
                p = entity_db.get(v)
                if p is None:
                    p = Process(v)
            elif k == 'VERB':
                a = p.Action(v)
            elif k == 'WHAT':
                a.name += ' ' + v

        return p

    def to_action_model(self, model_info, parent=None):
        p = self.to_action_model_op(model_info, parent)
        return p