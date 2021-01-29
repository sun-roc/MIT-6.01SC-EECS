import math
import lib601.sonarDist as sonarDist
import lib601.sm as sm
import lib601.util as util
import lib601.gridMap as gridMap
import lib601.dynamicGridMap as dynamicGridMap
import lib601.dynamicCountingGridMap as dynamicCountingGridMap
import bayesMapSkeleton as bayesMap
reload(bayesMap)

class MapMaker(sm.SM):
    def __init__(self, xMin, xMax, yMin, yMax, gridSquareSize):
        #startstate = dynamicGridMap.DynamicGridMap(xMin, xMax, yMin, yMax, gridSquareSize)
        
        startstate = bayesMap.BayesGridMap(xMin, xMax, yMin, yMax, gridSquareSize)
        self.startState = startstate
    def getNextValues(self, state, inp):
        maps = state
        robotPose = inp.odometry
        sonars = inp.sonars
        for sonarPose, distance in zip(sonarDist.sonarPoses, sonars):
            sonar_in_robot = maps.pointToIndices(robotPose.transformPoint(sonarPose.point()))
            if distance >= sonarDist.sonarMax:
                distance = sonarDist.sonarMax
                hits = maps.pointToIndices(sonarDist.sonarHit(distance, sonarPose, robotPose))
                for cell in util.lineIndices(sonar_in_robot, hits)[:-1]:
                    maps.clearCell(cell)
            else:
                hits = maps.pointToIndices(sonarDist.sonarHit(distance, sonarPose, robotPose))
                for cell in util.lineIndices(sonar_in_robot, hits)[:-1]:
                    maps.clearCell(cell)
                maps.setCell(hits)
        return (maps, maps)        
 

# For testing your map maker
class SensorInput:
    def __init__(self, sonars, odometry):
        self.sonars = sonars
        self.odometry = odometry

testData = [SensorInput([0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2],
                        util.Pose(1.0, 2.0, 0.0)),
            SensorInput([0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4],
                        util.Pose(4.0, 2.0, -math.pi))]

testClearData = [SensorInput([1.0, 5.0, 5.0, 1.0, 1.0, 5.0, 5.0, 1.0],
                             util.Pose(1.0, 2.0, 0.0)),
                 SensorInput([1.0, 5.0, 5.0, 1.0, 1.0, 5.0, 5.0, 1.0],
                             util.Pose(4.0, 2.0, -math.pi))]

def testMapMaker(data):
    (xMin, xMax, yMin, yMax, gridSquareSize) = (0, 5, 0, 5, 0.1)
    mapper = MapMaker(xMin, xMax, yMin, yMax, gridSquareSize)
    mapper.transduce(data)
    mapper.startState.drawWorld()

def testMapMakerClear(data):
    (xMin, xMax, yMin, yMax, gridSquareSize) = (0, 5, 0, 5, 0.1)
    mapper = MapMaker(xMin, xMax, yMin, yMax, gridSquareSize)
    for i in range(50):
        for j in range(50):
            mapper.startState.setCell((i, j))
    mapper.transduce(data)
    mapper.startState.drawWorld()

def testMapMakerN(n, data):
    (xMin, xMax, yMin, yMax, gridSquareSize) = (0, 5, 0, 5, 0.1)
    mapper = MapMaker(xMin, xMax, yMin, yMax, gridSquareSize)
    mapper.transduce(data*n)
    mapper.startState.drawWorld()

# testClearData = [SensorInput([1.0, 5.0, 5.0, 1.0, 1.0, 5.0, 5.0, 1.0],
#                              util.Pose(1.0, 2.0, 0.0)),
#                  SensorInput([1.0, 5.0, 5.0, 1.0, 1.0, 5.0, 5.0, 1.0],
#                              util.Pose(4.0, 2.0, -math.pi))]
# testMapMaker(testData)

