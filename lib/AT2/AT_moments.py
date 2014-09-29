import sys, os
import atable, aplot
import numpy as np
import admit2 as admit
import casa
import taskinit

class AT_moments(admit.AT):
    """
    single = 1  single call to moment, so all files come out the same call, no filename control
             0  call moment for each requested moments. bit slower maybe, but filename control
    """
    name = 'MOMENTS'
    version = '1.0'
    keys = ['moments','nsigma','cutoff','single']
    def __init__(self,name=None):
        if name != None: self.name = name
        admit.AT.__init__(self,self.name)
    def check(self):
        n=0
    def run(self):
        if not admit.AT.run(self):
            return False
        # specialized work can commence here
        if self.has('moments'):
            # convert string to int's
            moments = []
            for m in self.get('moments').split(','):
                moments.append(int(m))
        else:
            moments = [0]
        #
        cutoff = self.getf('cutoff',0.01)
        single = self.getb('single',0)
        dmax = 999999.9
        fni = self.bdp_in[0].filename
        virtual = self.bdp_in[0].virtual
        if virtual:
            fni = self.bdp_in[0].virtual
            ch0 = self.bdp_in[0].chan0
            ch1 = self.bdp_in[0].chan1
            virtual = 1

        n2 = len(moments)
        for i in range(n2):
            if virtual:
                fno = self.bdp_in[0].linecube
            else:
                fno = fni + '.mom%d' % moments[i]
            self.bdp_out.append(admit.BDP_image(fno))
        #  includepix=
        #  casa.immoments() doesn't have the overwrite option
        if not virtual:
            taskinit.ia.open(fni)

        if single == 0:
            # loop over 3 moments, this is where you have control over the output file names
            for (m,b) in zip(moments,self.bdp_out):
                fno = b.filename
                if virtual:
                    # virtual cube 
                    chans = '%d~%d' % (ch0,ch1)
                    print "virtual cube: ch0,ch1=",ch0,ch1,':',chans
                    os.system('rm -rf %s' % fno)
                    casa.immoments(fni,m,outfile=fno,includepix=[cutoff,dmax],chans=chans)
                else:
                    # straight cube (ia.moments does not have the chans= option)
                    taskinit.ia.moments(m,outfile=fno,includepix=[cutoff,dmax],overwrite=True)
                if m==0:
                    fno0 = fno
                    b0 = b
                    # add the flux/sum to the header
                    # 'sum' is the sum of the pixels, not beam corrected
                    if False:
                        # @todo  CASA BUG ?
                        # something not working, if we don't do an extra "dummy" imstat on 'fni', the 'fno' doesn't work":
                        # SEVERE	imstat::ImageAnalysis::open	Image linecube.U-112.357.mom0 cannot be opened; its type is unknown
                        h = casa.imstat(fni)
                        h = casa.imstat(fno)
                        b.flux = h['sum']
                        print "TOTAL SUM in %s : %g" % (fno,b.flux)
        else:
            # here one call to moment creation, all moments are now created behind the scenes with their own names
            fno = self.bdp_out[0].filename
            print 'Single call to (im)moments: Using base filename ',fno
            if virtual:
                # virtual cube 
                chans = '%d~%d' % (ch0,ch1)
                print "virtual cube: ch0,ch1=",ch0,ch1,':',chans,moments,fni
                os.system('rm -rf %s' % fno)
                casa.immoments(fni,moments,outfile=fno,includepix=[cutoff,dmax],chans=chans)
            else:
                # straight
                taskinit.ia.moments(moments,outfile=fno,includepix=[cutoff,dmax],overwrite=True)

        if not virtual:
            # grab a quick cubestats like thing 
            hlc = taskinit.ia.statistics(axes=[0,1],robust=True)
            sigma = hlc['medabsdevmed']
            xlab = 'rms'
            title = 'linecube stats'
            aplot.APlot().histogram([sigma],title,fno+'stat1',xlab=xlab)
            taskinit.ia.close()
        else:
            #
            print 'No linecube stats available in virtual mode (yet)'
        #
        if self.do_pickle:
            self.pdump()
        if self.do_plot:
            # histograms of the mom0,1,2 would also be useful here
            # 
            print "AT_moments: no plots"
