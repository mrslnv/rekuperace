# print (format(0xff,'#04x'))
# print (format(0xff,'#14x'))

import struct

def convert(v1,v2, type,endian):
    print("in:",v1,"  ",v2,"    endian=",endian)
    print("in:",format(v1,'#04x'),"  ",format(v2,'#04x'))
    s = struct.pack(endian+type+type,v1,v2)
    # print(s)
    p = struct.unpack('f',s)
    print(p)

# r1=0x40be
# r2=0xb08d

r1 = 0x3895
r2 = 0x9a84


for v1,v2 in [[0x3895,0x9a84],[0x40be,0xb08d],[0x8c99,0x4126],[0xe54c,0x41a8]]:
    for endian in ['<']:
        convert(v1,v2,'H',endian)
        # convert(v2,v1,'H',endian)
        # convert(v1,0,'H',endian)
        # convert(0,v2,'H',endian)
        # convert(v2,0,'H',endian)
        # convert(v1,v1,'H',endian)
        # convert(v2,v2,'H',endian)

