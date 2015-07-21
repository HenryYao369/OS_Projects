from threading import Thread, Lock, Semaphore  # why I did not use Lock??
import time

# sema = Semaphore(1)

sema_list = []
for i in xrange(10):
    sema_list.append(Semaphore(1))

class Add(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # sema.acquire()
        for j in range(10000):
            # sema.acquire()
            for i in range(10):
                # sema.acquire()  # slower!
                sema_list[i].acquire()  #  faster!
                matrix[i] = matrix[i] + 1
                sema_list[i].release()
                # sema.release()
            # sema.release()
        # sema.release()


class Sub(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # sema.acquire()
        for j in range(10000):
            # sema.acquire()
            for i in range(10):
                # sema.acquire()
                sema_list[i].acquire()
                matrix[i] = matrix[i] - 1
                sema_list[i].release()
                # sema.release()
            # sema.release()
        # sema.release()


matrix = [90, 90, 90, 90, 90, 90, 90, 90, 90, 90]

a = Add()
s = Sub()

start_time = time.time()

a.start()
s.start()

a.join()
s.join()

print matrix

print "elapsed time: ", time.time() - start_time

## vim: et ai ts=4 sw=4

