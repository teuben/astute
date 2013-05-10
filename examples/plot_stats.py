#! /usr/bin/env python
#

from astropy.io import ascii
import matplotlib.pyplot as plt
import numpy as np
import math
import sys

degrad = 57.2957795

def gettab(file):
    data = ascii.read(file)
    return data

def plot1(data, label='',efactor=1,rmax=2):
    # iz z min  max  N  mean sigma skew kurt sum sum  robust[N mean sig med]
    ch   = data['col1']
    freq = data['col2']/1e9
    peak = data['col4']*1000
    rms  = data['col7']*1000
    rrms = data['col14']*1000
    son  = peak/rrms
    # trms = trend(rrms)/1.41
    #
    fig = plt.figure()
    plt.suptitle('CUBE stats :  (%s)' % label)
    #
    ax1 = fig.add_subplot(2,3,1)
    ax1.set_title('peak rms rrms')
    ax1.plot(freq,peak)
    ax1.plot(freq,rms)
    ax1.plot(freq,rrms)
    ax1.set_ylim([0,100])
    ax1.xaxis.label.set_size(10)
    ax1.yaxis.label.set_size(10)
    #
    ax2 = fig.add_subplot(2,3,2)
    ax2.set_title('peak/rrms')
    ax2.plot(freq,son)
    ax2.set_ylim([0,16])
    ax2.xaxis.label.set_size(10)
    ax2.yaxis.label.set_size(10)
    #
    ax3 = fig.add_subplot(2,3,3)
    ax3.set_title('histo rrms')
    ax3.hist(rrms,bins=80,range=[0,10])
    ax3.xaxis.label.set_size(10)
    ax3.yaxis.label.set_size(10)
    #
    ax4 = fig.add_subplot(2,3,4)
    ax4.set_title('log peak,rms,rrms')
    ax4.plot(freq,np.log(peak))
    ax4.plot(freq,np.log(rms))
    ax4.plot(freq,np.log(rrms))
    ax4.xaxis.label.set_size(10)
    ax4.yaxis.label.set_size(10)
    #
    plt.show()
    fig.savefig('stats.pdf')

if __name__ == "__main__":
    name = sys.argv[1]
    data = gettab(name)
    plot1(data,name)
