################################################
# Imports
################################################
from config.imports import *
from config.param import *
from lib import ppm

################################################
# Processing
################################################

# Input
B = np.random.randint(0, high=2, size=Ns)
time_axis = np.linspace(0, Ts*len(B), num=Fse*len(B))
B_mod = ppm.modulate(B)

# Truncated
B_trunc = B[:25]
time_axis_trunc = time_axis[:Fse*len(B_trunc)]  # Beware Fse, nb points in symbol
B_trunc_mod = B_mod[:Fse*len(B_trunc)]

# PSD with Welch
f, psd = signal.welch(B_mod, fe, nperseg=256, noverlap=None)        # for no ponderation window : do np.ones...etc TODO, maybe recode algo TODO

################################################
# Observations
################################################

# Modulations truncated
print(B_trunc)
plt.plot(time_axis_trunc, B_trunc_mod)
plt.xlabel('Time (in seconds)')
plt.ylabel('Amplitude (no units)')
plt.show()

# PSD plot
plt.semilogy(f, psd)
plt.show()
