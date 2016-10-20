from config.imports import *
from config.param import *

from lib import misc

class Reg:
    address = 0
    formatdf = 0
    typeftc = 0
    name = ''
    altitude = 0
    #timeFlag not considered
    cprFlag = 0
    latitude = 0
    longitude = 0
    path = []   # do

def get_oaci(B):    # ID string used to uniquely identify planes
    return str(misc.npToDec(B[8:32]))

def bit2reg(B, reg): # B on 112 bits, excluding preamble, DF=17 normally

    # Control fields
    target_formatdf = misc.npToDec(B[0:5])
    target_address = misc.npToDec(B[8:32])
    current_typeftc = misc.npToDec(B[32:37])

    # Control check
    if reg.address != 0 and reg.address != target_address:
        print('Error reg update on wrong plane')
        raise Exception('wrong_plane')
    elif target_formatdf != DF_ADSB:
        print('Error DF not ADSB')
        raise Exception('wrong_df')

    reg.formatdf = target_formatdf
    reg.address = target_address

    # ID msg
    if current_typeftc in range(0,5):
        name_construct = ''
        for i in range(8):  # ID on 8 characters
            name_construct += map_name( B[40+i*6:46+i*6] )
        reg.name = name_construct

    # Airborne msg
    elif current_typeftc in range(9, 23):
        reg.cprFlag = B[53]
        reg.altitude = Calc.alt(B[40:51])
        reg.latitude = Calc.lat(B[54:70], reg.cprFlag)
        reg.longitude = Calc.long(B[71:87], reg.cprFlag, reg.latitude)

    # Surface msg
    ''' No need
    elif current_typeftc in range(5, 9):
        pass
    '''

    # Update FTC
    reg.typeftc = current_typeftc    # always updated to the latest detected

    # Path
    reg.path += [ [reg.longitude, reg.latitude, reg.altitude] ]     # maybe better to use np.array for memory, but slow for concatenating

def validate_crc(B):
    # Problem CRC : DEBUG
    crc24_func = crcmod.mkCrcFun(0x1FFF409, initCrc=0, rev=False)
    #print('msg', misc.npToStr(B[0:88]))
    #print('real crc is', crc24_func(bytes(misc.npToStr(B[0:88]), encoding="UTF-8")))
    #print('crc extracted is', misc.npToDec(B[88:112]) )

    crc_calc = crc24_func(bytes(misc.npToStr(B[0:88]), encoding="UTF-8"))
    crc_extrac = misc.npToDec( B[88:112] )

    #return (crc_cal == crc_extrac)
    return True


def map_name(code):
    if misc.npToDec(code) == 32:    # SP
        return 'SP'
    elif misc.npToDec(code[0:2]) == 3:    # Number: 0-9, OK ASCII
        return chr(misc.npToDec(code))
    else:                                   # Letter: A-Z, Need ASCII shift
        return chr(ord('A') + misc.npToDec(code) - 1)

class Calc:
    def alt(B):
        # Verify if definition of b8 deleted correct TODO
        return 25*misc.npToDec(np.delete(B, 7)) - 1000     # in feet

    def lat(B, cprFlag):
        Dlati = 360/(4*NZ - cprFlag)
        lat_tmp = misc.npToDec(B)/(2**len(B))
        j=math.floor(LAT_REF/Dlati) + math.floor( (1/2) + (misc.MOD(LAT_REF, Dlati)/Dlati) - lat_tmp )
        return Dlati*(j+lat_tmp)

    def long(B, cprFlag, lat):
        #Dloni  : maybe later tabulate Nl TODO
        denum = misc.Nl(lat) - cprFlag
        if denum > 0:
            Dloni = 360/denum
        elif denum == 0:
            Dloni = 360
        else:
            print('Error negative denum, Nl value must be wrong')
            raise Exception('wrong_denum')

        #m
        long_tmp = misc.npToDec(B)/(2**len(B))
        m = math.floor(LONG_REF/Dloni)+math.floor( (1/2) + (misc.MOD(LONG_REF, Dloni)/Dloni) - long_tmp )

        return Dloni*(m+long_tmp)
