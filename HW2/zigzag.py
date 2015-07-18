from threading import Thread, Lock, Semaphore
import sys

#
# Using semaphores, modify the program below so that it prints the following:
#

result = """
---
   |
   |
    ---
       |
       |
        ---
           |
           |
"""

#
# You may split for loops into multiple loops, but the total number of
# iterations should remain the same.
#

dash_semaphore = Semaphore(1)  # 9
vertical_semaphore = Semaphore(0)  # 6
newLine_semaphore = Semaphore(0)  # 9
white_semaphore = Semaphore(0)  # 54


class Dash(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):

        dash_semaphore.acquire()
        for j in range(3):
            sys.stdout.write("-")
        # dash_semaphore.release()
        newLine_semaphore.release()

        dash_semaphore.acquire()
        for j in range(3):
            sys.stdout.write("-")
        newLine_semaphore.release()

        dash_semaphore.acquire()
        for j in range(3):
            sys.stdout.write("-")
        newLine_semaphore.release()



class Vertical(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        for i in range(6):
            vertical_semaphore.acquire()
            sys.stdout.write("|")
            newLine_semaphore.release()

class NewLine(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):

        for i in range(9):
            newLine_semaphore.acquire()
            sys.stdout.write("\n")
            white_semaphore.release()


class White(Thread):

    def __init__(self):
        Thread.__init__(self)

    def run(self):
        white_semaphore.acquire()
        for i in range(3):
            sys.stdout.write(" ")
        vertical_semaphore.release()

        white_semaphore.acquire()
        for i in range(3):
            sys.stdout.write(" ")
        vertical_semaphore.release()

        white_semaphore.acquire()
        for i in range(4):
            sys.stdout.write(" ")
        dash_semaphore.release()

        white_semaphore.acquire()
        for i in range(7):
            sys.stdout.write(" ")
        vertical_semaphore.release()

        white_semaphore.acquire()
        for i in range(7):
            sys.stdout.write(" ")
        vertical_semaphore.release()

        white_semaphore.acquire()
        for i in range(8):
            sys.stdout.write(" ")
        dash_semaphore.release()

        white_semaphore.acquire()
        for i in range(11):
            sys.stdout.write(" ")
        vertical_semaphore.release()

        white_semaphore.acquire()
        for i in range(11):
            sys.stdout.write(" ")
        vertical_semaphore.release()



if __name__ == "__main__":
    Dash().start()
    Vertical().start()
    NewLine().start()
    White().start()

## vim: et ai ts=4 sw=4

