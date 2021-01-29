import lib601.sm as sm
import lib601.util as util
import math
from soar.io import io

class FollowFigure(sm.SM):
    def __init__(self,square):
        self.square = square
        self.index = 0
    startState='none'
    def getNextValues(self, state, inp):
        # Replace this definition
        p1 = self.square[self.index]
        print "shuchu"
        print p1
        pose0 = inp.odometry
        p0 = pose0.point()
        inp = (p1,p0)
        axu = p0.angleTo(p1)
        axi = util.fixAnglePlusMinusPi(pose0.theta)
        print 'DynamicMoveToPoint', 'state=', state, 'inp=', inp
        
        rotatev = 0.05*axu
        gov = 0.2*(p0.distance(p1))
        anglewu = 0.005
        diswu = 0.005
        min_sonar = min(io.SensorInput().sonars)
        if min_sonar <= 0.3:
            return("none",io.Action(fvel = 0, rvel = 0))
        if state == "none" :
            if util.nearAngle(axu,axi,anglewu) :
                return ("go",io.Action(fvel = gov, rvel = 0))
            else :
                return ("rotate",io.Action(fvel = 0, rvel = rotatev))
        if state == "rotate" :
            if util.nearAngle(axu,axi,anglewu) :
                return ("go",io.Action(fvel = gov, rvel = 0))
            else :
                return ("rotate",io.Action(fvel = 0, rvel = rotatev))
        if state == "go":
            if p0.isNear(p1,diswu) :
                return ("stop",io.Action(fvel = 0, rvel = 0))
            else :
                return ("go",io.Action(fvel = gov, rvel = 0))
        if state == "stop":
            self.index = self.index + 1
            if self.index>=len(self.square) :
                self.index = len(self.square)-1
                return ("stop",io.Action(fvel = 0, rvel = 0))
            else :
                return ("none",io.Action(fvel = gov, rvel = 0))
        
        return (state, io.Action())
