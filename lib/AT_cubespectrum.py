import sys, os
import atable
import numpy as np
import casa
import admit1 as admit

class AT_cubespectrum(admit.AT):
    name = 'CUBESPECTRUM'
    version = '1.0'
    keys = ['pos']
    def __init__(self,bdp_in=[],bdp_out=[]):
        admit.AT.__init__(self,self.name,bdp_in,bdp_out)
    def run(self):
        if not admit.AT.run(self):
            return False
        # specialized work can commence here
        print "new CUBESPECTRUM"
        fn = self.bdp_in[0].filename

        # we expect a string "pos=maxposx,maxposy"
        if self.has('pos'):
            pp = self.get('pos')
            box = '%s,%s' % (pp,pp)
        else:
            pp = ""
            box = None
        #
        if len(self.bdp_in) == 1:
            # one BDP, it's the cube
            if box:
                vals = casa.imval(fn,box=box)
            else:
                vals = casa.imval(fn)
        elif len(self.bdp_in) == 2:
            # two BDP's, 2nd one is a CubeStats where we take the peak location
            b = self.bdp_in[1]
            pp = "%d,%d" % (b.maxpos[0],b.maxpos[1])
            box = '%s,%s' %  (pp,pp)
            vals = casa.imval(fn,box=box)
        else:
            print "no case implemented for > 2 BDP's"
            return
        #
        data = vals['data']
        # grab the X coords again
        h = casa.imhead(fn,mode='list')
        n = h['shape'][2]
        p = h['crpix3']
        d = h['cdelt3']
        v = h['crval3']
        ch = np.arange(n) + 1
        fr = ((ch-p-1)*d + v)/1e9


        a1 = atable.ATable([fr,data],['frequency','data'])
        # a1.pdump('cubespectrum.bin')
        self.bdp_out[0].table = a1
        data   = data * 1000              # in mJy/beam now
        print "Freq range : %g %g GHz" % (fr.min(), fr.max())
        print "Data range : %g %g mJy/beam" % (data.min(), data.max())
        if self.do_pickle:
            self.pdump()
        if self.do_plot:
            title = 'CubeSpectrum(%s)' % pp
            xlabel = 'Frequency (Ghz)'
            ylabel = 'Flux (mJy/beam)'
            a1.plotter(fr,[data],title,fn+'.png',xlab=xlabel,ylab=ylabel)
