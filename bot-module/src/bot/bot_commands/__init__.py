from .trade import *
from .general import *
from .help import *

cmds = [obj for (name , obj) in vars().items()
                 if hasattr(obj, "__class__") and obj.__class__.__name__ == "Command"]