""" This package declares meta data for SAI schema.
"""

# Force __all__ modules to be imported when importing sysmpy package
from sysmpy import *

# in __init__.py
from entity import *
from relationship import *
from interfaceanalyzer import *
from matrix_for_graph import *
from script_to_model import *
from script_generator import *
from sms_searcher import *

# Only these modules will be imported with "import *"
# __all__ = ["entity", "relationship"]

