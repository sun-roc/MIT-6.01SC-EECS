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
    startState="turn"
    def getNextValues(self, state, inp):
        V_Location = inp.analogInputs[1]
        V_Light = inp.analogInputs[2]
        V_Base = 5
        V_0.5 = 7.5
        V_thh = 8
        V_thl = 7
        V_nolight = 9.6
        V_diffLocation = V_Base - V_Location
        V_diffLight = V_Light - V_0.5
        print V_Light
        #a is aerfa
        #a = 1 - V_Location/10.0
        k_Location = 0.5
        k_Light = 1
        #HeadAngle = a*1.5*math.pi - math.pi/4
        #pose0 = inp.odometry
        # if state == 'stop':
        #     if V_Location == V_Base or V_Light >V_nolight :
        #         return('light',io.Action(fvel = 0, rvel = 0))
        #     else :
        #         return('turn',io.Action(fvel = 0,
        #                                 rvel = k_Location*V_diffLocation))
        if state == 'turn':
            if V_Location == V_Base:
                return("light",io.Action(fvel = 0, rvel = 0))
            else :
                return('turn',io.Action(fvel = 0,
                                        rvel = k_Location*V_diffLocation))
        if state == 'light':
            # if V_Light >= V_nolight:
            #     return('turn',io.Action(fvel = 0, rvel = 0))
            if V_thl <= V_Light and V_Light <= V_thh:
                return('turn',io.Action(fvel = 0, rvel = 0))
            elif V_Light < V_thl:
                return('light',io.Action(fvel = -k_Light*V_diffLight, rvel = 0))
            elif V_Light > V_thh:
                return('light',io.Action(fvel = k_Light*V_diffLight, rvel = 0))
            

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
