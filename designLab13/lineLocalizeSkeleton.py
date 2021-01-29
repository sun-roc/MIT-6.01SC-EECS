import lib601.util as util
import lib601.dist as dist
import lib601.distPlot as distPlot
import lib601.sm as sm
import lib601.ssm as ssm
import lib601.sonarDist as sonarDist
import lib601.move as move
import lib601.seGraphics as seGraphics
import lib601.idealReadings as idealReadings

# For testing your preprocessor
class SensorInput:
    def __init__(self, sonars, odometry):
        self.sonars = sonars
        self.odometry = odometry

preProcessTestData = [SensorInput([0.8, 1.0], util.Pose(1.0, 0.5, 0.0)),
                       SensorInput([0.25, 1.2], util.Pose(2.4, 0.5, 0.0)),
                       SensorInput([0.16, 0.2], util.Pose(7.3, 0.5, 0.0))]
testIdealReadings = ( 5, 1, 1, 5, 1, 1, 1, 5, 1, 5 )
testIdealReadings100 = ( 50, 10, 10, 50, 10, 10, 10, 50, 10, 50 )


class PreProcess(sm.SM):
    
    def __init__(self, numObservations, stateWidth):
        self.startState = (None, None)
        self.numObservations = numObservations
        self.stateWidth = stateWidth

    def getNextValues(self, state, inp):
        (lastUpdatePose, lastUpdateSonar) = state
        currentPose = inp.odometry
        currentSonar = idealReadings.discreteSonar(inp.sonars[0],
                                                   self.numObservations)
        # Handle the first step
        if lastUpdatePose == None:
            return ((currentPose, currentSonar), None)
        else:
            action = discreteAction(lastUpdatePose, currentPose,
                                    self.stateWidth)
            print (lastUpdateSonar, action)
            return ((currentPose, currentSonar), (lastUpdateSonar, action))

# Only works when headed to the right
def discreteAction(oldPose, newPose, stateWidth):
    return int(round(oldPose.distance(newPose) / stateWidth))

def makeRobotNavModel(ideal, xMin, xMax, numStates, numObservations):
    
    startDistribution = dist.squareDist(0,numStates)
    def observationModel(ix):
        choose =  int(numObservations *float(1/3))
        trangelwith =  max (2,choose)
        maxsonar = dist.MixtureDist(dist.squareDist(0,numObservations), dist.DeltaDist(numObservations - 1), 0.5)
        return dist.MixtureDist(dist.triangleDist(ideal[ix], trangelwith, 0, numObservations), maxsonar, 0.9)
        

    def transitionModel(a):
        tri_anglewidth = 2
        def getState(s):
            background = dist.squareDist(0,numStates)
            nextvalue = s+a
            nextvalue = min(nextvalue,numStates-1)
            nextvalue = max(nextvalue,0)
            tridist = dist.triangleDist(nextvalue, tri_anglewidth, 0, numStates - 1)
            return dist.MixtureDist(tridist, background, 1 )
        return getState

    return ssm.StochasticSM(startDistribution, transitionModel,
                            observationModel)

def makeLineLocalizer(numObservations, numStates, ideal, xMin, xMax, robotY):

    statewidth = (xMax - xMin) / float(numStates)
    preprocessor = PreProcess(numObservations, statewidth)
    models = makeRobotNavModel(ideal, xMin, xMax, numStates, numObservations)
    estimator = seGraphics.StateEstimator(models)
    driver = move.MoveToFixedPose(util.Pose(xMax, robotY, 0.0), maxVel=0.5)
    return sm.Cascade(sm.Parallel(sm.Cascade(preprocessor, estimator), driver), sm.Select(1))
    
def ppEst(numObservations, numStates, ideal, xMin, xMax):
    statewidth = (xMax - xMin) / float(numStates)
    preprocessor = PreProcess(numObservations, statewidth)
    models = makeRobotNavModel(ideal, xMin, xMax, numStates, numObservations)
    estimator = seGraphics.StateEstimator(models)
    return sm.Cascade(preprocessor, estimator)

    
