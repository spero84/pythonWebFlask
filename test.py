import os
from datetime import datetime

dir1 = os.path.dirname(os.path.dirname(__file__))
dir2 = os.path.dirname(__file__)

print(dir1)
print(dir2)
print(datetime.now())