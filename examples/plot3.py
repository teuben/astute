#! /usr/bin/env python
#
#  dual axes, but it shows how hard it is to change the axis order

import numpy as np
import matplotlib.pyplot as plt

freq  = np.arange(100.0, 102.0, 0.05)
freq0 = 101.5
c     = 300000.0
vlsr = (1 - freq/freq0) * c
vsys = 100
disp = 500
chan = np.arange(1,len(vlsr)+1)

arg = (vlsr-vsys)/disp

flux = np.exp(-0.5*arg*arg)


print freq
print vlsr
print flux




fig, ax1 = plt.subplots()
t = np.arange(0.01, 10.0, 0.01)
s1 = np.exp(t)
ax1.plot(freq, flux, 'b-')
ax1.set_xlabel('freq (GHz)')
ax1.set_ylabel('flux', color='b')
for tl in ax1.get_yticklabels():
    tl.set_color('b')

#  freq[0] to freq[n-1] probably easier if we know they're sorted
plt.axis([max(freq), min(freq), min(flux), max(flux)])
#plt.gca().invert_xaxis() # this doesn't match

if True:
    ax2 = ax1.twiny()
    ax2.plot(vlsr, flux, 'r.')
    ax2.set_xlabel('vlsr', color='r')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    plt.axis([min(vlsr), max(vlsr), min(flux), max(flux)])
    plt.show()
else:
    ax2 = ax1.twiny()
    ax2.plot(chan, flux, 'r.')
    ax2.set_xlabel('channel', color='r')
    for tl in ax2.get_yticklabels():
        tl.set_color('r')
    plt.axis([max(chan), min(chan), min(flux), max(flux)])
    plt.show()
