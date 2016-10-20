################################################
# Imports
################################################
from config.imports import *
from config.param import *
from lib import frame, misc

from pymatbridge import Matlab
mlab = Matlab('/Applications/MATLAB_R2011a.app/bin/matlab')
mlab.start()

crc24_func = crcmod.mkCrcFun(0x1FFF409, initCrc=0, rev=False, xorOut=0)

B = np.array([1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1])

data = B[0:88]
crc_extract = misc.npToDec(B[88:112])

crc_calc = crc24_func(bytes(misc.npToStr(data), encoding="UTF-8"))

print("crc calc", crc_calc)
print("crc extract", crc_extract)
