import sys
import platform
from wx import version

__author__ = "Kumaran S/O Murugun"
__application__ = "The Watcher"
__version__ = "1.0 (Beta)"

PYTHON_VERSION = sys.version_info[0:2]
PyVersion = float(str(PYTHON_VERSION[0])+'.'+str(PYTHON_VERSION[1]))
WX_VERSION = version().split()[0]

SYSTEM = platform.system()
IS_OSX = SYSTEM == 'Darwin'
IS_WINDOWS = SYSTEM == 'Windows'