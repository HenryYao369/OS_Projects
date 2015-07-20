# -*- coding: utf-8 -*-

from threading import Thread, Lock, Semaphore, Condition
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

    def __init__(self):
        # TODO
        pass

    def cross(self,direction):
        """wait for permission to cross the bridge.  direction should be either
        north (0) or south (1)."""
        # TODO
        pass

    def finished(self):
        # TODO
        pass


class Car(Thread):
    def __init__(self, bridge):
        Thread.__init__(self)
        self.direction = random.randrange(2)
        self.wait_time = random.uniform(0.1,0.5)
        self.bridge    = bridge

    def run(self):
        # drive to the bridge
        time.sleep(self.wait_time)

        # [request permission] to cross
        self.bridge.cross(self.direction)

        # drive across
        time.sleep(0.01)

        # [signal] that we have finished crossing
        self.bridge.finished()


class OneLineBridgeMonitor(object):
    def __init__(self):

        self.lock = Lock()

        self.left_num = 0
        self.right_num = 0
        self.status = -100

        self.left_driving = Condition(self.lock)  # pred: self.right_num == 0
        self.right_driving = Condition(self.lock)  # pred: self.left_num == 0

        # variables for debug:
        self.start_count = 1
        self.fin_count = 1

    def cross(self,direction):
        with self.lock:
            # print 'enter ' + str(self.start_count), self.status
            # self.start_count += 1
            if direction == 0:  # toward left
                # self.toward_left()
                while not (self.right_num==0):
                    self.left_driving.wait()
                self.left_num += 1
                self.status = 0

            elif direction == 1:  # toward right
                # self.toward_right()
                while not (self.left_num==0):
                    self.right_driving.wait()
                self.right_num += 1
                self.status = 1

            else:
                print 'not south/north, Error!'

            print 'enter_cross:' + str(self.start_count),'direction:', self.status
            self.start_count += 1

    '''
    # private
    def toward_left(self):
        # with self.lock:
        while not (self.left_num==0):
            self.no_left.wait()
        self.left_num += 1

    # private
    def toward_right(self):
        # with self.lock:
        while not (self.right_num==0):
            self.no_right.wait()
        self.right_num += 1
    '''

    def finished(self):
        with self.lock:
            print 'finish ' + str(self.fin_count)
            self.fin_count += 1

            if self.status == 0:  # toward left
                # self.finish_left()
                self.left_num -= 1
                if self.left_num == 0:
                    self.right_driving.notifyAll()
            elif self.status == 1:  # towards right
                # self.finish_right()
                self.right_num -= 1
                if self.right_num == 0:
                    self.left_driving.notifyAll()
            else:
                print 'in finished: Error! -- status'

    '''
    # private
    def finish_left(self):
        # with self.lock:
        self.left_num -= 1
        if self.left_num == 0:
            self.no_left.notifyAll()

    # private
    def finish_right(self):
        # with self.lock:
        self.right_num -= 1
        if self.right_num == 0:
            self.no_right.notifyAll()
    '''




if __name__ == "__main__":

    # judd_falls = OneLaneBridge()
    # for i in range(100):
    #     Car(judd_falls).start()

    ithaca_falls = OneLineBridgeMonitor()
    for i in range(100):
        Car(ithaca_falls).start()

# vim:expandtab:tabstop=8:shiftwidth=4:softtabstop=4

