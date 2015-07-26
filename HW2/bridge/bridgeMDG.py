from threading import Thread, Lock, Semaphore
import time
import random

north = 0
south = 1

class OneLaneBridgeMonitor(object):
    """
    A one-lane bridge allows multiple cars to pass in either direction, but at any
    point in time, all cars on the bridge must be going in the same direction.

    Cars wishing to cross should call the cross function, once they have crossed
    they should call finished()
    """

    def __init__(self):
        self.lock = Lock()

        self.direction    = None
        self.num_crossing = 0

        self.is_safe = [Condition(lock), Condition(lock)]
        # predicate[north]: direction == north or num_crossing == 0
        # predicate[south]: direction == south or num_crossing == 0

    def cross(self,direction):
        with self.lock:
            while not (self.direction == direction or num_crossing == 0):
                self.is_safe[direction].wait()

            self.num_crossing += 1
            # no need to notify: can't make any predicate become true

            self.direction     = direction
            # no need to notify: can only make predicate[d] become true, but it
            # was already true.

    def finished(self):
        # precondition: is_safe[self.direction] holds and num_crossing > 0

        with self.lock:
            self.num_crossing -= 1

            if self.num_crossing == 0:
                # predicate[d] was true before, but the other predicate just
                # became true
                self.is_safe[1 - self.direction].notifyAll()


def P(sema):
    sema.acquire()

def V(sema):
    sema.release()

class OneLaneBridgeSema(object):
    """
    A one-lane bridge allows multiple cars to pass in either direction, but at any
    point in time, all cars on the bridge must be going in the same direction.

    Cars wishing to cross should call the cross function, once they have crossed
    they should call finished()
    """

    # implementation strategy:
    #    There is a single bridge mutex, and a mutex for each end.
    #
    #    If any car is on the bridge, then the bridge mutex will be 0, so no
    #    other thread will be able to acquire it.
    #
    #    The first car going in direction d will block on the bridge.
    #    Additional cars going in direction d will block on the end mutex.

    def __init__(self):
        # signal that the bridge is empty
        self.bridge_signal = Semaphore(0)

        # protected by bridge_mutex
        self.direction    = None

        # num_crossing[d] : number of cars currently crossing in direction d
        # protected by head_of_bridge_mutex
        self.num_crossing = [0, 0]
        self.end_mutex    = [Semaphore(1), Semaphore(1)]

        # signal that the bridge is free!
        V(self.bridge_signal)

    def cross(self,direction):

        P(self.end_mutex[direction])

        # if your direction doesn't have the bridge, wait for the signal
        if self.num_crossing[direction] == 0:
            P(self.bridge_signal)
            self.direction = direction

        self.num_crossing[direction] += 1

        V(self.end_mutex[direction])

    def finished(self):

        # read of self.direction is safe because direction never changes
        # between when this thread returned from cross() and when it reaches
        # this line.

        P(self.head_of_bridge[self.direction])

        self.num_crossing[self.direction] -= 1

        # if you're the last to leave, tell the world that the bridge is free!
        if self.num_crossing[self.direction] == 0:
            V(self.bridge_signal)

        self.head_of_bridge[self.direction].release()


class Car(Thread):
    def __init__(self, bridge):
        Thread.__init__(self)
        self.direction = random.randint(1)
        self.wait_time = random.randfloat(0.5)
        self.bridge    = bridge

    def run(self):
        thread.sleep(self.wait_time)
        bridge.cross(self.direction)

        thread.sleep(0.01)

        bridge.finished()


if __name__ == "__main__":

    judd_falls = OneLaneBridge()
    for i in range(100):
        Car(judd_falls).start()

# vim:expandtab:tabstop=8:shiftwidth=4:softtabstop=4

