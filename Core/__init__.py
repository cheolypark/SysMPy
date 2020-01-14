""" This package declares meta data for SAI schema.
"""

# Meta can't be accessed from here... TODO verify with Young
# from Meta import *

# Force __all__ modules to be imported when importing Core package
from Core import *

# Only these modules will be imported with "import *"
__all__ = ["entity", "relationship"]