import sys
import os

module_path = os.path.abspath(os.path.join('..', "/".join(__file__.split('/')[0:-2])))
if module_path not in sys.path:
    sys.path.append(module_path)

print(sys.path[-1])