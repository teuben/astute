import sys, os
import atable
import numpy as np
import casa
import admit1 as admit

class AT_cubestats(admit.AT):
    name = 'CUBESTATS'
    version = '1.0'
    keys = ['sigma', 'ppp']
    def __init__(self,bdp_in=[],bdp_out=[]):
        admit.AT.__init__(self,self.name,bdp_in,bdp_out)
    def run(self):
        if not admit.AT.run(self):
            return False
        # specialized work can commence here
        use_ppp = False
        #
        fn = self.bdp_in[0].filename
        print "casa::imhead(%s)" % fn
        h = casa.imhead(fn,mode='list')
        n = h['shape'][2]
        p = h['crpix3']
        d = h['cdelt3']
        v = h['crval3']
        ch = np.arange(n) + 1        # 1-based channels
        fr = ((ch-p-1)*d + v)/1e9    # in GHz !!
        #
        print "casa::imstat(%s)" % fn
        imstat0 = casa.imstat(fn,           logfile='imstat0.logfile',append=False)
        imstat1 = casa.imstat(fn,axes=[0,1],logfile='imstat1.logfile',append=False)
        if use_ppp:
            print "Creating PeakPosPoint"
            # n= number of channels
            xpos = np.arange(n)
            ypos = np.arange(n)
            for i in range(n):
                s = casa.imstat(fn,chans='%d'%i)
                xpos[i] = s['maxpos'][0]
                ypos[i] = s['maxpos'][1]
        #
        c1 = 'max'
        c2 = 'sigma'
        c3 = 'medabsdevmed'
        c4 = 'mean'
        #
        print "Cube Stats:"
        print "  mean, sigma: %g %g  (%g) mJy/beam" % (imstat0[c4][0]*1000,imstat0[c3][0]*1000,imstat0[c2][0]*1000)
        print "  max: ", imstat0[c1][0]*1000," mJy/beam  @: ",imstat0['maxpos']

        col_names = ['channel','frequency','mean','sigma','max']
        col_data = [ ch, fr, imstat1[c1], imstat1[c2], imstat1[c3]] 
        if use_ppp:
            col_names.append(['maxposx','maxposy'])
            col_data.append([xpos,ypos])
        a1 = atable.ATable(col_data, col_names)
           

        self.bdp_out[0].table = a1
        self.bdp_out[0].mean  = imstat0[c4][0]
        self.bdp_out[0].sigma = imstat0[c3][0]
        self.bdp_out[0].max   = imstat0[c1][0]
        self.bdp_out[0].maxpos = [ imstat0['maxpos'][0], imstat0['maxpos'][1], imstat0['maxpos'][2] ]

        freq   = a1.get('frequency')            # in GHz 
        noise  = a1.get('sigma')*1000           # in mJy/beam now
        signal = a1.get('max')*1000             # in mJy/beam now
        print 'freq type ',freq.dtype
        print "Freq range : %g %g GHz" % (freq.min(), freq.max())
        print "Noise range : %g %g mJy/beam" % (noise.min(), noise.max())
        print "Peak Signal range : %g %g mJy/beam" % (signal.min(), signal.max())


        print "Cube Stats after pickle:"
        print "  mean, sigma: %g %g  (%g) mJy/beam" % (imstat0[c4][0]*1000,imstat0[c3][0]*1000,imstat0[c2][0]*1000)
        print "  max: ", imstat0[c1][0]*1000," mJy/beam  @: ",imstat0['maxpos']

        fno = self.bdp_out[0].filename 
        if self.do_pickle:
            self.pdump()
        if self.do_plot:
            xlabel = 'Frequency (Ghz)'
            ylabel = 'log(Peak,Noise[mJy/beam])'
            if False:
                # signal is green, noise is blue
                ydata = [np.log(signal),np.log(noise)]
            else:
                # also add the plot (ratio is now red)
                ratio = np.log(noise)-np.log(signal)
                ydata = [np.log(signal),np.log(noise),ratio]
            a1.plotter(freq,ydata,'CubeStats',      fno+'.1.png',xlab=xlabel,ylab=ylabel)
            a1.histogram(ydata,   'CubeStats-S,N,R',fno+'.2.png')
            a1.histogram([ratio], 'CubeStats-R',    fno+'.3.png',range=[0.3,0.5])
            
