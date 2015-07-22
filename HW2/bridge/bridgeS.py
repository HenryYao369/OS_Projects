from threading import Thread, Lock, Semaphore, Condition
import time
import random

north = 0
south = 1


# Semaphore for car enter or exit the bridge
sgate = Semaphore()

# Semaphore for waiting car ask for access
# This Semaphore is only available for waiting cars
# when no more other direction cars on the bridge
# signal semaphore
saccess = Semaphore()

#firt car came to wait queue is the representative
srep = Semaphore()


class OneLaneBridge(object):

    #A one-lane bridge allows multiple cars to pass in either direction, but at any
    #point in time, all cars on the bridge must be going in the same direction.

    #Cars wishing to cross should call the cross function, once they have crossed
    #they should call finished()


    def __init__(self):
        # TODO
        # initialization : no car on brige, direction -1
        
        # protected by sgate and srep(for waiting zone)
        self.carnum = 0
        # protected by sgate and srep(for waiting zone)
        self.direction = -1
        # protected by sgate and srep
        self.wait = 0
    
   
    def cross(self,direction):
        #wait for permission to cross the bridge.  direction should be either
        #north (0) or south (1).
        # TODO
        # check what direction is allowed to cross the bridge now
        # need to check coming car's direction
        # car has same direction with bridge can go, car has different direction need go to wait zone
        
        sgate.acquire()
        
        #at the beginning, or no car wait after carnum==0
        if self.direction == -1:
            saccess.acquire()
            self.direction = direction
            self.carnum = self.carnum + 1
            #print self.carnum, self.direction
         
            sgate.release()
        
        
        #Currently, there are cars on bridge, or cars in wait zone
        else:
            #Coming car has same direction with bridge
            if self.direction == direction:
                self.carnum = self.carnum + 1
                #print self.carnum, self.direction
               
                sgate.release()
 
            # Coming car has different direction with bridge
            # put this car into waiting area
            else:
                #First waiting car is the representative car, when bridge no longer has cars on it
                # this representative car will get the access to the bridge and let other waiting car go
                if self.wait == 0:
                   
                    srep.acquire()
                    self.wait = self.wait + 1
                    #print self.wait, direction, "#"
                    sgate.release()
                    saccess.acquire()
                    self.carnum = self.carnum + 1
                    self.wait = self.wait - 1
                    
                    if self.wait == 0:
                        self.direction = direction
                        sgate.release()
                    srep.release()
            
                
                else:
                    self.wait = self.wait + 1
                    #print self.wait, direction, "#"
                    sgate.release()
                    srep.acquire()
                    self.wait = self.wait - 1
                    self.carnum = self.carnum + 1
                    if self.wait == 0:
                        self.direction = direction
                        sgate.release()
                    srep.release()


    def finished(self):
        # TODO
        # decrease car num when it leaves bridge
        # when no car on bridge, and waiting zone is not empty
        # let the cars in waiting zone go first
        sgate.acquire()
        
        self.carnum = self.carnum - 1
        #print self.carnum, self.direction, "*"
        
        #When no car on bridge
        if self.carnum == 0:
            #let waiting cars go first
            if self.wait != 0:
                saccess.release()
            #if there is no waiting car, reset the default bridge direction
            else:
                self.direction = -1
                sgate.release()
                saccess.release()

        else:
                sgate.release()



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
        # other thread can run only after current thread go to sleep
        time.sleep(0.01)

        # signal that we have finished crossing
        self.bridge.finished()


if __name__ == "__main__":

    judd_falls = OneLaneBridge()
    for i in range(100):
        Car(judd_falls).start()

# vim:expandtab:tabstop=8:shiftwidth=4:softtabstop=4

