import sys, os
import atable, aplot
import numpy as np
import casa
import admit2 as admit

class AT_cubespectrum(admit.AT):
    """
    bdp_in[0]     cube
    bdp_in[1]     (optional) cubestats

    pos=x,y       ignored if a CubeStats is given as second BDP, the peak in the cube is used for pos=
    """
    name = 'CUBESPECTRUM'
    version = '1.0'
    keys = ['pos','freq']
    def __init__(self,name=None):
        if name != None: self.name = name
        admit.AT.__init__(self,self.name)
    def check(self):
        self.bdp_out = [  admit.BDP_cubespectrum(self.name) ]
    def run(self):
        if not admit.AT.run(self):
            return False
        # specialized work can commence here
        fni = self.bdp_in[0].filename
        fno = self.bdp_out[0].filename
        use_freq = self.getb('freq',1)
        
        if not use_freq:
            restfreq = self.bdp_in[0].restfreq


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
            if box == None:
                vals = casa.imval(fni)
                pp = "%d,%d" % (vals['blc'][0],vals['blc'][1])
            else:
                vals = casa.imval(fni,box=box)
            pp = "Pos(%s)" % pp
            yrange = None
        elif len(self.bdp_in) == 2:
            # two BDP's, 2nd one is a CubeStats where we take the peak location
            b = self.bdp_in[1]
            pp = "%d,%d" % (b.maxpos[0],b.maxpos[1])
            box = '%s,%s' %  (pp,pp)
            vals = casa.imval(fni,box=box)
            pp = "Peak(%s)" % pp
            nsigma = 10.0
            yrange = [-nsigma*self.bdp_in[1].sigma, nsigma*self.bdp_in[1].sigma]
        else:
            print "no case implemented for > 2 BDP's"
            return
        print 'IMVALS:',vals['blc'],vals['trc']
        #print vals.keys()
        posx = vals['blc'][0]   # only 1 point, trc should be same
        posy = vals['blc'][1]   #
        data = vals['data']     # spectrum in units of vals['unit']
        if True:
            # alternate mathod to grab the freq
            fr = vals['coords'].transpose()[2]/1e9
            print "TESTING:  fr2: ",fr.min(),fr.max()
        else:
            # grab the X coords again
            h = casa.imhead(fni,mode='list')
            n = h['shape'][2]
            p = h['crpix3']
            d = h['cdelt3']
            v = h['crval3']
            ch = np.arange(n) + 1
            fr = ((ch-p-1)*d + v)/1e9
        if not use_freq:
            vel = (1-fr/restfreq)*300000.0

        a1 = atable.ATable([fr,data],['frequency','data'])
        if self.do_pickle:
            a1.pdump('cubespectrum.atable')
        self.bdp_out[0].table = a1
        self.bdp_out[0].pos = [posx, posy]
        data   = data * 1000              # plotting in mJy/beam now
        print "Freq range : %g %g GHz" % (fr.min(), fr.max())
        print "Data range : %g %g mJy/beam" % (data.min(), data.max())
        if not use_freq:
            print "Vel range  : %g %g GHz" % (vel.min(), vel.max())
            print "RestFreq: ",restfreq
        if self.do_pickle:
            self.pdump()
        if self.do_plot:
            title = 'CubeSpectrum(%s)' % pp
            ylabel = 'Flux (mJy/beam)'
            if use_freq:
                xlabel = 'Frequency (Ghz)'
                aplot.APlot().plotter(fr,[data],title,fno+'.1',xlab=xlabel,ylab=ylabel)
                if yrange != None:
                    aplot.APlot().plotter(fr,[data],title,fno+'.2',xlab=xlabel,ylab=ylabel,yrange=yrange)
            else:
                xlabel = 'Velocity (km/s'
                aplot.APlot().plotter(vel,[data],title,fno+'.1',xlab=xlabel,ylab=ylabel)
                if yrange != None:
                    aplot.APlot().plotter(vel,[data],title,fno+'.2',xlab=xlabel,ylab=ylabel,yrange=yrange)
