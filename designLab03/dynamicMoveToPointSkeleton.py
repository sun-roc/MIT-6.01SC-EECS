import lib601.sm as sm
import lib601.util as util
import math

# Use this line for running in idle
# import lib601.io as io
# Use this line for testing in soar
from soar.io import io

class DynamicMoveToPoint(sm.SM):
    startState='none'
    def getNextValues(self, state, inp):
        # Replace this definition
        print inp
        p1 = util.Point(1.0,0.5)
        pose0 = inp.odometry
        p0 = pose0.point()
        inp = (p1,p0)
        axu = p0.angleTo(p1)
        axi = util.fixAnglePlusMinusPi(pose0.theta)
        print 'DynamicMoveToPoint', 'state=', state, 'inp=', inp
        assert isinstance(inp,tuple), 'inp should be a tuple'
        assert len(inp) == 2, 'inp should be of length 2'
        assert isinstance(inp[0],util.Point), 'inp[0] should be a Point'
        rotatev = 0.05*axu
        gov = 0.2*(p0.distance(p1))
        anglewu = 0.005
        diswu = 0.005
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
        return (state, io.Action())
