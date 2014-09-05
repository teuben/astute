import sys, os
import atable
import numpy as np
import admit1 as admit
#import casa
import taskinit

class AT_linecube(admit.AT):
    """
    bdp_in[0]   bandcube
    bdp_in[1]   cubestats (needs cols::
    """
    name = 'LINECUBE'
    version = '1.0'
    keys = ['']
    def __init__(self,bdp_in=[],bdp_out=[]):
        admit.AT.__init__(self,self.name,bdp_in,bdp_out)
    def run(self):
        if not admit.AT.run(self):
            return False
        # specialized work can commence here
        fni = self.bdp_in[0].filename
        t = self.bdp_in[1].table
        freq  = t.get('frequency')
        sigma = t.get('sigma')
        peak  = t.get('max')
        print sigma
        ratio = np.log(sigma)-np.log(peak)
        t.plotter(freq,[ratio],'CubeStats-1',xlab='Freq',ylab='log(signal/noise)')
        t.histogram([ratio],'CubeStats-2',range=[0.3,0.5])

        taskinit.ia.open(fni)
        taskinit.ia.close()

        if self.do_pickle:
            self.pdump()
        if self.do_plot:
            print "nothing to print here yet"
