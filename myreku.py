#!/usr/bin/env python
"""
Pymodbus Synchronous Client Examples
--------------------------------------------------------------------------

The following is an example of how to use the synchronous modbus client
implementation from pymodbus.

It should be noted that the client can also be used with
the guard construct that is available in python 2.5 and up::

    with ModbusClient('127.0.0.1') as client:
        result = client.read_coils(1,10)
        print result
"""
# --------------------------------------------------------------------------- # 
# import the various server implementations
# --------------------------------------------------------------------------- # 
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
    # ------------------------------------------------------------------------# 
    # choose the client you want
    # ------------------------------------------------------------------------# 
    # make sure to start an implementation to hit against. For this
    # you can use an existing device, the reference implementation in the tools
    # directory, or start a pymodbus server.
    #
    # If you use the UDP or TCP clients, you can override the framer being used
    # to use a custom implementation (say RTU over TCP). By default they use
    # the socket framer::
    #
    #    client = ModbusClient('localhost', port=5020, framer=ModbusRtuFramer)
    #
    # It should be noted that you can supply an ipv4 or an ipv6 host address
    # for both the UDP and TCP clients.
    #
    # There are also other options that can be set on the client that controls
    # how transactions are performed. The current ones are:
    #
    # * retries - Specify how many retries to allow per transaction (default=3)
    # * retry_on_empty - Is an empty response a retry (default = False)
    # * source_address - Specifies the TCP source address to bind to
    #
    # Here is an example of using these options::
    #
    #    client = ModbusClient('localhost', retries=3, retry_on_empty=True)
    # ------------------------------------------------------------------------# 

    # client = ModbusClient('localhost', port=5020)

    client = ModbusClient('192.168.1.92', port=502)

    # client = ModbusClient('192.168.99.100', port=1502)
    # client = ModbusClient(method='ascii', port='/dev/pts/2', timeout=1)
    # client = ModbusClient(method='rtu', port='/dev/ttyp0', timeout=1)
    client.connect()
    print("Connected - fake reku")

# Reku
    for i in range(0,4):
        print("Reading reg ",i)
        reg = client.read_input_registers(2*i, 2)
        s = struct.pack('<HH',reg.registers[0],reg.registers[1])
        print(i,' ',struct.unpack('f',s))


if __name__ == "__main__":
    run_sync_client()
