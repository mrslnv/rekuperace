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

    def getInputRegister(self, index) -> float:
        pass

    def getTempExtIn(self) -> float:
        pass

    def getHeater(self) -> float:
        pass

    def getEngine1(self) -> float:
        pass

    def getEngine2(self) -> float:
        pass

class VentboxClient(AbstractClient):
    def __init__(self) -> None:
        super().__init__()
        self.client = ModbusClient('192.168.1.92', port=502)
        self.client.connect()
        print("Connected")

    def getInputRegister(self, index) -> float:
        reg = self.client.read_input_registers(index, 2)
        s = struct.pack('<HH', reg.registers[0], reg.registers[1])
        return struct.unpack('f', s)[0]

    def getTempExtIn(self) -> float:
        return self.getInputRegister(0)

    def getHeater(self) -> float:
        return self.getInputRegister(16)

    def getEngine1(self) -> float:
        return self.getInputRegister(12)

    def getEngine2(self) -> float:
        return self.getInputRegister(14)

    def setPower(self, power: int) -> None:
        self.power = power
        s = struct.pack('>f', power)
        i1, i2 = struct.unpack('>HH', s)
        self.client.write_register(6, i2)
        self.client.write_register(6 + 1, i1)

    def closeReku(self):
        self.client.close()


class TestClient(AbstractClient):
    def __init__(self,shouldLog) -> None:
        super().__init__()
        self.i = -1
        self.dataT = np.empty(500)
        self.shouldLog = shouldLog
        for x in range(5):
            self.dataT[5 * x] = 5.1
            self.dataT[5 * x + 1] = 5.2
            self.dataT[5 * x + 2] = 4.8
            self.dataT[5 * x + 3] = 5.1
            self.dataT[5 * x + 4] = 4.8


        for x in range(5, 100):
            self.dataT[5 * x] = 5.1
            self.dataT[5 * x + 1] = 5.0
            self.dataT[5 * x + 2] = 4.8
            self.dataT[5 * x + 3] = 4.5
            self.dataT[5 * x + 4] = 4.2

        self.engine = 0
        self.heater = 0
        self.tDelta = 0.1
        self.timeout = 10

    def log(self,*args):
        if self.shouldLog:
            print(args)

    def calculate(self):
        if self.engine > 0:
            self.tDelta -= 0.1
        else:
            self.tDelta += 0.1

        if self.tDelta + self.getInputRegister(0) < 3.9:
            self.heater = 0.5
        else:
            self.heater = 0

    def getInputRegister(self, index) -> float:
        self.i += 1
        return self.dataT[self.i % 500]

    def getTempExtIn(self) -> float:
        self.calculate()

        t = self.getInputRegister(0) + self.tDelta
        self.log("getTemp:",t)
        return t

    def getHeater(self) -> float:
        self.calculate()
        self.log("getHeater:",self.heater)
        return self.heater

    def getEngine1(self) -> float:
        self.calculate()
        if self.heater > 0:
            if self.timeout > 0:
                self.engine = 30
                self.timeout -= 1
            else:
                self.timeout = 10
                self.heater = 0
                self.tDelta = 0
                self.engine = 0

        self.log("getPower:",self.engine)
        return self.engine

    def getEngine2(self) -> float:
        return self.getEngine1()

    def setPower(self, power: int):
        self.calculate()
        self.engine = power
        self.log("setPower:",power)
