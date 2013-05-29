#
#  astute tools to process lines
#from astropy.io import ascii


def read_cheat_lines(file):
    """ read a cheat lines list  Freq (Ghz) and Name (ascii)
    """
    #data = ascii.read(file)
    #return data
    fp = open(file)
    lines = fp.readlines()
    fp.close()
    f_out=[]
    l_out=[]
    for line in lines:
        if line[0] == '#': continue
        w = line.strip().split()
        f_out.append(float(w[0]))
        l_out.append(w[1])
    return (f_out,l_out)

      

def in_range(val,naxisi,crvali,cdelti,crpixi):
    """very generic in axis range finder
    """
    val0 = (1-crpixi)*cdelti+crvali
    val1 = (naxisi-crpixi)*cdelti+crvali
    if val0<val1:
        if val<val0: return False
        if val>val1: return False
        return True
    if val0>val1:
        if val<val1: return False
        if val>val0: return False
        return True
    # should never come here
    return False

def axis_range(naxisi,crvali,cdelti,crpixi):
    """  
    generic axis range 
    """
    val0 = (1-crpixi)*cdelti+crvali
    val1 = (naxisi-crpixi)*cdelti+crvali
    return [val0,val1]


c_kms = 299792.458

def f_doppler(vlsr, f0):
    """ return sky freq for given VLSR
    @todo   relativistic
    """
    return   (1-vlsr/c_kms)*f0


def f_rest(vlsr, f):
    """ return rest freq for given VLSR
    @todo   relativistic
    """
    return   f/(1-vlsr/c_kms)


def edit_slines_doppler(file,vlsr):
    """ very special edit for vlsr assumption 
    012345678.0.........0.........0.........0.........0.........0
    c-HCC13CH               * Cyclopropenylidene    113.964130 10(4,7)-9(5,4) ....
    """
    fp = open(file)
    lines = fp.readlines()
    fp.close()
    print lines[0]
    print lines[1][48:58]
    print lines[2][48:58]
    print lines[3][48:58]
    # unfinished code

  
