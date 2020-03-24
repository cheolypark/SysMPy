""" This package declares meta data for SAI schema.
"""

# Force __all__ modules to be imported when importing sysmpy package
# from sysmpy import *

# in __init__.py
from sysmpy.entity import *
from sysmpy.relationship import *
from sysmpy.interfaceanalyzer import *
from sysmpy.matrix_for_graph import *
from sysmpy.script_to_model import *
from sysmpy.script_generator import *
from sysmpy.sms_searcher import *

# Only these modules will be imported with "import *"
# __all__ = ["entity", "relationship"]

