################################################
# Imports
################################################
from config.imports import *
from config.param import *
from lib import ppm, filters, misc

################################################
# Processing
################################################

# Reference
SNR_db = np.arange(Nteb); SNR = 10**(SNR_db/10)
TEB = np.zeros(Nteb)
print(SNR)

# Filter: g
time_axis_g = np.linspace(0, Ts, num=Fse) # block on Ts here
g = filters.vg(time_axis_g)
Eg = np.sum(g**2)

# Block: abs
block_abs = filters.vblock_abs

# Filter: ga
time_axis_ga = np.linspace(0, Ts, num=Fse) # block on Ts here
ga = filters.vga(time_axis_ga)

for i in range(Nteb):
    nb_error = 0
    count = 0
    while(nb_error < SIG_NB_ERROR and count < MAX_COUNT):
        B = np.random.randint(0, high=2, size=Ns)
        A = ppm.mapping(B)  # Tmp
        sl = ppm.modulate(B)

        # Noise
        mu = 0
        sigma_2 = (np.var(A)*Eg/2)*( (SNR[i])**(-1) ) # formula
        nl = np.random.normal(mu, sigma_2, len(sl))

        # Process
        yl = sl + nl
        rl = np.convolve(block_abs(yl), ga)    # ATTENTION : delay because of p(t) : 5 microseconds
        delay = int(round((Fse * filters.getDelay() ) / Ts))-1    # delay in number of points, ATTENTION -1

        # Sampling
        rln = rl[delay:len(rl):Fse]       # sampling step, no sync error

        # Decision
        B_recep = ppm.decide(rln)

        # Results
        nb_error = nb_error + np.sum(B!=B_recep)
        count=count+1
        #print("nb error ", nb_error, " and i=", i, "and sigma_2 ", sigma_2, "and var a ", np.var(A))

    TEB[i]=nb_error/(len(B)*count)

Pb= (1/2)*special.erfc(np.sqrt(SNR)) # regarding expression q.2,3, or misc.qfunc( np.sqrt(2*SNR) )
print(TEB)
print(SNR)

################################################
# Observations
################################################

# theory
plt.semilogy(SNR_db, Pb)

# simulation
plt.semilogy(SNR_db, TEB)

# show
plt.show()
