################################################
# Imports
################################################
from config.imports import *
from config.param import *
from lib import ppm, imperfection, filters, frame, misc

################################################
# Processing : PHYSICAL LAYER
################################################

# Init var
init_fe( io.loadmat('data/cplx_sample.mat')['Fe'][0][0] )   # readjust fe for this sample

# Filter: ga
delay_conv = int(round((Fse * filters.getDelay() ) / Ts))-1
time_axis_ga = np.linspace(0, Ts, num=Fse) # block on Ts here
ga = filters.vga(time_axis_ga)

# Frames bank : majorate no columns (better whole array, than merging numpy : arrays slow, and python lists high memory usage)
time_recording = 1 # in seconds
max_columns = math.ceil(time_recording/(Ns*Ts))+1
frames = np.zeros((Ns, max_columns))

# Extracting data
vl = io.loadmat('data/cplx_sample.mat')['abs_cplxBuffer'][0]

# Syncing : finding frames
sync_time = imperfection.sync_time(vl)

# Looping through : processing frames
i=0
while( sync_time[i]+Ns*Fpe < len(vl)):
    index_frame = sync_time[i] + Fpe
    vl_extracted = vl[ index_frame : index_frame + Ns*Fse ]       # Attention notation end-1 implicit, Ns bits in total

    # Process
    rl = np.convolve(vl_extracted, ga)    # ATTENTION : delay because of p(t) : 5 microseconds

    # Sampling
    rln = rl[delay_conv:len(rl):Fse]       # sampling step, sync time

    # Decision
    print(len(rln))
    B_recep = ppm.decide(rln)   # decide

    # Filling the i column with frame
    frames[:,i] = B_recep

    # Adjusting cursor
    i=i+1

# Compact bank (resize to only frames, clean unnecessary columns from majoration) & convert to int
frames = frames[:,0:i].astype(int)

################################################
# Processing : MAC LAYER
################################################

# Dictionnary of registers
dic = {}    # oaci is ID thus can be key of our dictionary
reg = frame.Reg()

# Going through frames sample
for i in range(len(frames[0])):
    B = frames[:,i]    #column 0 : first frame among the 21
    oaci = frame.get_oaci(B)

    if(frame.validate_crc(B)):
        if oaci in dic:
            frame.bit2reg(B,dic[oaci])  # update reg
        else:
            dic[oaci] = frame.Reg()     # add new reg in dictionary
            frame.bit2reg(B,dic[oaci])

    else:
        print('crc not valid')




################################################
# Observations
################################################
