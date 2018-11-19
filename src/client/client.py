from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import logging
import struct
import numpy as np


class AbstractClient:
    def __init__(self):
        pass

    def getTempExtIn(self) -> float:
        return 0

    def setPower(self, power: int) -> None:
        pass

    def closeReku(self) -> None:
        pass


class VentboxClient(AbstractClient):
    def __init__(self) -> None:
        super().__init__()
        self.client = ModbusClient('192.168.1.92', port=502)
        self.client.connect()
        print("Connected")

    def getTempExtIn(self) -> float:
        reg = self.client.read_input_registers(0, 2)
        s = struct.pack('<HH', reg.registers[0], reg.registers[1])
        return struct.unpack('f', s)[0]

    def setPower(self, power: int) -> None:
        self.power = power
        s = struct.pack('>f', power)
        i1, i2 = struct.unpack('>HH', s)
        self.client.write_register(6, i2)
        self.client.write_register(6 + 1, i1)

    def closeReku(self):
        self.client.close()


class TestClient(AbstractClient):
    def __init__(self) -> None:
        super().__init__()
        self.i = -1
        self.data = np.empty(500)
        # for x in range(5):
        #     self.data[5*x] = 5.1
        #     self.data[5*x+1] = 5.2
        #     self.data[5*x+2] = 4.8
        #     self.data[5*x+3] = 5.1
        #     self.data[5*x+4] = 4.8


        for x in range(1, 5):
            self.data[5 * x] = 5.1
            self.data[5 * x + 1] = 5.2
            self.data[5 * x + 2] = 4.8
            self.data[5 * x + 3] = 5.1
            self.data[5 * x + 4] = 4.8

    def getTempExtIn(self) -> float:
        self.i += 1
        t = self.data[self.i]
        return t

    def setPower(self, power: int):
        pass
