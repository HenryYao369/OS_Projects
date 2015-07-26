__author__ = 'Hengzhi'

from threading import Semaphore

s = Semaphore()
s.acquire()

# s.acquire()

s.release()
s.acquire()


s.release()
s.release()
s.release()
s.acquire()
s.acquire()
s.acquire()

# s.acquire()
if s > 0:
    print( 'nihao')

