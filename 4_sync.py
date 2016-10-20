################################################
# Imports
################################################
from config.imports import *
from config.param import *
from lib import ppm, filters, imperfection, misc

################################################
# Processing
################################################

# Reference
SNR_db = np.arange(Nteb); SNR = 10**(SNR_db/10)
TEB = np.zeros(Nteb)

# Filter: g
time_axis_g = np.linspace(0, Ts, num=Fse) # block on Ts here
g = filters.vg(time_axis_g)
Eg = np.sum(g**2)

# Block: abs
block_abs = filters.vblock_abs

# Filter: ga
time_axis_ga = np.linspace(0, Ts, num=Fse) # block on Ts here
ga = filters.vga(time_axis_ga)

# Constructing TEB
for i in range(Nteb):
    nb_error = 0
    count = 0
    while(nb_error < SIG_NB_ERROR and count < MAX_COUNT):
        B = np.random.randint(0, high=2, size=Ns)
        A = ppm.mapping(B)  # Tmp
        sl = ppm.modulate(B)
        sl_pre = imperfection.pre(sl)

        # Delays
        delay_conv = int(round((Fse * filters.getDelay() ) / Ts))-1    # delay from convolution in number of points, ATTENTION -1
        delay_time = (Te/100) + np.random.rand()*(100-1)*Te; delay_time_npts = int(round((Fse*delay_time/Ts)))    # -1 or not?, to exclude 0
        delay_freq = np.random.choice([-1, 1])*np.random.randint(1, 1*10**3); delay_freq_pts = int(round(Fse*1/(delay_freq*Ts))) # to exclude 0

        # Imperfection
        sl_imp = imperfection.transf(sl_pre, delay_time_npts, delay_freq_pts)    # with error sync

        # Noise
        mu = 0
        sigma_2 = (np.var(A)*Eg/2)*( (SNR[i])**(-1) ) # formula adapt
        nl = np.random.normal(mu, sigma_2, len(sl_imp)) # Ok to take on all sl_imp? or need to adapt regarding delay, formula...etc?

        # Process
        yl = sl_imp + nl
        vl = block_abs(yl)

        # Syncing
        sync_time = imperfection.sync_time(yl)[0]
        index_frame = sync_time + Fpe
        print('Time delay is ', delay_time_npts)
        print('Syncing: frame beginning is ', sync_time)

        vl_extracted = vl[index_frame:]       # frequency sync not necessary, abs(), the leftover term considered as noise
        rl = np.convolve(vl_extracted, ga)    # ATTENTION : delay because of p(t) : 5 microseconds

        # Sampling
        rln = rl[delay_conv:len(rl):Fse]       # sampling step, sync time

        # Decision
        B_recep = ppm.decide(rln)   # decide

        # Results
        nb_error = nb_error + np.sum(B!=B_recep)
        count=count+1

    TEB[i]=nb_error/(len(B)*count)

Pb=(1/2)*special.erfc(np.sqrt(SNR))
print(TEB)
print(SNR)

################################################
# Observations
################################################

# simulation
plt.semilogy(SNR_db, TEB)

# show
plt.show()
