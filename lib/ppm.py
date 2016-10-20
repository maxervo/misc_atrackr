from config.imports import *
from config.param import *

# Symbol mapping
def mapping(B):
    A = np.zeros(len(B))
    for i in range(len(B)):
        if B[i]==0:
            A[i] = 1
        else:
            A[i] = -1
    return A

# PPM impulsions
def p0(t):
    if t<=0.5*10**(-6): # in seconds
        return 0
    else:
        return 1

def p1(t):
    return -p0(t)+1 # Complementary

# Vectorize functions
vp0 = np.vectorize(p0)
vp1 = np.vectorize(p1)

time_symbol = np.linspace(0, Ts, num=Fse)
symb0 = vp0(time_symbol)
symb1 = vp1(time_symbol)
# Modulation
def modulate(B):
    # Building each symbol
    result = np.zeros(len(B)*Fse) # using np.arrays() less memory than python lists (but the latter is faster for concatenating)
    for i in range(len(B)):
        if B[i]==0:                 # forced to use index, instead of collection for in because of array nature instead of lists
            result[i*Fse:(i+1)*Fse] = symb0
        else:
            result[i*Fse:(i+1)*Fse] = symb1

    return result

# Decision
def decide(rln):
    B_recep = np.zeros(len(rln))
    for i in range(len(rln)):
        if rln[i]>0:
            B_recep[i] = 0
        else:
            B_recep[i] = 1
    return B_recep
