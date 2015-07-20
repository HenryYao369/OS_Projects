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

    def __init__(self):
        # TODO

        # Cars' direction on bridge.
        self.gate_direction = 1  # 0 for left and 1 for right.
        self.gate_direction_mutex = Semaphore(1)


        # left side variables and their mutex
        self.driving_left_num = 0
        self.driving_left_num_mutex = Semaphore(1)

        self.waiting_to_left_num = 0
        self.waiting_to_left_num_mutex = Semaphore(1)
        self.sema_left = Semaphore(0)


        # right side variables and their mutex
        self.driving_right_num = 0
        self.driving_right_num_mutex = Semaphore(1)

        self.waiting_to_right_num = 0
        self.waiting_to_right_num_mutex = Semaphore(1)
        self.sema_right = Semaphore(0)


        # variables for debug (and their mutex):
        self.start_count = 1
        self.fin_count = 1
        self.printer_mutex = Semaphore(1)


    def cross(self,direction):
        """wait for permission to cross the bridge.  direction should be either
        north (0) or south (1)."""
        # TODO

        # with lock:
        with self.printer_mutex:
            print 'enter_cross:' + str(self.start_count),'direction:', direction
            self.start_count += 1

        if direction == 1:  # toward right

            with self.gate_direction_mutex:

                if self.gate_direction == 1:
                    with self.driving_right_num_mutex:
                        self.driving_right_num += 1

                elif self.gate_direction == 0:
                    with self.waiting_to_right_num_mutex:
                        self.waiting_to_right_num += 1
                    self.sema_right.acquire()

                else:
                    print 'error 2'

        elif direction == 0:  # toward left
            with self.gate_direction_mutex:
                if self.gate_direction == 0:
                    with self.driving_left_num_mutex:
                        self.driving_left_num += 1

                elif self.gate_direction == 1:
                    with self.waiting_to_left_num_mutex:
                        self.waiting_to_left_num += 1
                    self.sema_left.acquire()

                else:
                    print 'error 1'

        else:
            print 'At cross function: direction error!'



    def finished(self):
        # TODO

        # with lock2:
        with self.gate_direction_mutex:
            if self.gate_direction == 1:

                with self.driving_right_num_mutex:
                    if self.driving_right_num > 0:
                        self.driving_right_num -= 1

                    # Next line: change else to if
                    if self.driving_right_num == 0:
                        # self.driving_right_num = 0
                        self.gate_direction = 0

                        with self.waiting_to_left_num_mutex:
                            for i in xrange(self.waiting_to_left_num):
                                self.sema_left.release()
                            self.waiting_to_left_num = 0

                    # elif self.driving_right_num == 0:
                    #     pass

                    if self.driving_right_num < 0:
                        print 'error 3'

            if self.gate_direction == 0:

                with self.driving_left_num_mutex:
                    if self.driving_left_num > 0:
                        self.driving_left_num -= 1

                    # Next line: change else to if
                    if self.driving_left_num == 0:
                        # self.driving_left_num = 0
                        self.gate_direction = 1
                        with self.waiting_to_right_num_mutex:
                            for i in xrange(self.waiting_to_right_num):
                                self.sema_right.release()
                            self.waiting_to_right_num = 0

                    # elif self.driving_left_num == 0:
                    #     pass

                    else:
                        print 'error 4'


        with self.printer_mutex:
            print 'finish ' + str(self.fin_count)
            self.fin_count += 1


class Car(Thread):
    def __init__(self, bridge):
        Thread.__init__(self)
        self.direction = 1 #random.randrange(2)
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
        self.bridge.finished()


if __name__ == "__main__":

    judd_falls = OneLaneBridge()
    for i in range(100):
        Car(judd_falls).start()

# vim:expandtab:tabstop=8:shiftwidth=4:softtabstop=4

