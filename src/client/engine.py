from time import sleep
import time
from time import strftime

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
