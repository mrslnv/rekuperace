import simpy
import simpy.rt

def processB(env):
    print("Process B")
    for i in range(3):
        yield env.timeout(1.3)
        print("Process B",i)
    env.process(processA(env))


def processA(env):
    print("Process A")
    for i in range(3):
        yield env.timeout(1.4)
        print("Process A",i)
    env.process(processB(env))

def processC(env):
    print("Process C")
    for i in range(100):
        yield env.timeout(2.7)
        print("Process C",i)

env = simpy.rt.RealtimeEnvironment(1)

env.process(processA(env))
env.process(processC(env))

env.run()