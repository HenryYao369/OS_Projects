__author__ = 'Hengzhi'

import time

def worker():
    print "worker"
    time.sleep(1)
    return

if __name__ == "__main__":
    for i in xrange(5):
        worker()
