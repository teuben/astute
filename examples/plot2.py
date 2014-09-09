#! /usr/bin/env python
#! /usr/bin/env ipython --pylab=qt
#
import sys, os
import numpy as np

# support for interactive/non-interactive mode depends upon the backend.
# pylab mode vs. pyplot mode

if False:
    # Agg is great for never showing a figure on the screen, but using in batch mode only
    import matplotlib
    matplotlib.use('Agg')



import matplotlib.pyplot as plt

#if matplotlib.is_interactive():
#    matplotlib.use('Agg')
#fig.set_size_inches(8.27, 11.69)
#fig.savefig('test.pdf')


x = np.arange(10)
y = np.sqrt(x)
z = x*x

mode = 0    # nothing
mode = 1    # plot on screen
mode = 2    # plot in file
mode = 3    # both


mode=1

if mode==1:
    # on screen and blocking
    #
    print "on screen and blocking"
    plt.ioff()
    #plt.ion()
    fig = plt.figure(1)
    ax1 = fig.add_subplot(1,1,1)
    ax1.plot(x,y)
    #plt.show()
    plt.ioff()
    #
    fig = plt.figure(2)
    ax2 = fig.add_subplot(1,1,1)
    ax2.plot(x,z)
    plt.show()
elif mode==2:
    # batch mode ; just a file
    print "batch mode ; just a file"
    plt.ioff()
    fig = plt.figure(1)
    ax1 = fig.add_subplot(1,1,1)
    ax1.plot(x,y)
    fig.savefig('plot2a.png')
    #
    fig = plt.figure(2)
    ax2 = fig.add_subplot(1,1,1)
    ax2.plot(x,z)
    fig.savefig('plot2b.png')
    # plt.clf()
elif mode==3:
    # batch mode + screen version
    print "batch mode + screen version"
    plt.ioff()
    fig = plt.figure(1)
    ax1 = fig.add_subplot(1,1,1)
    ax1.plot(x,y)
    fig.savefig('plot2a.png')
    plt.show()
    #
    fig = plt.figure(2)
    ax2 = fig.add_subplot(1,1,1)
    ax2.plot(x,z)
    fig.savefig('plot2b.png')
    plt.show()



#
#   screen:         + show
#   file:   savefig + clf (clf doesn't seem to matter)
#   s+f:    savefig + show
#
#   but the screen all blocks.  how can we keep a plot on screen and continue computing?

# use this?
#import matplotlib
#matplotlib.use('Agg')


if False:
    if use_screen:
        plt.show()
    if figname:
        fig.savefig(figname)
    
