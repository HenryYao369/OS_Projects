__author__ = 'Hengzhi'

import matplotlib.pyplot as plt


f = open('data_CPU_bound.txt','r')

a = f.readline()

thread_data = []
for i in xrange(20):
    data_str = f.readline()
    data = float(data_str)
    thread_data.append(data)

a = f.readline()


subproc_data = []
for i in xrange(20):
    data_str = f.readline()
    data = float(data_str)
    subproc_data.append(data)

x = range(1,21)
plt.plot(x, thread_data, 'rH-',label='multiplier bit:1',linewidth=3,markersize=10)
plt.plot(x, subproc_data, 'bv-', label='multiplier bit:2',linewidth=3,markersize=10)

plt.grid(True)
plt.show()
