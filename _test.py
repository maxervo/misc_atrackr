################################################
# Imports
################################################
from config.imports import *
from config.param import *
from lib import frame, misc
from vendor import junzis_crc

#from pymatbridge import Matlab
#mlab = Matlab('/Applications/MATLAB_R2011a.app/bin/matlab')
#mlab.start()

#crc24_func = crcmod.mkCrcFun(0x1FFF409, initCrc=0, rev=True, xorOut=0)

B = np.array([1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 1, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1])

#data = B[0:88]
crc_extract = misc.npToStr(B[88:112])

#crc_calc = crc24_func(bytes(misc.npToStr(B), encoding="UTF-8"))
crc_calc = junzis_crc.calc(misc.npToStr(B), encode=True)

print(crc_calc == crc_extract)
print("crc calc", crc_calc)
print("crc extract", crc_extract)
