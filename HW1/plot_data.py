__author__ = 'Hengzhi'

import parcount
import sys,time
from subprocess import Popen


f = open('data_CPU_bound.txt','w')

f.write('thread:'+'\n')
for i in xrange(1,21):
    start_time = time.time()
    p = Popen([sys.executable,'parcount.py','threaded',str(i)])  # let program launch program: cool!!
    p.wait()

    delta = time.time() - start_time
    f.write(str(delta)+'\n')

f.write('subproc:'+'\n')


for i in xrange(1,21):
    start_time = time.time()
    p = Popen([sys.executable,'parcount.py','parent',str(i)])
    p.wait()

    delta = time.time() - start_time
    f.write(str(delta)+'\n')

f.close()





