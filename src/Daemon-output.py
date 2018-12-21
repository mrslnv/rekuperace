# import client.client
# import client.engine
from client.client import VentboxClient
from client.client import AbstractClient
from client.client import TestClient
from client.engine import EngineState
from simpy import Environment
import simpy
import simpy.rt
from time import sleep
import time
from time import strftime
import numpy as np
import math

# Working on better output


# SLEEP_TIME = 10
SLEEP_TIME = 10
ENGINE_POWER = 19
RESTART_DELAY = 600

env = simpy.Environment()


class DataCollector:
    PERIOD = 20

    def __init__(self, env: Environment):
        self.env = env
        self.process = env.process(self.summaryProcess())
        intervals = np.array([60,300,600,3600,5*3600,10*3600,24*3600,48*3600],np.float32)
        # 1st coll - interval length in seconds
        # 2nd coll - time % interval (if 2dn == 0, 3rd MUST be 0)
        # 3nd coll - current interval usage
        # 4rd coll - previous closed interval usage
        # 5rd coll - prev prev ...
        self.lastPeriodPower = np.zeros([intervals.shape[0],30],np.float32)
        self.lastPeriodPower[:,0] = intervals
        self.lastChange = 0

    def summaryProcess(self):
        while True:
            self.printSummary()
            yield self.env.timeout(DataCollector.PERIOD)

    def printSummary(self):
        for a in range(self.lastPeriodPower.shape[0]):
            print("Avg [ {0:3.0f} ]".format(self.lastPeriodPower[a,0]/60),end='')
            for b in range(2,7):
                print(" {0:3.0f}".format(self.lastPeriodPower[a,b]),end='')
            print()

    def updatePower(self, old, time):
        if old <= 0:
            return
        # print("up",self.lastPeriodPower)
        DataCollector.updateArray(self.lastPeriodPower, time - self.lastChange, old)
        # print("after up",self.lastPeriodPower)
        self.lastChange = time

    def updateArray(what, deltaSinceLast, power):
        for a in range(what.shape[0]):
            DataCollector.updateRow(what[a], deltaSinceLast, power)


    def updateRow(what, deltaSinceLast, power):
        period = what[0]
        lastPortion = what[1]
        newPortion = (lastPortion + deltaSinceLast) % period
        updates = math.floor((lastPortion + deltaSinceLast) / period) + 1
        updateCoefs = np.ones(min(updates, what.shape[0] - 2), what.dtype)
        if updates > 1:
            if updates > what.shape[0] - 2:
                what[2:] = 0
                updateCoefs[0] = newPortion / period
            else:
                what[updates + 1:] = what[2:-updates + 1]
                what[2:updates+1] = 0
                updateCoefs[-1] = (period - lastPortion) / period
                updateCoefs[0] = newPortion / period
        else:
            updateCoefs[0] = (newPortion - lastPortion) / period
        newUsage = updateCoefs * power
        what[2:2 + updates] += newUsage
        what[1] = newPortion

    def updateTemperature(self, t, now):
        #ToDo: temp gradient
        pass

    def updateHeater(self, actualHeater, now):
        #ToDo: heat
        pass


class BulkDecider:
    def __init__(self, ec: 'EngineController', dc: DataCollector):
        self.ec = ec
        self.dc = dc
        self.deciders = []

    def should(self):
        for d in self.deciders:
            if (not d(self.ec, self.dc)):
                return False
        return True

    def add(self, shouldFunction):
        return self.deciders.append(shouldFunction)


