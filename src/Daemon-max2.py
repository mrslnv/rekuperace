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
RESTART_DELAY = 120
PRINT_DELAY = 5
printTime = 0
tempAtStart=4
TEMP_TRASHOLD=4
shouldStop = False


def now():
    return strftime('%H:%M:%S %d.%m.', time.localtime(time.time()))


while True:
    try:
        SLEEP_TIME = 10
        ENGINE_POWER = 25
        RESTART_DELAY = 240
        PRINT_DELAY = 5
        printTime = 0
        tempAtStart=4
        TEMP_TRASHOLD=4
        shouldStop = False

        cl = client.VentboxClient()
        # cl = client.TestClient()

        es = EngineState()
        desiredPower = ENGINE_POWER

        while True:
            t = cl.getTempExtIn()
            h = cl.getHeater()
            e1 = cl.getEngine1()
            e2 = cl.getEngine2()

            if shouldStop:
                if e1 == 0:
                    shouldStop = False
                    TEMP_TRASHOLD = max(tempAtStart - t, 2)
					
            if time.time() - es.lastStopTime > 560:
                TEMP_TRASHOLD = 4    

            if (time.time() - printTime) > PRINT_DELAY:
                print(now(), " Temp: ", round(t,2), " Heat: ", round(h,2), " EngineA: ", round(e1,2), " EngineB: ", round(e2,2))
                print(now(), " Power:", desiredPower, " Temp Tresh:", TEMP_TRASHOLD)
                printTime = time.time()

            if h > 0.2 and e1 > 29.5 and e1 < 30.5:
                print(now(), " Motor - stop")
                desiredPower = 0
                shouldStop = True
                SLEEP_TIME = 18
            else:
                if es.currentPower > 0:
                    desiredPower = ENGINE_POWER
                else:
                    if (time.time() - es.lastStopTime) > RESTART_DELAY and t > TEMP_TRASHOLD:
                        print(now(), " Motor - starting ")
                        desiredPower = ENGINE_POWER
                        tempAtStart = t
                        SLEEP_TIME = 0.5
                    else:
                        print(now(), " Motor - not starting, delta:", round(time.time() - es.lastStopTime,0))
                        if desiredPower>0:
                            shouldStop = True
                        desiredPower = 0
                        SLEEP_TIME = 18

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
