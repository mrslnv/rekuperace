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
        intervals = np.array([60,120,300,600,3600,7200,5*3600,10*3600,24*3600,48*3600],np.float32)
        self.lastPeriodPower = np.zeros([intervals.shape[0],2],np.float32)
        self.lastPeriodPower[:,0] = intervals
        self.tGrad = np.zeros([intervals.shape[0],2],np.float32)
        self.tGrad[:,0] = intervals
        self.lastChange = 0

    def summaryProcess(self):
        while True:
            self.printSummary()
            yield self.env.timeout(DataCollector.PERIOD)

    def printSummary(self):
        print("Data 123")

    def shouldStart(ec, dc):
        return True

    def shouldStop(ec, dc):
        return True

    def changePower(self, old, new):
        if old <= 0:
            return
        print("up",self.lastM)
        DataCollector.updateInterval([self.lastM], 60, self.env.now - self.lastChange, old)
        print("after up",self.lastM)
        self.lastChange = self.env.now

    def updateInterval(what, range, delta, power):
        what[0] = power if delta > range else (power * delta)/range
        print("new?",what[0])

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
    PERIOD = 12
    ACTIVE_PERIOD = 0.5
    ACTIVE_POWER = 25
    PASSIVE_POWER = 0
    PASSIVE_PERIOD = 12
    TEMP_STOP = 4.3
    RESTART_DELAY = 60

    def __init__(self, env: Environment, client: AbstractClient, dataCol: DataCollector):
        self.env = env
        self.client = client
        self.dataCol = dataCol
        self.period = EngineController.PASSIVE_PERIOD
        self.power = EngineController.PASSIVE_POWER
        env.process(self.passiveProcess())
        env.process(self.runEngineProcess())
        self.passiveDecider = BulkDecider(self, dataCol)
        self.passiveDecider.add(EngineController.shouldStart)
        self.passiveDecider.add(DataCollector.shouldStart)
        self.activeDecider = BulkDecider(self, dataCol)
        self.activeDecider.add(DataCollector.shouldStop)
        self.lastStopTime = 0

    def runEngineProcess(self):
        while True:
            self.setPower()
            yield env.timeout(self.PERIOD)

    def passiveProcess(self):
        while True:
            self.t = self.client.getTempExtIn()
            if (self.t > EngineController.TEMP_STOP and self.passiveDecider.should()):
                self.env.process(self.activeProcess())
                self.changePower(EngineController.ACTIVE_POWER)
                return
            yield env.timeout(self.PASSIVE_PERIOD)

    def activeProcess(self):
        while True:
            self.t = self.client.getTempExtIn()
            if (self.t <= EngineController.TEMP_STOP and self.activeDecider.should()):
                self.changePower(EngineController.PASSIVE_POWER)
                self.lastStopTime = env.now
                self.env.process(self.passiveProcess())
                return
            yield env.timeout(self.ACTIVE_PERIOD)

    def shouldStart(ec, dc) -> bool:
        if (env.now - ec.lastStopTime) < EngineController.RESTART_DELAY:
            return False
        return True

    def setPower(self):
        self.client.setPower(self.power)

    def changePower(self, power):
        self.dataCol.changePower(old=self.power, new=power)
        self.power = power
        self.setPower()


env = simpy.rt.RealtimeEnvironment(factor=0.03)

c = EngineController(env, TestClient(), DataCollector(env))
env.sync()
env.run()
