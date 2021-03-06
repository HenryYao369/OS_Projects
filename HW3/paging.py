# coding=utf-8
import time
import sys

################################################################################
## Shared paging simulation infrastructure #####################################
################################################################################

class Pager(object):
  """Pager objects implement page replacement strategies.  A program can call
     pager.access(addr) to indicate that the given address is being accessed;
     the Pager will ensure that that page is loaded and return the corresponding
     frame number.

     The Pager keeps track of the number of page faults."""
  def __init__(self, num_frames, page_size):
    self.page_faults = 0

    self.frames      = [None for i in range(num_frames)]
    self.num_frames  = num_frames

    self.page_size   = page_size


  # protected
  def evict(self):
    """return the frame number of a page to be evicted."""
    # This will be implemented in your subclasses below.
    raise NotImplementedError


  # public
  def access(self, address):
    """loads the page containing the address into memory and returns the
    frame number of the loaded page."""

    page_num = address / self.page_size  # page_num will be casted into integer!
    if page_num in self.frames:
      # hit
      return self.frames.index(page_num)
    else:
      # fault
      self.page_faults += 1

      index = self.evict()
      self.frames[index] = page_num

      return index


################################################################################
## Paging algorithm implementations ############################################
################################################################################

class FIFO(Pager):
  def __init__(self, num_frames, page_size):
    Pager.__init__(self, num_frames, page_size)
    # TODO
    self.ptr = self.num_frames - 1


  def access(self, address):
    # TODO: you may wish to do additional bookkeeping here.

    return Pager.access(self, address)

  def evict(self):
    # TODO
    # raise NotImplemented
    self.ptr = (self.ptr +1) % self.num_frames
    return self.ptr


class LRU(Pager):
  def __init__(self, num_frames, page_size):
    Pager.__init__(self, num_frames, page_size)
    # TODO
    self.ts = [None for i in xrange(self.num_frames)]  # ts: timestamp

  def access(self, address):
    # TODO: you may wish to do additional bookkeeping here.

    page_num = address / self.page_size  # page_num will be casted into integer!
    if page_num in self.frames:
        # hit
        index = self.frames.index(page_num)
        self.ts[index] = time.time()

    return Pager.access(self, address)

  def evict(self):
    # TODO
    # raise NotImplemented

    index = self.ts.index(min(self.ts))  # note:min(2,None) => None, so here we don't have to judge 'None' -- Python is great!
    self.ts[index] = time.time()
    return index



class OPT(Pager):
  def __init__(self, num_frames, page_size, trace):
    """trace is a list of addresses; the full trace of accesses that will be
       performed"""
    Pager.__init__(self, num_frames, page_size)
    # TODO
    self.trace_ptr = -1
    self.future_pos = [None for i in xrange(num_frames)]


    self.list_of_list = [[] for i in xrange(1024/self.page_size+1)]  # 这是一个查找表，以空间换时间！

    for i in xrange(len(trace)):
        self.list_of_list[trace[i]/self.page_size].append(i)
    # for list in self.list_of_list:
    #     print list


  def access(self, address):
    # TODO: you may wish to do additional bookkeeping here.
    self.trace_ptr += 1


    return Pager.access(self, address)

  def evict(self):
    # TODO
    # raise NotImplemented

    if None in self.frames: # still during initialization
        return self.frames.index(None)

    for i in xrange(self.num_frames):

      page_num_to_lookup = self.frames[i]

      while True:
        if len(self.list_of_list[page_num_to_lookup]) < 1:
          self.future_pos[i] = sys.maxint
          break

        if self.list_of_list[page_num_to_lookup][0] <= self.trace_ptr:
          self.list_of_list[page_num_to_lookup].remove(self.list_of_list[page_num_to_lookup][0])

        else:
          self.future_pos[i] =  self.list_of_list[page_num_to_lookup][0]
          break



    index_to_evict = self.future_pos.index(max(self.future_pos))
    return index_to_evict




################################################################################
## Command line parsing and main driver ########################################
################################################################################

if __name__ == '__main__':
  import argparse
  parser = argparse.ArgumentParser(description="simulate various page replacement algorithms")


  parser.add_argument("-s","--page-size", help="the number of pages",
                      type=int, required=True)
  parser.add_argument("-n","--num-frames", help="the number of frames",
                      type=int, required=True)
  parser.add_argument("algorithm", choices=["FIFO", "LRU", "OPT"],
                      help="the replacement strategy to use")
  parser.add_argument("trace",  help="the sequence of addresses to access.  Should be a filename containing one address per line.",
                      type=file)

  args = parser.parse_args()

  trace = [int(line) for line in args.trace.readlines()]
  # 非常简洁的一种写法，学习！  对每一行，读，并强制转化为int。  有点lambda exp的感觉？！


  start_time = time.time()
  pager = None
  if args.algorithm == "LRU":
    pager = LRU(args.num_frames, args.page_size)
  elif args.algorithm == "FIFO":
    pager = FIFO(args.num_frames, args.page_size)
  elif args.algorithm == "OPT":
    pager = OPT(args.num_frames, args.page_size, trace)


  for addr in trace:
    frame = pager.access(addr)
    assert(pager.frames[frame] == addr / args.page_size)

  print("total page faults: %i" % pager.page_faults)
  print "elapsed time: ", time.time() - start_time

# vim: ts=2 sw=2 ai et list

