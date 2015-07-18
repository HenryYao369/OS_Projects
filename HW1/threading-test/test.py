__author__ = 'Hengzhi'

from threading import Semaphore

test_sema = Semaphore(0)
test_sema.acquire()

for i in range(8/5,19/3):
    print i


