from client import *
from time import sleep
import time


class EngineState:
    lastChange = time.time()
    currentPower = 0
    lastStopTime = 0
    lastHourUsage = 0

    def changePower(self,newPower):
        if self.currentPower == newPower:
            return
        if newPower == 0:
            self.lastStopTime = time.time()

        self.currentPower = newPower



cl = client.VentboxClient()
# cl = client.TestClient()
es = EngineState()
while True:
    t = cl.getTempExtIn()
    print("Temp:",t)

    desiredPower = 20
    if t<=6:
        print("Motor - stop")
        desiredPower = 0
    else:
        if es.currentPower > 0:
            print("Motor - already running ",time.time())
            desiredPower = 20
        else:
            if (time.time() - es.lastStopTime) > 180:
                print("Motor - starting ",time.time())
                desiredPower = 20
            else:
                print("Motor - not starting, delta:", (time.time() - es.lastStopTime))
                desiredPower = 0

    print("Setting power:",desiredPower,"time:",time.time())
    cl.setPower(desiredPower)
    es.changePower(desiredPower)
    sleep(10)
