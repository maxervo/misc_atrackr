from config.imports import *
from config.param import *

''' TRASH
# Biphase wave form
def p(t):                 # ATTENTION : delay caused by shifting the function of 5 microseconds to the right
    if t<0.5*10**(-6):
        return 0
    elif t<1*10**(-6): # in seconds
        return -0.5
    elif t<1.5*10**(-6):
        return 0.5
    else:
        return 0

vp = np.vectorize(p)
'''

# Filters, blocks
def g(t):
    if t<0.5*10**(-6):
        return -0.5
    elif t<=1*10**(-6): # in seconds
        return 0.5
    else:
        return 0

def block_abs(t):
    return abs(t)**2

def ga(t):
    if t<0.5*10**(-6):
        return 0.5
    elif t<=1*10**(-6): # in seconds
        return -0.5
    else:
        return 0

# Vectorize
vg = np.vectorize(g)
vblock_abs = np.vectorize(block_abs)
vga = np.vectorize(ga)

# Accessors
def getDelay():           # delay defined by shifting in p(t), in microseconds
    return 1*10**(-6)
