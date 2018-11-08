#!/usr/bin/env python
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
#from pymodbus.client.sync import ModbusUdpClient as ModbusClient
# from pymodbus.client.sync import ModbusSerialClient as ModbusClient

# --------------------------------------------------------------------------- # 
# configure the client logging
# --------------------------------------------------------------------------- # 
import logging
import struct
from time import sleep

logging.basicConfig()
log = logging.getLogger()
# log.setLevel(logging.DEBUG)
log.setLevel(logging.ERROR)

UNIT = 0x1

def print_reg(reg):
    v = reg.registers[0]
    print(v, " ", format(v,'#04x')," ", format(v,'#10x'))

def run_sync_client():
    client = ModbusClient('192.168.1.92', port=502)
    client.connect()
    print("Connected")

    powers = [float(0), float(15.15), float(18.18), float(20.20), float(22.22), float(33.3),
              float(27.27),float(10.10),float(5.5),float(0)]
    for i in range(len(powers)*10):
        power = powers[i%len(powers)]
    # Reku
        setPower1(client, power)
        # setPower(client, power, 0)

#does not work :-(
def setPower1(client, power):
    print("Setting power to:", power)
    s = struct.pack('>f', power)
    i1, i2 = struct.unpack('>HH', s)
    client.write_register(6, i2)
    client.write_register(6 + 1, i1)
    sleep(5)
    print("done with ", power)

def setPower2(client, power,regOffset):
    print("Setting power for: ",2+regOffset,"to :", power)
    # client.write_register(6, 0xFF)
    s = struct.pack('f', power)
    i1, i2 = struct.unpack('>HH', s)
    client.write_register(6, i1)
    client.write_register(8, i2)
    # client.write_register(6 + 1, i2)
    sleep(10)
    print("done with ", power)
    client.write_register(6, 0)
    sleep(10)

run_sync_client()
