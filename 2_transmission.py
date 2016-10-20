################################################
# Imports
################################################
from config.imports import *
from config.param import *
from lib import ppm, filters

################################################
# Processing
################################################

# Input
B = np.random.randint(0, high=2, size=Ns)
print(B)

time_axis_mod = np.linspace(0, Ts*len(B), num=Fse*len(B))
sl = ppm.modulate(B)

# Noise
mu, sigma_2 = 0, 0.9 # example sigma
nl = 0 #np.random.normal(mu, sigma_2, len(sl))

# Filters, blocks
block_abs = filters.vblock_abs
time_axis_ga = np.linspace(0, Ts, num=Fse) # block on Ts here
ga = filters.vga(time_axis_ga)

# Process
yl = sl + nl
rl = np.convolve(block_abs(yl), ga)    # ATTENTION : delay because of p(t) : 5 microseconds
delay = int(round((Fse * filters.getDelay() ) / Ts))-1    # delay in number of points, ATTENTION -1

# Sampling
rln = rl[delay:len(rl):Fse]       # sampling step

# Decision
B_recep = ppm.decide(rln)
print(B_recep)
print("Percentage of error : ", np.mean(B != B_recep)*100, "%")

################################################
# Observations
################################################

# rl
plt.plot(time_axis_mod, rl[delay:len(rl)])
plt.show()

# rln
plt.plot(Ts*np.arange(len(rln)), rln, 'bo')
plt.show()
