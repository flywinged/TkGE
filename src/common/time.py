# Quick module for giving accurate times based on which platform is calling the time

import time as pythonTime
import sys

from types import FunctionType
timeFunction: FunctionType = None

if sys.platform == "win32":
    timeFunction = pythonTime.clock
else:
    timeFunction = pythonTime.time
