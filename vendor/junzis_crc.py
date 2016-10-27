# Copyright (C) 2015 Junzi Sun (TU Delft)

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Modified version for atrackr

"""
Common functions for ADS-B and Mode-S EHS decoder
"""

import math

# the polynominal generattor code for CRC
GENERATOR = "1111111111111010000001001"

def calc(msg, encode=False):
    """Mode-S Cyclic Redundancy Check
    Detect if bit error occurs in the Mode-S message
    Args:
        msg (string): 28 bytes hexadecimal message string
        encode (bool): True to encode the date only and return the checksum
    Returns:
        string: message checksum, or partity bits (encoder)
    """

    msgbin = list(msg)

    if encode:
        msgbin[-24:] = ['0'] * 24

    # loop all bits, except last 24 piraty bits
    for i in range(len(msgbin)-24):
        # if 1, perform modulo 2 multiplication,
        if msgbin[i] == '1':
            for j in range(len(GENERATOR)):
                # modulo 2 multiplication = XOR
                msgbin[i+j] = str((int(msgbin[i+j]) ^ int(GENERATOR[j])))

    # last 24 bits
    reminder = ''.join(msgbin[-24:])
    return reminder
