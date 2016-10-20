################################################
# Imports
################################################
from config.imports import *
from config.param import *
from lib import frame, misc

################################################
# Processing
################################################

frames = io.loadmat('data/frames_rtajan.mat')['trames_20141120']

reg = frame.Reg()

# Going through frames sample
for i in range(len(frames[0])):
    B = frames[:,i]    #column 0 : first frame among the 21

    if(frame.validate_crc(B)):
        frame.bit2reg(B,reg)   # operates by reference : reg is updated
    else:
        print('crc not valid')

    # DEBUG msg
    print("FRAME", i)
    print(reg.address)
    print(reg.formatdf)
    print(reg.typeftc)
    print(reg.name)
    print(reg.altitude)
    print(reg.cprFlag)
    print(reg.latitude)
    print(reg.longitude)
    print(reg.path);
    print("END OF FRAME")


# Saving .mat for MATLAB, plot_google_map
io.savemat('data/5_register.mat', {'register': reg});

print(io.loadmat('data/5_register.mat')['register'])

################################################
# Observations
################################################
