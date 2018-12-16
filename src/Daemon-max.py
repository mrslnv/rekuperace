from client import *
from time import sleep
import time
from time import strftime


class EngineState:
    lastChange = time.time()
    currentPower = 0
    lastStopTime = 0
    lastHourUsage = 0

    def changePower(self, newPower):
        if self.currentPower == newPower:
            return
        if newPower == 0:
            self.lastStopTime = time.time()

        self.currentPower = newPower


# SLEEP_TIME = 10
SLEEP_TIME = 10
ENGINE_POWER = 25
RESTART_DELAY = 200
PRINT_DELAY = 2
printTime = 0


def now():
    return strftime('%H:%M:%S %d.%m.', time.localtime(time.time()))


while True:
    try:
        cl = client.VentboxClient()
        # cl = client.TestClient()

        es = EngineState()
        desiredPower = ENGINE_POWER
        while True:
            t = cl.getTempExtIn()
            h = cl.getHeater()
            e1 = cl.getEngine1()
            e2 = cl.getEngine2()

            if (time.time() - printTime) > PRINT_DELAY:
                print(now(), " Temp: ", t, "Heat: ", h, "EngineA: ", e1, "EngineB: ", e2)
                print(now(), " Power:", desiredPower)
                printTime = time.time()

            if h > 0.2 and e1 > 29.5 and e1 < 30.5:
                print(now(), " Motor - stop")
                desiredPower = 0
                SLEEP_TIME = 18
            else:
                if es.currentPower > 0:
                    desiredPower = ENGINE_POWER
                else:
                    if (time.time() - es.lastStopTime) > RESTART_DELAY and t > 0.5:
                        print(now(), " Motor - starting ")
                        desiredPower = ENGINE_POWER
                        SLEEP_TIME = 0.5
                    else:
                        print(now(), " Motor - not starting, delta:", (time.time() - es.lastStopTime))
                        desiredPower = 0

            cl.setPower(desiredPower)
            es.changePower(desiredPower)
            sleep(SLEEP_TIME)
    except Exception as e:
        print(now(), " Error:", e)
        try:
            cl.closeReku()
        except Exception as e2:
            print(now(), " Error while closing:", e)

    print(now(), " Retry")
    sleep(21)
