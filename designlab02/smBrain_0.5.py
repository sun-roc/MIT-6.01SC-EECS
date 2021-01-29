import math
import lib601.util as util
import lib601.sm as sm
import lib601.gfx as gfx
from soar.io import io

class MySMClass(sm.SM):
    startState = 'up'
    def getNextValues(self, state, inp):
        sonars = inp.sonars
        f_sonars = sonars[2:7]
        '''
        因为声纳的第四个和第五个返回值都不是垂直于墙的距离，所以将临界距离设置为一个范围
        可同时解决小车到达临界距离时，前后震荡的问题
        '''
        dis_min = 0.48   #距离墙的临界距离
        dis_max = 0.52   #距离墙的临界距离
        if state =='up':
            #当距离小于0.5时，返回下一个状态 back
            if min(f_sonars)<=dis_min:
                return ('back', io.Action(fvel = -0.05, rvel = 0))
            #当距离大于0.5时，返回下一个状态 up
            elif min(f_sonars)>dis_max:
                return ('up',io.Action(fvel = 0.05, rvel = 0))
            #在这个区间，即认为小车到达了距离墙面0.5m的距离，返回下一个状态 stop
            elif min(f_sonars)<dis_max and min(f_sonars)>dis_min:
                return ('stop',io.Action(fvel = 0, rvel = 0))
        if state == 'back':
            if min(f_sonars)<=dis_min:
                return ('back', io.Action(fvel = -0.05, rvel = 0))
            elif min(f_sonars)>dis_max:
                return ('up', io.Action(fvel = 0.05, rvel = 0))
            elif min(f_sonars)<dis_max and min(f_sonars)>dis_min:
                return ('stop',io.Action(fvel = 0, rvel = 0))
        if state == 'stop':
            if min(f_sonars)<=dis_min:
                return ('back', io.Action(fvel = -0.05, rvel = 0))
            elif min(f_sonars)>dis_max:
                return ('up', io.Action(fvel = 0.05, rvel = 0))
            elif min(f_sonars)<dis_max and min(f_sonars)>dis_min:
                return ('stop',io.Action(fvel = 0, rvel = 0))
        #return (state, io.Action(fvel = 0, rvel = 0))
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
    robot.gfx = gfx.RobotGraphics(drawSlimeTrail=False, # slime trails
                                  sonarMonitor=False) # sonar monitor widget
    
    # set robot's behavior
    robot.behavior = mySM

# this function is called when the start button is pushed
def brainStart():
    robot.behavior.start(traceTasks = robot.gfx.tasks())

# this function is called 10 times per second
def step():
    inp = io.SensorInput()
    print inp.sonars[3]
    robot.behavior.step(inp).execute()
    io.done(robot.behavior.isDone())

# called when the stop button is pushed
def brainStop():
    pass

# called when brain or world is reloaded (before setup)
def shutdown():
    pass
