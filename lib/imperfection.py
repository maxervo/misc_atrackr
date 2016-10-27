from config.imports import *
from config.param import *
from vendor.detect_peaks import detect_peaks

vexp = np.vectorize(cmath.exp)

# Preamble pattern
def sp(t):
    if t<=0.5*(10**(-6)):
        return 1
    elif t<1*(10**(-6)):
        return 0
    elif t<=1.5*(10**(-6)):
        return 1
    elif t<3.5*(10**(-6)):
        return 0
    elif t<=4*(10**(-6)):
        return 1
    elif t<4.5*(10**(-6)):
        return 0
    elif t<=5*(10**(-6)):
        return 1
    else:
        return 0

vsp = np.vectorize(sp)
preamble = vsp( np.linspace(0, Tp, num=Fpe) )
preamble_rev = preamble[::-1]    #reversed

# Add preamble to frame
def pre(sl):
    sl_pre = np.lib.pad(sl, (Fpe,0), 'edge')
    sl_pre[0:Fpe] = preamble

    return sl_pre

# Add imperfections
def transf(sl, delay_time_npts, delay_freq_pts):
    # Delay time
    sl_imp = np.lib.pad(sl, (delay_time_npts,0), 'constant', constant_values=(0))    # ok model delay time?

    # Delay freq
    exp_term = 1 #vexp(-1j*2*math.pi*delay_freq_pts*np.arange(len(sl_imp)) )
    sl_imp = sl_imp*exp_term

    return sl_imp

# Syncing to remove imperfections
delay_conv = 8*(10**(-6))
delay_conv_pts = int(round((Fpe * delay_conv)/Tp))-1
rect = np.ones(Fpe)

def sync_time(yl):
    #DEBUG
    #num = np.convolve(vl, preamble)   # OK because : flip preamble(-t), symmetry but induce a delay of convolution 5 microseconds
    #denum = no need because we are only looking for maximum of correlation, no need normalization
    #num = num[delay_conv_pts:]
    #num = np.correlate(vl, preamble, 'full')
    #num = num[num.size/2:]  # because negative side counted

    num = np.convolve(yl, preamble_rev, 'full')     #attention : delay_conv
    denum = np.convolve(np.power(yl,2), rect, 'full')   #attention : same delay_conv #indeed, sum is equivalent to convolution with a rectangle -> speed improvement
    ratio = np.divide(num, denum)   #Others factors in formula not necessary, we only observe the trend
    similarity = ratio[delay_conv_pts:len(ratio)-delay_conv_pts] #here take into account beginning delay and end as well (error fix)

    '''
    plt.plot(np.arange(len(similarity)), similarity)
    plt.show()'''

    sync_index = detect_peaks(similarity, show=True, mpd=Ns*Fse)   # for only one : sync_index = first np.argmax(similarity)

    return sync_index
