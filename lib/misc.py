from config.imports import *
from config.param import *

qfunc = lambda x: 0.5-0.5*special.erf(x/np.sqrt(2))

def npToStr(B):
    result_str = ''
    for x in B:
        result_str += str(x)

    return result_str

def npToDec(B):
    return int(npToStr(B), 2)
    '''
    result_str = ''
    for x in B:
        result_str += str(x)

    return int(result_str,2)
    '''

def MOD(x,y):
    return x-y*math.floor(x/y)

def Nl(x):
    if x==0:
        return 59
    elif x==87:
        return 2
    elif abs(x)>87:
        return 1
    else:
        return math.floor( 2*math.pi * (math.acos( 1 - (1 - math.cos(math.pi/(2*NZ)))/(math.cos(math.pi*abs(x)/180)**2) ))**(-1) )
