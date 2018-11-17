from client import *
from time import sleep

# cl = client.VentboxClient()
cl = client.VentboxClient()
while True:
    t = cl.getTempExtIn()
    print("Temp:",t)
    if t<=5:
        print("Motor - stop")
        cl.setPower(0)
    else:
        print("Motor - run")
        cl.setPower(20)
    sleep(10)
