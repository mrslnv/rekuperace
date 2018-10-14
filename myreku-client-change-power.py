#!/usr/bin/env python
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
#from pymodbus.client.sync import ModbusUdpClient as ModbusClient
# from pymodbus.client.sync import ModbusSerialClient as ModbusClient

# --------------------------------------------------------------------------- # 
# configure the client logging
# --------------------------------------------------------------------------- # 
import logging
import struct
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

# Reku
    for i in range(0,4):
        print("Reading reg ",i)
        reg = client.read_input_registers(2*i, 2)
        s = struct.pack('<HH',reg.registers[0],reg.registers[1])
        print(i,' ',struct.unpack('f',s))


run_sync_client()
