from rubidium import RUBI
import time
import RsInstrument as rsi
from datetime import datetime
import logging, coloredlogs
import tyro
import os
from classes.PI import PI

logger = logging.getLogger(__name__)

####
# pps_sync.py --name rubi0 --serial_port /dev/ttyUSB0 --scope TCPIP::number42.acs-lab.eonerc.rwth-aachen.de::hislip0 --measurement MEASurement1:RESult:ACTual? --p 5e6 --i 1e-5 --log_level DEBUG

####
def main(
        name : str,
        serial_port: str,
        scope: str,
        measurement: str,
        p: float = 1.0,
        i: str = 1.0,
        log_level: str = "DEBUG"
):
    """Isolator test bench CLI

    Args:
        name: Name of the device
        serial_port: Path to serial port
        scope: url of scope
        measurement: the measurement string to receive phase
        p: proportional value
        i: integral value
        log_level: The log level
    """

    coloredlogs.install(level=log_level,
    fmt='%(asctime)s %(levelname)-8s %(name)s[%(process)d] %(message)s',
    field_styles=dict(
        asctime=dict(color='green'),
        hostname=dict(color='magenta'),
        levelname=dict(color='white', bold=True),
        programname=dict(color='cyan'),
        name=dict(color='blue')))
    logger.info("Isolator test bench started.")


    step = 6.8126e-6

    if not os.path.exists(serial_port):
        raise Exception(f"Serial port {serial_port} does not exists")
    rubi = RUBI(serial_port)
    rubi_pi = PI(rubi.current_value_float)

    mxo = rsi.RsInstrument(scope)
    mxo.write('SYSTem:DISPlay:UPDate ON')
    delay = mxo.query_float(measurement)
    logging.info(f"{name} Setpoint:{rubi.current_value_float:.12f};  Delay:{delay:.12f}")

    now = datetime.now()

    fh = open(f"data/{name}pps_" + now.strftime("%Y-%m-%d_%H_%M_%S") + ".csv", "a")
    #fh = open("data/pps_2026-02-24_12_05_28.csv", "a")

    while True:
        delay = mxo.query_float(measurement)
        rubi_pi.update(delay)
        if abs(rubi_pi.now - rubi_pi.last) > step:
            if rubi.write_value(rubi.float_to_value(rubi_pi.now)):
                print("New Setpoint send")
        logging.info(f"{name} Setpoint:{rubi.current_value_float:.12f};  Delay:{delay:.12f}")

        fh.write(f"{time.time()};{rubi.current_value_float:.12f};{delay:.12f}\n")
        fh.flush()
        
        time.sleep(1)

if __name__ == "__main__":
    tyro.cli(main)


# step = 6.8126e-6
# i = 0
# pass

# rubi0 = RUBI("/dev/ttyUSB0", enable_update = False) 
# rubi1 = RUBI("/dev/ttyUSB1", limit = 0.3) 
# rubi2 = RUBI("/dev/ttyUSB3", enable_update = False)

# rubi0_pi = PI(rubi0.current_value_float)
# rubi1_pi = PI(rubi1.current_value_float)
# rubi2_pi = PI(rubi2.current_value_float)

# logging.warning(f"Current Setpoint\t rubi0:{rubi0.current_value_float}\t rubi1:{rubi1.current_value_float}\trubi2:{rubi2.current_value_float}")

# now = datetime.now()

# fh = open("data/pps_" + now.strftime("%Y-%m-%d_%H_%M_%S") + ".csv", "a")
# #fh = open("data/pps_2026-02-24_12_05_28.csv", "a")


# mxo = rsi.RsInstrument('TCPIP::number42.acs-lab.eonerc.rwth-aachen.de::hislip0')
# mxo.write('SYSTem:DISPlay:UPDate ON')

# while True:

#     delay_rubi0 = mxo.query_float('MEASurement1:RESult:ACTual?')
#     delay_rubi1 = mxo.query_float('MEASurement2:RESult:ACTual?')
#     delay_rubi2 = mxo.query_float('MEASurement3:RESult:ACTual?')


#     rubi0_pi.update(delay_rubi0)
#     if abs(rubi0_pi.now - rubi0_pi.last) > step:
#         if rubi0.write_value(rubi0.float_to_value(rubi0_pi.now)):
#             print("New Setpoint send rubi 0")

#     rubi1_pi.update(delay_rubi1)
#     if abs(rubi1_pi.now - rubi0_pi.last) > step:
#         if rubi1.write_value(rubi1.float_to_value(rubi1_pi.now)):
#             print("New Setpoint send rubi 1")

#     rubi2_pi.update(delay_rubi2)
#     if abs(rubi2_pi.now - rubi0_pi.last) > step:
#         if rubi2.write_value(rubi2.float_to_value(rubi2_pi.now)):
#             print("New Setpoint send rubi 2")

#     print(f"rubi0_setp:{rubi0.current_value_float:.12f};  rubi0_delay:{delay_rubi0:.12f}\trubi1_setp:{rubi1.current_value_float:.12f};  rubi1_delay:{delay_rubi1:.12f}\trubi2_setp: {rubi2.current_value_float:.12f};  rubi2_delay:{delay_rubi2:.12f}")
#     #print(f"\t\t")
    
    
#     fh.write(f"{time.time()};{rubi0.current_value_float:.12f};{delay_rubi0:.12f};{rubi1.current_value_float:.12f};{delay_rubi1:.12f};{rubi2.current_value_float:.12f};{delay_rubi2:.12f}\n")
#     fh.flush()
#     #f"{time.time()},{phase},{value},{pi.p},{pi.i},{rubidium.byte_to_hexstring(setpoint)},{devs[0].get_temperatures(sensors=sensors)[0]['temperature_c']},{devs[1].get_temperatures(sensors=sensors)[0]['temperature_c']},{ref_phasej3},{ref_phasej4}\n")
 

#     time.sleep(1)
