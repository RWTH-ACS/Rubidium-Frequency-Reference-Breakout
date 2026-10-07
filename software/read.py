from rubidium import RUBI
import time
import RsInstrument as rsi
from datetime import datetime
import logging
import tyro


mxo = rsi.RsInstrument('TCPIP::number42.acs-lab.eonerc.rwth-aachen.de::hislip0')
mxo.write('SYSTem:DISPlay:UPDate ON')

while True:

    delay = mxo.query_float('MEASurement2:RESult:ACTual?')



    print(f"delay:{delay:.12f}")

    time.sleep(1)
