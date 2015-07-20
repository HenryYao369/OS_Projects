# -*- coding: utf-8 -*-

from threading import Thread, Lock, Semaphore, Condition
import time
import random

north = 0  # == left  -- I did this just because it's easier for me to think:)
south = 1  # == right

# lock = Semaphore(1)
# lock2 = Semaphore(1)

class OneLaneBridge(object):
    """
    A one-lane bridge allows multiple cars to pass in either direction, but at any
    point in time, all cars on the bridge must be going in the same direction.

    Cars wishing to cross should call the cross function, once they have crossed
    they should call finished()
    """

    def __init__(self):
        # TODO
        self.status = 1  # 0 for left and 1 for right. Cars' direction on bridge.

        self.driving_left_num = 0
        self.waiting_to_left_num = 0
        self.sema_left = Semaphore(0)

        self.driving_right_num = 0
        self.waiting_to_right_num = 0
        self.sema_right = Semaphore(0)


        # variables for debug:
        self.start_count = 1
        self.fin_count = 1
        self.start_count_mutex = Semaphore(1)
        self.fin_count_mutex = Semaphore(1)


    def cross(self,direction):
        """wait for permission to cross the bridge.  direction should be either
        north (0) or south (1)."""
        # TODO

        # with lock:
        with self.start_count_mutex:
            print 'enter_cross:' + str(self.start_count),'direction:', direction
            self.start_count += 1

        if direction == 1:  # toward right
            if self.status == 1:
                self.driving_right_num += 1

            elif self.status == 0:
                self.waiting_to_right_num += 1
                self.sema_right.acquire()

            else:
                print 'error 2'

        elif direction == 0:  # toward left
            if self.status == 0:
                self.driving_left_num += 1

            elif self.status == 1:
                self.waiting_to_left_num += 1
                self.sema_left.acquire()

            else:
                print 'error 1'

        else:
            print 'At cross function: direction error!'



    def finished(self):
        # TODO

        # with lock2:
        if self.status == 1:
            if self.driving_right_num > 0:
                self.driving_right_num -= 1

            # Next line: change else to if
            if self.driving_right_num == 0:
                # self.driving_right_num = 0
                self.status = 0
                for i in xrange(self.waiting_to_left_num):
                    self.sema_left.release()
                self.waiting_to_left_num = 0

            # elif self.driving_right_num == 0:
            #     pass

            else:
                print 'error 3'

        if self.status == 0:
            if self.driving_left_num > 0:
                self.driving_left_num -= 1

            # Next line: change else to if
            if self.driving_left_num == 0:
                # self.driving_left_num = 0
                self.status = 1
                for i in xrange(self.waiting_to_right_num):
                    self.sema_right.release()
                self.waiting_to_right_num = 0

            # elif self.driving_left_num == 0:
            #     pass

            else:
                print 'error 4'


        with self.fin_count_mutex:
            print 'finish ' + str(self.fin_count)
            self.fin_count += 1




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
        self.status = -100  # initial value; 0 for left and 1 for right. Cars' direction on bridge.

        self.left_driving = Condition(self.lock)  # pred: self.right_num == 0
        self.right_driving = Condition(self.lock)  # pred: self.left_num == 0

        # variables for debug:
        self.start_count = 1
        self.fin_count = 1

    def cross(self,direction):
        with self.lock:
            # print 'enter ' + str(self.start_count), self.status  # 为啥第一次写错了，阻塞了后面好多线程，这里还能
            # 打印到100？？————因为wait()方法的时候，其他thread就可以进来的！！
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

            print 'finish ' + str(self.fin_count)
            self.fin_count += 1

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

    judd_falls = OneLaneBridge()
    for i in range(100):
        Car(judd_falls).start()

    # ithaca_falls = OneLineBridgeMonitor()
    # for i in range(100):
    #     Car(ithaca_falls).start()

# vim:expandtab:tabstop=8:shiftwidth=4:softtabstop=4

