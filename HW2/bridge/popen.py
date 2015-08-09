
from subprocess import Popen
import sys

for i in xrange(100):
    p = Popen([sys.executable,'bridgeMDG_modf.py'])  # let program launch program: cool!!
    p.wait()

    print(i)