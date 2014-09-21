import sys, os
import atable, aplot
import numpy as np
import numpy.ma as ma
import casa
import taskinit
import admit1 as admit
import matplotlib.pyplot as plt

def rejecto1(data, f=1.5):
    u = np.mean(data)
    s = np.std(data)
    newdata = [e for e in data if (u - f * s < e < u + f * s)]
    return newdata

def rejecto2(data, f=1.5):
    d = np.abs(data - np.median(data))
    mdev = np.median(d)
    s = d/mdev if mdev else 0.
    return data[s<f]

def mystats(data):
    m1 = data.mean()
    s1 = data.std()
    n1 = len(data)
    d = rejecto2(data)
    m2 = d.mean()
    s2 = d.std()
    n2 = len(d)
    return (n1,m1,s1,n2,m2,s2)

class AT_cubestats(admit.AT):
    name = 'CUBESTATS'
    version = '1.0'
    keys = ['ppp','verbose','cubehist']
    def __init__(self,bdp_in=[],bdp_out=[]):
        admit.AT.__init__(self,self.name,bdp_in,bdp_out)
    def run(self):
        if not admit.AT.run(self):
            return False
        # specialized work can commence here
        #
        verbose      = self.geti('verbose',0)
        use_ppp      = self.getb('ppp',0)
        use_cubehist = self.getb('cubehist',1)
        #
        fin = self.bdp_in[0].filename
        print "casa::imhead(%s)" % fin
        h = casa.imhead(fin,mode='list')
        n = h['shape'][2]
        p = h['crpix3']
        d = h['cdelt3']
        v = h['crval3']
        ch = np.arange(n) + 1        # 1-based channels
        fr = ((ch-p-1)*d + v)/1e9    # in GHz !!
        #
        print "casa::imstat(%s)" % fin
        mask = '"%s" != 0.0' % fin
        imstat0 = casa.imstat(fin,           logfile='imstat0.logfile',append=False)
        if verbose: print imstat0
        imstat1 = casa.imstat(fin,axes=[0,1],logfile='imstat1.logfile',append=False)
        if use_ppp:
            # until imstat  can do this per plane, we need to loop over the planes
            # so it's expensive.
            print "Creating PeakPosPoint (expensive method)"
            # n= number of channels
            xpos = np.arange(n)
            ypos = np.arange(n)
            for i in range(n):
                s = casa.imstat(fin,chans='%d'%i)
                xpos[i] = s['maxpos'][0]
                ypos[i] = s['maxpos'][1]
        #
        if use_cubehist:
            taskinit.tb.open(fin)
            data = taskinit.tb.getcol('map')   # get the N-Dim view
            shape = data.shape
            taskinit.tb.close()
            d1 = data.ravel()                  # get a 1D view
            d1 = d1*1000.0                     # get it in mJy/beam
        #
        c1 = 'max'
        c2 = 'sigma'
        c3 = 'medabsdevmed'
        c4 = 'mean'
        c5 = 'min'
        #
        print "Cube Stats:"
        print "  number of points: %d" % imstat0['npts']
        print "  mean, sigma: %g %g  (%g) mJy/beam" % (imstat0[c4][0]*1000,imstat0[c3][0]*1000,imstat0[c2][0]*1000)
        print "  min: ", imstat0[c5][0]*1000," mJy/beam  @: ",imstat0['minpos']
        print "  max: ", imstat0[c1][0]*1000," mJy/beam  @: ",imstat0['maxpos']
        nsigma = 5.0
        d2min = (imstat0[c4][0] - nsigma * imstat0[c2][0])*1000
        d2max = (imstat0[c4][0] + nsigma * imstat0[c2][0])*1000
  
        print "Plane Stats: N    mean                 std       (all)      N    mean                   std (robust)"
        #                  (246, 0.27362257102568238, 0.74791136119946566, 156, 0.0080285586976625214, 0.016183423031758848)
        print "  mean  :: ",mystats( imstat1[c4]*1000 )
        print "  madm  :: ",mystats( imstat1[c3]*1000 )
        print "  max   :: ",mystats( imstat1[c1]*1000 )
        print "  sigma :: ",mystats( imstat1[c2]*1000 )
        print "  s/n   :: ",mystats( imstat1[c1]/imstat1[c3] )

        col_names = ['channel','frequency','mean',      'sigma',     'max']
        col_data  = [ ch,       fr,         imstat1[c4], imstat1[c3], imstat1[c1]] 
        if use_ppp:
            col_names.append('maxposx')
            col_data.append(xpos)
            col_names.append('maxposy')
            col_data.append(ypos)
        a1 = atable.ATable(col_data, col_names)
        a1.pdump('cubestats.bin')

        self.bdp_out[0].table = a1
        self.bdp_out[0].mean  = imstat0[c4][0]
        self.bdp_out[0].sigma = imstat0[c3][0]
        self.bdp_out[0].max   = imstat0[c1][0]
        self.bdp_out[0].maxpos = [ imstat0['maxpos'][0], imstat0['maxpos'][1], imstat0['maxpos'][2] ]

        freq   = a1.get('frequency')            # in GHz 
        mean   = a1.get('mean')*1000            # in mJy/beam now
        noise  = a1.get('sigma')*1000           # in mJy/beam now
        signal = a1.get('max')*1000             # in mJy/beam now
        s2n    = signal/noise                   # dimensionless
        print "Freq range : %g %g GHz" % (freq.min(), freq.max())
        print "Mean range : %g %g mJy/beam" % (mean.min(), mean.max())
        print "Noise range : %g %g mJy/beam" % (noise.min(), noise.max())
        print "Peak range : %g %g mJy/beam" % (signal.min(), signal.max())
        print "S/N range : %g %g mJy/beam" % (s2n.min(), s2n.max())

        d2min = mean.mean() - nsigma * noise.mean()
        d2max = mean.mean() + nsigma * noise.mean()

        (n1,sn1,sn2,n3,sn3,sn4) = mystats( imstat1[c1]/imstat1[c3] )
        print "SIGNAL CONFIDENCE FACTOR: ",(s2n.max()-sn3)/sn4
        (n1,sn1,sn2,n3,sn3,sn4) = mystats( imstat1[c3] )
        print "SIGNAL/NOISE:             ",(signal.max()/sn3/1000.0)

        
        #print "Cube Stats after pickle:"
        #print "  mean, sigma: %g %g  (%g) mJy/beam" % (imstat0[c4][0]*1000,imstat0[c3][0]*1000,imstat0[c2][0]*1000)
        #print "  max: ", imstat0[c1][0]*1000," mJy/beam  @: ",imstat0['maxpos']

        fno = self.bdp_out[0].filename 
        if self.do_pickle:
            self.pdump()
        if self.do_plot:
            # be careful, arrays not checked for 0
            xlabel = 'Frequency (Ghz)'
            ylabel = 'log(Peak,Noise[mJy/beam])'
            # signal is green, noise is blue
            # also add the plot (ratio is now red)
            ratio = np.log10(signal)-np.log10(noise)
            use_ratio = True
            if use_ratio:
                ydata = [np.log10(signal),np.log10(noise),ratio]
            else:
                ydata = [np.log10(signal),np.log10(noise)]
            title = 'CubeStats-1 %s' % self.bdp_in[0].project
            # a1.plotter(freq,ydata,title, fno+'.1.png',xlab=xlabel,ylab=ylabel,pmode=self.pmode)
            aplot.APlot().plotter(freq,ydata,title, fno+'.1.png',xlab=xlabel,ylab=ylabel)
            if True:
                title = 'CubeStats-2 %s' % self.bdp_in[0].project
                if use_ratio:
                    xlab  = 'log(Peak,Noise,P/N[mJy/beam])'
                else:
                    xlab  = 'log(Peak,Noise[mJy/beam])'
                aplot.APlot().histogram(ydata,title,fno+'.2.png',xlab=xlab)
                title = 'CubeStats-3 %s' % self.bdp_in[0].project
                xlab  = 'log(Peak/Noise[mJy/beam])'
                #a1.histogram([ratio],title,fno+'.3.png',xlab=xlab,pmode=self.pmode)
                aplot.APlot().histogram([ratio],title,fno+'.3.png',xlab=xlab)
            if use_ppp:
                title = 'CubeStats-4'
                xlab = 'Pixel'
                ylab = 'Pixel'
                #aplot.APlot().scatter([xpos],[ypos],title,fno+'.4.png',xlab=xlab,ylab=ylab,pmode=self.pmode)
            if use_cubehist:
                title = 'CubeStats-5 %s' % self.bdp_in[0].project                
                xlab = 'CubeData [mJy/beam])'
                print "Masking outside %g  %g" % (d2min,d2max)
                #   @todo this is no good, masking is not zero
                #d2 = ma.masked_outside(d1,d2min,d2max)
                d2 = d1[d1!=0]
                n1 = len(d1)
                n2 = len(d2)
                fraction = (100.0*n2)/n1
                print "  %d/%d (%g %%) data are non-zero" % (n2,n1,fraction)
                #a1.histogram([d2],title,fno+'.4.png',xlab=xlab,range=[d2min,d2max])
                if True:
                    # robust
                    gmean = mean.mean()
                    gdisp = noise.mean()
                else:
                    # raw cube
                    gmean = imstat0[c4][0]*1000
                    gdisp = imstat0[c2][0]*1000
                aplot.APlot().hisplot(d2,title,fno+'.5.png',xlab=xlab,range=[d2min,d2max],gauss=[gmean,gdisp])
            
