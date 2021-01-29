import lib601.dist as dist
import lib601.coloredHall as coloredHall
from lib601.coloredHall import *
import lib601.util as util
import math

standardHallway = ['white', 'white', 'green', 'white', 'white']
alternating = ['white', 'green'] * 6
sterile = ['white'] * 16
testHallway = ['chocolate', 'white', 'green', 'white', 'white',
               'green', 'green', 'white',  
               'green', 'white', 'green', 'chocolate']
possibileColors=['black','white','red','green','blue']
maxAction = 5
actions = [str(x) for x in range(maxAction) + [-x for x in range(1, maxAction)]]

def makePerfect(hallway = standardHallway):
    return makeSim(hallway, actions, perfectObsNoiseModel,
                   standardDynamics, perfectTransNoiseModel,'perfect')

def makeNoisy(hallway = standardHallway):
    return  makeSim(hallway, actions, noisyObsNoiseModel, standardDynamics,
                    noisyTransNoiseModel, 'noisy')

def makeNoisyKnownInitLoc(initLoc, hallway = standardHallway):
    return  makeSim(hallway, actions, noisyObsNoiseModel, standardDynamics,
                    noisyTransNoiseModel, 'known init',
                    initialDist = dist.DDist({initLoc: 1}))
###########################################
# This is Problem 11.1.1
###########################################
def whiteEqGreenObsDist(actualColor):
    if actualColor=='white' or actualColor=='green':
        return dist.DDist({'white': 0.5,'green': 0.5})
    else:
        return dist.DDist({actualColor:1})
def whiteVsGreenObsDist(actualColor):
    if actualColor == 'white':
        return dist.DDist({'green':1.0})
    elif actualColor == 'green':
        return dist.DDist({'white':1.0})
    else :
        return dist.DDist({actualColor:1.0})
def noisyObs(actualColor):
    lists = possibleColors
    lists.remove(actualColor)
    dists ={actualColor: 0.8}
    for i in range(4):
        dists.update({lists[i]:0.05})
    return dist.DDist(dists)
def black(actualColor):
    return dist.DDist({'black': 1.0})
noisyObsModel = makeObservationModel(standardHallway,noisyObs)
###########################################
# This is step1
###########################################
#p = makePerfect()
#p.run(10)


###########################################
# This is Problem 11.1.2
###########################################
def ringDynamics(loc,act,hallwayLength):
    if loc + act >= 0 and loc + act <= (hallwayLength - 1):
        return loc + act
    elif loc + act < 0:
        return loc + (hallwayLength + act)
    else :
        return loc - (hallwayLength - act)
def leftSlipTrans(nominalLoc,hallwayLength):
    if nominalLoc == 0:
        return dist.DDist({nominalLoc : 1.0})
    else :
        left = nominalLoc - 1
        return dist.DDist({nominalLoc : 0.9,left : 0.1})
def noisyTrans(nominalLoc,hallwayLength):
    if nominalLoc == 0:
        right = nominalLoc + 1
        return dist.DDist({nominalLoc : 0.9,right: 0.1})
    elif nominalLoc == hallwayLength - 1:
        left = nominalLoc - 1
        return dist.DDist({nominalLoc : 0.9,left: 0.1})
    else :
        right = nominalLoc + 1
        left = nominalLoc - 1
        return dist.DDist({nominalLoc: 0.8,right: 0.1,left: 0.1})
def standardDynamics(loc, act, hallwayLength):
    return util.clip(loc + act, 0, hallwayLength-1)
noisyTransModel = makeTransitionModel(standardDynamics,noisyTrans,5)
###########################################
# This is step2
###########################################
#n = makeNoisy()
#n.run(20)


###########################################
# This is step4
###########################################
#w = makeSim(testHallway,actions,
#            whiteVsGreenObsDist,
#            standardDynamics,perfectTransNoiseModel)
#w.run(50)



###########################################
# This is step6
###########################################
#w = makeNoisyKnownInitLoc(7,sterile)
#w.run(50)
    


###########################################
# This is Problem 11.1.6
###########################################
def sonarHit(distance, sonarPose, robotPose):
    return robotPose.transformPoint(sonarPose.transformPoint(util.Point(distance, 0)))
###########################################
# This is Problem 11.1.7
###########################################
sonarMax = 1.5
numObservations = 10
sonarPose0 = util.Pose(0.08, 0.134, 1.570796)
def wall((x1, y1), (x2, y2)):
    return util.LineSeg(util.Point(x1,y1), util.Point(x2,y2))
wallSegs = [wall((0, 2), (8, 2)),
            wall((1, 1.25), (1.5, 1.25)),
            wall((2, 1.75), (2.8, 1.75))]
robotPoses = [util.Pose(0.5, 0.5, 0),
             util.Pose(1.25, 0.5, 0),
             util.Pose(1.75, 1.0, 0),
             util.Pose(2.5, 1.0, 0)]
def discreteSonar(snoarReading):
    base = sonarMax / numObservations
    discrete = int(snoarReading / base)
    return util.clip(discrete, 0, 9)
def idealReadings(wallSegs, robotPoses):
    discreteDiss = []
    for i in range(4):
        discreteDis = []
        sonarStartPoint = sonarHit(0, sonarPose0, robotPoses[i])
        sonarEndPoint = sonarHit(sonarMax, sonarPose0, robotPoses[i])
        sonarSeg = util.LineSeg(sonarStartPoint, sonarEndPoint)
        for j in range(3):            
            if sonarSeg.intersection(wallSegs[j]) == False:
                node = None
            else :
                node = sonarSeg.intersection(wallSegs[j])
            if node == None :
                distance = sonarMax
            else :
                distance = sonarStartPoint.distance(node)
            discreteDis.append(discreteSonar(distance))
        discreteDiss.append(min(discreteDis))
    return discreteDiss        
        
        
        
    
