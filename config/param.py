# Default constants
DF_ADSB = 17
LAT_REF = 44.807047    # TODO put reference values
LONG_REF = -0.605526
NZ=15

# Default variables
fe=20*10**6; Te=1/fe
Ds=1*10**6; Ts=1/Ds
Fse=int(round(Ts/Te))
Ns=112 # Number of points of the signal : 1000, 112
Nfft=512 # Number of points of FFT

# Default TEB parameters
SIG_NB_ERROR = 100
MAX_COUNT = 500
Nteb = 11   # OK step of 1 db

# Default sync parameters
Tp = 8*(10**(-6))
Fpe = int(round(Tp/Te))

# Init operators to modify default config
def init_ref(lat_ref, long_ref):
    LAT_REF = lat_ref
    LONG_REF = long_ref

def init_fe(in_fe):    # better : do lamda functions for variable recalculations
    fe=in_fe; Te=1/fe
    Fse=int(round(Ts/Te))
    Fpe = int(round(Tp/Te))
