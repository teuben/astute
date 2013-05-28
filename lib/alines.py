#
#  astute tools to process lines

from astropy.io import ascii


def read_cheat_lines(file):
    """ read a cheat lines list  Freq (Ghz) and Name (ascii)
    """
    data = ascii.read(file)
    return data

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
        
