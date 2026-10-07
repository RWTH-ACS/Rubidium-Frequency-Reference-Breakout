import rubidium
import time
import RsInstrument as rsi
from datetime import datetime
from temperusb import TemperHandler
#rm = pyvisa.ResourceManager()
#inst = rm.open_resource('TCPIP::number42.acs-lab.eonerc.rwth-aachen.de::INSTR')
#print(inst.query("*IDN?"))
now = datetime.now()

fh = open("data/" + now.strftime("%Y-%m-%d_%H_%M_%S") + ".csv", "a")


step = 6.8126e-6
i = 0
class PI():
    #halbiert um 08:03 5.12.25 i:1e-8, p:-5e-5
    I = -0.5e-8
    P = -2.5e-5
    def __init__(self, x):
        self.i = x
        self.p = 0
    def update(self, error):
        if error >= 2.5:
            error = error - 2.5
        elif error <= -2.5:
            error = error + 2.5
        else:
            error = 0
        self.i += error * self.I
        self.p = error * self.P
        return self.i + self.p

th = TemperHandler()
devs = th.get_devices()
sensors = range(devs[0].get_sensor_count())


mxo = rsi.RsInstrument('TCPIP::number42.acs-lab.eonerc.rwth-aachen.de::hislip0')
mxo.write('SYSTem:DISPlay:UPDate ON')
currentValue = rubidium.value_to_float(rubidium.read_current_value())
#rubidium.write_value_to_eeprom(rubidium.read_current_value())
pi = PI(currentValue)
last_setpoint = pi.i
while True:
    phase = mxo.query_float('MEASurement2:RESult:ACTual?')
    ref_phasej3 = mxo.query_float('MEASurement1:RESult:ACTual?')
    #ref_phasej4 = mxo.query_float('MEASurement3:RESult:ACTual?')
    ref_phasej4 = 0
    setpoint = pi.update(phase)
    value = rubidium.value_to_float(rubidium.float_to_value(setpoint))
    print(f"phase:{phase}\toffset:{value}\tp:{pi.p}\ti:{pi.i},{rubidium.byte_to_hexstring(setpoint)}\tTemp_Room:{devs[0].get_temperatures(sensors=sensors)[0]['temperature_c']}\tTemp_Device:{devs[1].get_temperatures(sensors=sensors)[0]['temperature_c']}\tRef_PhaseJ3:{ref_phasej3}\tRef_PhaseJ4:{ref_phasej4}")
    fh.write(f"{time.time()},{phase},{value},{pi.p},{pi.i},{rubidium.byte_to_hexstring(setpoint)},{devs[0].get_temperatures(sensors=sensors)[0]['temperature_c']},{devs[1].get_temperatures(sensors=sensors)[0]['temperature_c']},{ref_phasej3},{ref_phasej4}\n")
    fh.flush()
    if abs(setpoint - last_setpoint) > step:
        rubidium.write_value(rubidium.float_to_value(setpoint))
        last_setpoint = setpoint
        print("New Setpoint send")
    time.sleep(1)





print(f'Device IDN: {mxo.idn_string}')
#

#print(currentValue)




#value = rubidium.value_to_float(rubidium.float_to_value(new_value))

#rubidium.write_value(rubidium.float_to_value(value))
