import serial
import struct

class RUBI():
#/dev/ttyUSB0 rubi1
#/dev/ttyUSB2 rubi0
    startup_value = None
    current_value = None
    current_value_float  = None
    port = None


    def __init__(self, port, limit = 0.5, enable_update = True, baudrate = 9600):
        self.port = port
        self.limit = limit
        self.enable_update = enable_update
        if self.port is None:
            self.startup_value = 0
            self.current_value = 0
        else:
            self.ser = serial.Serial(port, baudrate)
            self.startup_value = self.read_current_value()
            self.current_value = self.startup_value

    def read_current_value(self) -> bytes:
        if not self.enable_update:
            self.current_value_float = 0
            return 0
        self.ser.write(b'\x2d\x04\x00\x29')
        res = self.ser.read(9)
        self.current_value_float = self.value_to_float(res[4:8])
        return res[4:8]
    
    def read_current_value_float(self) -> float:
        return self.value_to_float(self.read_current_value())


    def write_value(self, v: bytes):
        if not self.enable_update:
            return 0
        if self.current_value == v:
            return 0
        self.current_value = v
        self.current_value_float = self.value_to_float(v)
        s = b'\x2e\x09\x00\x27' + v + (v[0] ^ v[1] ^ v[2] ^ v[3]).to_bytes(1)
        print(''.join(format(x, '02x') for x in s))
        self.ser.write(s)
        return 1

    def byte_to_hexstring(self, v: float):
        return ''.join(format(x, '02x') for x in self.float_to_value(v))


    def write_value_to_eeprom(self,v: int):
        if not self.enable_update:
            return
        s = b'\x2c\x09\x00\x25' + v + (v[0] ^ v[1] ^ v[2] ^ v[3]).to_bytes(1)
        self.ser.write(s)

    def try_setpoint(self, v: float) -> bool:
        if v < self.limit and v > -1 * self.limit:
            return True
        return False
        

    def float_to_value(self, v: float) -> bytes:
        if v > self.limit:
            v = self.limit
        if v < -1 * self.limit:
            v = -1 * self.limit
        v = round(v / 6.8126e-6)
        return struct.pack(">i", int(v))

    def value_to_float(self, v: bytes) -> float:
        i = float(struct.unpack(">i",v)[0])
        return i * 6.8126e-6
