from threading import Thread, Lock, Semaphore
import time
import random

north = 0
south = 1

class OneLaneBridge(object):
    """
    A one-lane bridge allows multiple cars to pass in either direction, but at any
    point in time, all cars on the bridge must be going in the same direction.

    Cars wishing to cross should call the cross function, once they have crossed
    they should call finished()
    """

    def  __init__(self):
        self.dir = -1
        self.bridge_access = Semaphore()
        self.cars_on_bridge = 0
        self.mutex = Semaphore()


    def cross(self,direction):
        """wait for permission to cross the bridge.  direction should be either
        north (0) or south (1)."""

        self.mutex.acquire()
        if(self.dir == -1):
            self.dir = direction

        if(direction == self.dir):
            if(self.cars_on_bridge == 0):
                self.bridge_access.acquire()
            self.cars_on_bridge += 1
        else:
            self.mutex.release()
            self.bridge_access.acquire()
            self.mutex.acquire()
            self.cars_on_bridge += 1
            self.dir = direction
            self.mutex.release()

        self.mutex.release()

    def finished(self,direction):
       self.mutex.acquire()
       self.cars_on_bridge -= 1 #car is now off the bridge
       if(self.cars_on_bridge == 0): #no more cars on bridge so release access
           self.bridge_access.release()
           self.dir = -1 #reset the direction so the next car will dictate the direction

       self.mutex.release()


class Car(Thread):
    def __init__(self, bridge):
        Thread.__init__(self)
        self.direction = random.randrange(2)
        self.wait_time = random.uniform(0.1,0.5)
        self.bridge    = bridge

    def run(self):
        # drive to the bridge
        time.sleep(self.wait_time)

        # request permission to cross
        self.bridge.cross(self.direction)

        # drive across
        time.sleep(0.01)

        # signal that we have finished crossing
        self.bridge.finished(self.direction)


if __name__ == "__main__":

    judd_falls = OneLaneBridge()
    for i in range(100):
        Car(judd_falls).start()

# vim:expandtab:tabstop=8:shiftwidth=4:softtabstop=4