class EngineController:
    PERIOD = 10
    ACTIVE_PERIOD = 0.5
    ACTIVE_POWER = 25
    PASSIVE_POWER = 0
    PASSIVE_PERIOD = 10
    RESTART_DELAY = 60

    def __init__(self, env: Environment, client: AbstractClient, dataCol: DataCollector):
        self.env = env
        self.client = client
        self.dataCol = dataCol
        self.period = EngineController.PASSIVE_PERIOD
        self.desiredPower = EngineController.PASSIVE_POWER
        env.process(self.passiveProcess())
        env.process(self.runEngineProcess())
        self.shouldStart = BulkDecider(self, dataCol)
        self.shouldStop = BulkDecider(self, dataCol)
        self.lastStopTime = 0

    def runEngineProcess(self):
        while True:
            self.readTemperature()
            self.updatePower()
            self.setPower()
            print("==> keep running ",self.desiredPower)
            yield env.timeout(self.PERIOD)

    def passiveProcess(self):
        while True:
            self.readTemperature()
            self.readPower()
            self.readHeater()
            if (self.shouldStart.should()):
                self.env.process(self.activeProcess())
                self.changePower(EngineController.ACTIVE_POWER)
                return
            print("==> passive ",self.desiredPower)
            yield env.timeout(self.PASSIVE_PERIOD)

    def activeProcess(self):
        while True:
            self.readTemperature()
            self.readPower()
            self.readHeater()
            if (self.shouldStop.should()):
                self.changePower(EngineController.PASSIVE_POWER)
                self.lastStopTime = env.now
                self.env.process(self.passiveProcess())
                return
            print("==> active ",self.desiredPower)
            yield env.timeout(self.ACTIVE_PERIOD)

    def addShouldStop(self,decider):
        self.shouldStop.add(decider)

    def addShouldStart(self,decider):
        self.shouldStart.add(decider)

    def readTemperature(self):
        self.t = self.client.getTempExtIn()
        self.dataCol.updateTemperature(self.t, self.env.now)

    def readPower(self):
        self.actualPower = self.client.getEngine1()
        self.dataCol.updatePower(self.actualPower, self.env.now)

    def readHeater(self):
        self.actualHeater = self.client.getHeater()
        self.dataCol.updateHeater(self.actualHeater, self.env.now)

    def setPower(self)->float:
        self.client.setPower(self.desiredPower)

    def changePower(self, power):
        oldActual = self.actualPower
        self.desiredPower = power
        self.actualPower = self.client.getEngine1()
        self.dataCol.updatePower(old=oldActual, time=self.env.now)

    def updatePower(self):
        oldActual = self.actualPower
        self.actualPower = self.client.getEngine1()
        self.dataCol.updatePower(old=oldActual, time=self.env.now)

class Deciders:
    TEMP_STOP = 0.5

    def shouldStartTempAbove(ec: EngineController, dc: DataCollector) -> bool:
        print("Should start? temp above:",ec.t," above ", Deciders.TEMP_STOP)
        if ec.t > Deciders.TEMP_STOP:
            return True
        return False

    def shouldStopTempBelow(ec: EngineController, dc: DataCollector) -> bool:
        print("Should stop? temp below:",ec.t," below ", Deciders.TEMP_STOP)
        if ec.t <= Deciders.TEMP_STOP:
            return True
        return False

    def shouldStartOnlyWithDelay(ec: EngineController, dc: DataCollector) -> bool:
        print("Should delay? delay",ec.env.now - ec.lastStopTime)
        if (ec.env.now - ec.lastStopTime) > EngineController.RESTART_DELAY:
            return True
        return False


    def shouldStopHeater(ec: EngineController, dc: DataCollector) -> bool:
        print("Should stop heater? h=",ec.actualHeater," e= ", ec.actualPower)
        if ec.actualHeater > 0.4 and ec.actualPower == 30:
            return True
        return False


env = simpy.rt.RealtimeEnvironment(factor=0.03)

c = EngineController(env, TestClient(True), DataCollector(env))
c.addShouldStop(Deciders.shouldStopTempBelow)
c.addShouldStop(Deciders.shouldStopHeater)
c.addShouldStart(Deciders.shouldStartTempAbove)
c.addShouldStart(Deciders.shouldStartOnlyWithDelay)

env.sync()
env.run()
