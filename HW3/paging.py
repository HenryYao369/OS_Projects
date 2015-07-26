
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

  def evict(self):
    """return the frame number of a page to be evicted."""
    # This will be implemented in your subclasses below.
    raise NotImplementedError

  def access(self, address):
    """loads the page containing the address into memory and returns the
    frame number of the loaded page."""

    page_num = address / self.page_size
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

  def access(self, address):
    # TODO: you may wish to do additional bookkeeping here.
    return Pager.access(self, address)

  def evict(self):
    # TODO
    raise NotImplemented


class LRU(Pager):
  def __init__(self, num_frames, page_size):
    Pager.__init__(self, num_frames, page_size)
    # TODO

  def access(self, address):
    # TODO: you may wish to do additional bookkeeping here.
    return Pager.access(self, address)

  def evict(self):
    # TODO
    raise NotImplemented


class OPT(Pager):
  def __init__(self, num_frames, page_size, trace):
    """trace is a list of addresses; the full trace of accesses that will be
       performed"""
    Pager.__init__(self, num_frames, page_size)
    # TODO

  def access(self, address):
    # TODO: you may wish to do additional bookkeeping here.
    return Pager.access(self, address)

  def evict(self):
    # TODO
    raise NotImplemented


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

# vim: ts=2 sw=2 ai et list

