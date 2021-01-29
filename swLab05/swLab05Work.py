import lib601.poly as poly
import sfSkeleton as sf
reload(sf)

######################################################################
##  Examples from handout on SystemFunction class
##  You should comment out the parts that you don't want
######################################################################

s1 = sf.SystemFunction(poly.Polynomial([1]),
                       poly.Polynomial([0.63, -1.6, 1]))

print '----------------------------------------'
print 's1:', s1
print 's1.poles():', s1.poles()
print 's1.poleMagnitudes():', s1.poleMagnitudes()
print 's1.dominantPole():', s1.dominantPole()

s2 = sf.SystemFunction(poly.Polynomial([1]),
                       poly.Polynomial([1.1, -1.9, 1]))

print '----------------------------------------'
print 's2:', s2
print 's2.poles():', s2.poles()
print 's2.poleMagnitudes():', s2.poleMagnitudes()
print 's2.dominantPole():', s2.dominantPole()


'''
T = 0.1
k = 2.0
controller = sf.SystemFunction(poly.Polynomial([-k]), poly.Polynomial([1]))
plant = sf.SystemFunction(poly.Polynomial([-T, 0]), poly.Polynomial([-1, 1]))
controllerAndPlant = sf.Cascade(controller, plant)
wire = sf.SystemFunction(poly.Polynomial([1]), poly.Polynomial([1]))
wall = sf.FeedbackSubtract(controllerAndPlant, wire)
print '----------------------------------------'
print 'controller:', controller
print 'plant:', plant
print 'controllerAndPlant:', controllerAndPlant
print 'wall:', wall
print 'wall.poles():', wall.poles()
print '----------------------------------------'
'''

