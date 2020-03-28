from entity import *
from relationship import *
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
