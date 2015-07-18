from threading import Thread, Lock, Semaphore  # why I did not use Lock??

sema = Semaphore(1)

class Add(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        # sema.acquire()
        for j in range(10000):
            # sema.acquire()
            for i in range(10):
                sema.acquire()
                matrix[i] = matrix[i] + 1
                sema.release()
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
                sema.acquire()
                matrix[i] = matrix[i] - 1
                sema.release()
            # sema.release()
        # sema.release()


matrix = [90, 90, 90, 90, 90, 90, 90, 90, 90, 90]

a = Add()
s = Sub()

a.start()
s.start()

a.join()
s.join()

print matrix


## vim: et ai ts=4 sw=4

