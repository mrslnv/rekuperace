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

    powers = [0.2, 0.5, 0.333, 0.35]
    for i in range(4):
        power = powers[i]
    # Reku
        setPower2(client, power)

#does not work :-(
def setPower1(client, power):
    print("Setting power to:", power)
    s = struct.pack('f', power)
    i1, i2 = struct.unpack('<HH', s)
    client.write_register(20 * 2, i1)
    client.write_register(20 * 2 + 1, i2)
    sleep(10)
    print("done with ", power)

def setPower2(client, power):
    print("Setting power to:", power)
    s = struct.pack('f', power)
    i1, i2 = struct.unpack('<HH', s)
    client.write_register(6 * 2, i1)
    client.write_register(6 * 2 + 1, i2)
    sleep(10)
    print("done with ", power)


run_sync_client()
