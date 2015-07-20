from threading import Thread, Lock, Semaphore
import time
import random


lock = Semaphore(1)

# primary colors

red    = 0
yellow = 1
blue   = 2

# the total number of paint cans available [red, yellow, blue]
max_available = [1, 1, 1]

# the number of paint cans of each color that are not in use
available     = max_available  # aliasing is not a good programming habit!

def check_invariants():
    """ensures that the number of available paint cans is sensible"""
    global available, max_available

    for color in [red, yellow, blue]:
        assert(0 <= available[color] <= max_available[color])

def mix():
    """simulates the mixing of paint"""

    sleep_time = random.randint(1, 10000)
    time.sleep(sleep_time/100000.0)


class Mixer(Thread):
    """A mixer is parameterized by two primary colors; it repeatedly acquires
       cans of both colors and mixes them."""

    def __init__(self, c1, c2):
        Thread.__init__(self)
        self.c1 = c1; self.c2 = c2

    def run(self):
        global available

        for i in range(5):

            lock.acquire()

            # acquire paint cans
            available[self.c1] -= 1
            available[self.c2] -= 1

            # sanity check
            check_invariants()

            # mix the paint
            mix()

            # release paint cans
            available[self.c1] += 1
            available[self.c2] += 1

            # sanity check
            check_invariants()

            lock.release()


if __name__ == "__main__":
    green  = Mixer(blue, yellow)
    orange = Mixer(red,  yellow)
    purple = Mixer(red,  blue)

    for worker in [green, orange, purple]:
        worker.start ()

# vim: et ai sw=4 ts=4

