
import lib601.dist as dist
import lib601.util as util
import lib601.colors as colors
import lib601.ssm as ssm
import lib601.seFast as seFast
import lib601.dynamicGridMap as dynamicGridMap
falsePos = 0.05
falseNeg = 0.3
initPOcc = 0.3
occThreshold = 0.75

def oGivenS(s):
    if s == 'empty':
        return dist.DDist({'hit': falsePos, 'free': 1 - falsePos})
    return dist.DDist({'hit': 1 - falseNeg, 'free': falseNeg})


def uGivenAS(a):
    return lambda s: dist.DDist({s: 1.0})


cellSSM = ssm.StochasticSM(dist.DDist({'occ': initPOcc, 'empty': 1 - initPOcc}), uGivenAS, oGivenS)

class BayesGridMap(dynamicGridMap.DynamicGridMap):

    def squareColor(self, (xIndex, yIndex)):
        p = self.occProb((xIndex, yIndex))
        if self.robotCanOccupy((xIndex, yIndex)):
            return colors.probToMapColor(p, colors.greenHue)
        if self.occupied((xIndex, yIndex)):
            return 'black'
        return 'red'

    def occProb(self, (xIndex, yIndex)):
        return self.grid[xIndex][yIndex].state.prob('occ')

    def makeStartingGrid(self):

        def makeEstimator(ix, iy):
            m = seFast.StateEstimator(cellSSM)
            m.start()
            return m

        return util.make2DArrayFill(self.xN, self.yN, makeEstimator)

    def setCell(self, (xIndex, yIndex)):
        self.grid[xIndex][yIndex].step(('hit', None))
        self.drawSquare((xIndex, yIndex))
        return

    def clearCell(self, (xIndex, yIndex)):
        self.grid[xIndex][yIndex].step(('free', None))
        self.drawSquare((xIndex, yIndex))
        return

    def occupied(self, (xIndex, yIndex)):
        return self.occProb((xIndex, yIndex)) > occThreshold


