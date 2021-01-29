import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
import lib601.sonarDist as sonarDist
from soar.io import io

class MySMClass(sm.SM):  
    startState='go'  #初始状态
    def getNextValues(self, state, inp):  #将各个声呐的值打印
        sonarValues = inp.sonars
        n=0
        for i in inp.sonars:
            n=n+1
            print int(n),round(i,2)
        up_distance = min(inp.sonars[3:5])
        right_soar = inp.sonars[7]
        xie  = inp.sonars[6]  
        if state == "go":
            if right_soar <= 0.5 and right_soar >0.3 and  up_distance > 0.4:
                return ("go", io.Action(fvel = 0.1, rvel = 0))
            elif right_soar <= 0.5:
                return ("left", io.Action(fvel = 0.1,rvel = 0.5))
            elif up_distance <=0.5:
                return ("left", io.Action(fvel = 0.1, rvel = 0.5))
            else:
                return ("right", io.Action(fvel = 0.2, rvel = -0.5))
        if state == "right":
            if right_soar <= 0.5 and right_soar >0.3 and xie <=0.7:
                return ("go", io.Action(fvel = 0.05, rvel = 0))
            elif right_soar <= 0.5:
                return ("left", io.Action(fvel = 0.1, rvel = 0.5))
            elif up_distance <=0.5:
                return ("left", io.Action(fvel = 0.1, rvel = 0.5))
            else:
                return ("right", io.Action(fvel = 0.2, rvel = -0.5))
        if state == "left":
            if right_soar <= 0.5 and right_soar >0.3 and up_distance > 0.4:
                return ("go", io.Action(fvel = 0.1, rvel = 0))
            elif right_soar <= 0.5:
                return ("left", io.Action(fvel = 0.1, rvel = 0.5))
            elif up_distance <=0.5:
                return ("left", io.Action(fvel = 0.1, rvel = 0.5))
            else:
                return ("right", io.Action(fvel = 0.2, rvel = -0.5))
        return (state, io.Action(fvel = 0, rvel = 0))

mySM = MySMClass()
mySM.name = 'brainSM'

######################################################################
###
###          Brain methods
###
######################################################################

def plotSonar(sonarNum):
    robot.gfx.addDynamicPlotFunction(y=('sonar'+str(sonarNum),
                                        lambda: 
                                        io.SensorInput().sonars[sonarNum]))

# this function is called when the brain is (re)loaded
def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=True, # slime trails
                                  sonarMonitor=False) # sonar monitor widget
    
    # set robot's behavior
    robot.behavior = mySM

# this function is called when the start button is pushed
def brainStart():
    robot.behavior.start(traceTasks = robot.gfx.tasks())

# this function is called 10 times per second
def step():
    inp = io.SensorInput()
    #print inp.sonars[3]
    robot.behavior.step(inp).execute()
    io.done(robot.behavior.isDone())

# called when the stop button is pushed
def brainStop():
    pass

# called when brain or world is reloaded (before setup)
def shutdown():
    pass
