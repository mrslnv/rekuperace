from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import logging
import struct

class AbstractClient:
    def __init__(self):
        pass

    def getTempExtIn(self) -> float:
        return 0

    def setPower(self,power:int) -> None:
        pass

class VentboxClient(AbstractClient):
    def __init__(self) -> None:
        super().__init__()
        self.client = ModbusClient('192.168.1.92', port=502)
        self.client.connect()
        print("Connected")

    def getTempExtIn(self) -> float:
        reg = self.client.read_input_registers(0, 2)
        s = struct.pack('<HH',reg.registers[0],reg.registers[1])
        return struct.unpack('f',s)[0]

    def setPower(self,power:int) -> None:
        self.power = power


class TestClient(AbstractClient):
    def __init__(self) -> None:
        super().__init__()
        self.i = -1
        for x in range(100):
            self.data[5*x] = 5.1
            self.data[5*x+1] = 5.2
            self.data[5*x+2] = 4.8
            self.data[5*x+3] = 5.1
            self.data[5*x+4] = 4.8

    def getTempExtIn(self) -> float:
        self.i += 1
        t = self.data[self.i]
        print("t=",t)
        return t

    def setPower(self,power:int):
        pass

