import lib601.util as util
import math
sonarMax = 1.5
numObservations = 10
sonarPose0 = util.Pose(0.08,0.134,1.570796)
#test
def wall((x1,y1),(x2,y2)):
    return util.LineSeg(util.Point(x1,y1),util.Point(x2,y2))
wallSegs = [wall((0,2),(8,2)),wall((1,1.25),(1.5,1.25)),wall((2,1.75),(2.8,1.75))]
robotPoses = [util.Pose(0.5, 0.5, 0), util.Pose(1.25, 0.5,0),util.Pose(1.75, 1.0, 0), util.Pose(2.5, 1.0, 0)]
def sonarHit(distance, sonarPose, robotPose):
    return robotPose.transformPoint(sonarPose.transformPoint(util.Point(distance, 0)))
def discreteSonar(sonarReading):
    value = int(sonarReading*numObservations/sonarMax)
    return min(value,numObservations-1)
def idealReadings(wallSegs,robotPoses):
    sonarPose0 = (util.Pose(0.08, 0.134, math.pi / 2))
    statelist = []
    for posestate in robotPoses:
        sonarOriginPoint = sonarHit(0, sonarPose0, posestate)
        sonarline = util.LineSeg(sonarOriginPoint,sonarHit(sonarMax, sonarPose0, posestate))
        hits = [ (seg.intersection(sonarline), seg) for seg in wallSegs ]
        distances = [ sonarOriginPoint.distance(hit) for hit, seg in hits if hit]
        statelist.append(discreteSonar(min(distances)))
    return statelist

