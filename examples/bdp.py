"""
ADMIT pipeline
Basic Data Product (BDP) class

"""

from telescope import TelescopeType as Type

####### Base BDP class #########
class BDP:

    def __init__(self, telescope, perms):
        self.tele_name = telescope
        self.tele_obj = Type()
        self.tele_obj.setVal(telescope, perms)

    def getTele(self):
        return self.tele_name
 
    def printPerms(self):
        return self.tele_obj.report()
 
    def readXML(self):
        rw = XMLrw()
        print "In readXML of BDP class"
 
    def writeBDP():
        print "In writeBDP, Telescope = %d" % tele_type
 
    def writeBDPZip():
        print "In writeBDPZIP of BDP Telescope = %d" % tele_type

#####################################
class BDPContinuumMap(BDP):
    """ Class for ContinnumMap """
 
    def __init__(self, tel, perms):
        BDP.__init__(self, tel, perms)
 
    def writeBDP():
        print "In writeBDP of BDPContinuumMap"
 
#####################################
class BDPMomentMap(BDP):
    """ Class for MomentMap """
 
    def __init__(self, tel, perms):
        BDP.__init__(self, tel, perms)
 
#####################################
class BDPPeakSpectrum(BDP):
    """ Class for PeakSectrum """

    def __init__(self, tel, perms):
        BDP.__init__(self, tel, perms)
 

#### Test ####
name = "ALMA"
ids = [('project', '2012.1.01234.S'),('sous', 'A000_X01_X00'), ('gous', 'A000_X01_X01'), ('mous', 'A000_X01_Xxx1')]

bdp = BDPPeakSpectrum(name, ids)
 
print "Telescope name:", bdp.getTele()
bdp.printPerms()
