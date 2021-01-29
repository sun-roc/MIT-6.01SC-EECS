import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

# the input is an io.SensorInput instance
# the output should be an io.Action instance
class MySMClass(sm.SM):
    offset = 0.1
    def getNextValues(self, state, inp):
        pass
################
# Your code here
################


mySM = MySMClass()
mySM.name = 'brainSM'

def settleTime(samples, epsilon=0.05):
    inRange = [abs(s-samples[-1])<epsilon for s in samples]
    lastBadIdx = None
    for i in range(len(samples)-2, -1, -1):
        if not inRange[i]:
            lastBadIdx = i
            break
    return lastBadIdx
    

######################################################################
###
###          Brain methods
###
######################################################################

def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=False)
    startTheta = io.SensorInput().odometry.theta
    # static plot of robot angle (from start) vs time
    robot.gfx.addStaticPlotFunction(
        y=('angle', lambda inp: util.fixAnglePlusMinusPi(
                (inp.odometry.theta-startTheta))))

def brainStart():
    robot.behavior = mySM
    robot.behavior.start(robot.gfx.tasks())
    robot.data = []
    # Do this to be sure that the plots are cleared whenever you restart
    robot.gfx.clearPlotData()    

def step():
    inp = io.SensorInput()
    (neck, left, right) = inp.analogInputs[0:3]
    print 'neck=', neck, 'left=', left, 'right=', right
    robot.behavior.step(inp).execute()
    robot.data.append(left-right)

def brainStop():
    print 'settle time: ', settleTime(robot.data)

def shutdown():
    pass
