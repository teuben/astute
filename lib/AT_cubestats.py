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
        c1 = 'max'
        c2 = 'sigma'
        c3 = 'medabsdevmed'
        c4 = 'mean'
        c_im = self.bdp_in[0].filename
        #
        print "casa::imstat(%s)" % c_im
        imstat1 = casa.imstat(c_im,axes=[0,1],logfile='imstat1.logfile',append=False)
        imstat0 = casa.imstat(c_im,logfile='imstat0.logfile',append=False)
        #
        print "casa::imhead(%s)" % c_im
        h = casa.imhead(c_im,mode='list')
        n = h['shape'][2]
        p = h['crpix3']
        d = h['cdelt3']
        v = h['crval3']
        ch = np.arange(n) + 1        # 1-based channels
        fr = ((ch-p-1)*d + v)/1e9    # in GHz !!
        #
        print "Cube Stats:"
        print "  mean, sigma: %g %g  (%g) mJy/beam" % (imstat0[c4][0]*1000,imstat0[c3][0]*1000,imstat0[c2][0]*1000)
        print "  max: ", imstat0[c1][0]*1000," mJy/beam  @: ",imstat0['maxpos']

        col_names = ['channel','frequency','mean','sigma','max']
        col_data = [ ch, fr, imstat1[c1], imstat1[c2], imstat1[c3]] 
        a1 = atable.ATable(col_data, col_names)
        a1.pdump('cubestats.bin')

        if use_ppp:
            print "Creating PPP with peakpospoint.bin"
            # n= number of channels
            xpos = np.arange(n)
            ypos = np.arange(n)
            for i in range(n):
                if i%10==0: print i
                s = casa.imstat(c_im,chans='%d'%i)
                xpos[i] = s['maxpos'][0]
                ypos[i] = s['maxpos'][1]
            a2 = atable.ATable([ch,fr,xpos,ypos,imstat[c1]],['channel','frequency','maxposx','maxposy','max'])
            a2.pdump('peakpospoint.bin')
           

        self.bdp_out[0].data['table'] = a1
        self.table = a1
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
        self.bdp_out[0].mean  = imstat0[c4][0]
        self.bdp_out[0].sigma = imstat0[c3][0]
        self.bdp_out[0].max   = imstat0[c1][0]
        self.bdp_out[0].maxpos = [ imstat0['maxpos'][0], imstat0['maxpos'][1], imstat0['maxpos'][2] ]

        filename = self.bdp_out[0].filename 
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
            a1.plotter(freq,ydata,'CubeStats',filename+'.png',xlab=xlabel,ylab=ylabel)

            
