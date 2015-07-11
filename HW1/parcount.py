"""A simulation for experimenting with multiple threads and processes"""

from threading import Thread
import sys  # ??
from subprocess import Popen  # subprocess

import time
import random

# from Queue import Queue


# Queue q = Queue()


################################################################################
## unit of work ################################################################
################################################################################

def do_step(i):
  """simulates a task that requires a bit of processing and some I/O"""

  time.sleep(0.01)  # IO bound.

  random.seed(i)
  val = random.gauss(0,2)
  if (val > 1):
    return 1
  else:
    return 0

def do_steps(k, n, N):
  """given N units of work divided into n batches, performs the kth batch (k is
     in the range [kN/n,(k+1)N/n)."""
  start  = k * N/n
  finish = min((k+1) * N/n, N)

  value = 0
  for i in range(start,finish):
    value += do_step(i)
  return value

################################################################################
## sequential implementation ###################################################
################################################################################

def run_sequential(N):
  """perform N steps sequentially"""
  return do_steps(0,1,N)

################################################################################
## threaded implementation #####################################################
################################################################################

class ThreadedWorker(Thread):
  def __init__(self,k,n,N):
    """initialize this thread to be the kth of n worker threads"""
    Thread.__init__(self)
    self.k      = k
    self.n      = n
    self.N      = N
    self.result = None

  def run(self):
    """execute the worker thread's work"""
    self.result = do_steps(self.k, self.n, self.N)



def run_threaded(num_threads, N):
  """use num_thread threads to perform N steps"""
  # TODO: create num_threads workers
  # TODO: run them
  # TODO: collect the results and return their sum

  sum = 0

  threads = []
  for i in xrange(num_threads):
    t = ThreadedWorker(i,num_threads,N)
    threads.append(t)

  for t in threads:
    # t.setDaemon(True)
    t.start()

  for t in threads:
    t.join()

  for t in threads:
    sum += t.result

  return sum

  # Note: use the threading module from the python standard library
  # Note: import threading; help(threading.Thread)
  # Note: be sure that your implementation is concurrent!

  # pass

################################################################################
## multiprocess implementation #################################################
################################################################################

def run_parent(num_children, N):
  """use num_children subprocesses to perform N steps"""
  # TODO: fork num_children subprocesses to compute the results
  # Note: use the python subprocess module
  # Note: use sys.executable to find python itself, and sys.argv[0] to get the
  #       name of the python script to run
  # Note: the child processes will exit with the exit code returned by
  #       run_child.  See __main__ below.  This is an abuse of the exit code
  #       system, which is intended to indicate whether a program failed or not,
  #       but since we're only trying to communicate a single integer from the
  #       child process to the parent, it suits our purposes.
  # Note: be sure that your implementation is concurrent!
  pass

def run_child(N):
  """do the work of a single subprocess"""
  # TODO: do the work for the ith (of n) children
  pass

################################################################################
## program main function #######################################################
################################################################################

def usage():
  print """
expected usage:
  %s %s <args>

where <args> is one of:
  sequential
  threaded  <num_threads>
  parent    <num_subprocesses>
  child     <arguments up to you>
""" % (sys.executable, sys.argv[0])
  return -1

if __name__ == '__main__':
  """parse the command line, execute the program, and print out elapsed time"""
  N = 100
  start_time = time.time()

  if len(sys.argv) <= 1:
    sys.exit(usage())
  command = sys.argv[1]

  if command == "sequential":
    print run_sequential(N)

  elif command == "threaded":
    if len(sys.argv) <= 2:
      sys.exit(usage())
    print run_threaded(int(sys.argv[2]), N)

  elif command == "parent":
    if len(sys.argv) <= 2:
      sys.exit(usage())
    print run_parent(int(sys.argv[2]), N)

  elif command == "child":
    # Note: this is an abuse of the exit status indication
    sys.exit(run_child(N))

  else:
    sys.exit(usage())

  print "elapsed time: ", time.time() - start_time

