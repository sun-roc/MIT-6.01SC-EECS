import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

import os
labPath = os.getcwd()
from sys import path
if not labPath in path:
    path.append(labPath)
    print 'setting labPath to', labPath

#from boundaryFollower import boundaryFollowerClass
        
class MySMClass(sm.SM):
    startState = 'stop'
    def getNextValues(self, state, inp):
        V01 = inp.analogInputs[1]
        V02 = inp.analogInputs[2]
        V_pot = 5.2
        V_half = 7.5
        V_thh = 7.7
        V_thl = 7.3
        dif1 = (V_pot - V01)
        dif2 = (V02 - V_half)
        k1 = 0.5 #best gain and the highest gain is 0.7
        k2 = 0.1
        rotatev = k1*dif1
        forwardv = k2*dif2
        print V01
        print V02
        if state == 'stop':
            if V01 <= 4.9 or V01 >= 5.6:
                return ('rotate', io.Action(fvel = 0, rvel = rotatev))
            else:
                if V02 >= V_thl and V02 <= V_thh:
                    return ('stop', io.Action(fvel = 0, rvel = 0))
                else:
                    return ('go', io.Action(fvel = forwardv, rvel = 0))                        
        if state == 'rotate':
            if V01 <= 4.9 or V01 >= 5.6:
                return ('rotate', io.Action(fvel = 0, rvel = rotatev))
            else:
                if V02 >= V_thl and V02 <= V_thh:
                    return ('stop', io.Action(fvel = 0, rvel = 0))
                else:
                    return ('go', io.Action(fvel = forwardv, rvel = 0))  
        if state == 'go':
            if V01 <= 4.9 or V01 >= 5.6:
                return ('rotate', io.Action(fvel = 0, rvel = rotatev))
            else:
                if V02 >= V_thl and V02 <= V_thh:
                    return ('stop', io.Action(fvel = 0, rvel = 0))
                else:
                    return ('go', io.Action(fvel = forwardv, rvel = 0))  
                
mySM = MySMClass()
mySM.name = 'brainSM'
    

######################################################################
###
###          Brain methods
###
######################################################################

def setup():
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=False)

def brainStart():
    robot.behavior = mySM
    robot.behavior.start(robot.gfx.tasks())
    robot.data = []

def step():
    inp = io.SensorInput()
    robot.behavior.step(inp).execute()

def brainStop():
    pass

def shutdown():
    pass
