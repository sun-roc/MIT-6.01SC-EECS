import lib601.sf as sf
import lib601.optimize as optimize
import operator

def delayPlusPropModel(k1, k2):
    T = 0.1
    V = 0.1
    
    controller = sf.FeedforwardAdd(sf.Gain(k1),sf.Cascade(sf.R(),sf.Gain(k2)))
    plant1 = sf.Cascade(sf.Gain(T),sf.FeedbackAdd(sf.R()))
    plant2 = sf.Cascade(sf.Gain(V*T),sf.FeedbackAdd(sf.R()))
    sys = sf.FeedbackSubtract(sf.Cascade(sf.Cascade(controller(k),plant1(T)),plant2(T,V)))
    return sys

# You might want to define, and then use this function to find a good
# value for k2.

# Given k1, return the value of k2 for which the system converges most
# quickly, within the range k2Min, k2Max.  Should call optimize.optOverLine.

def bestk2(k1, k2Min, k2Max, numSteps):
    def objective(x):
        return delayPlusPropModel(k1, x).dominantPole()  
    return optimize.optOverLine(objective, k2Min, k2Max, numSteps)

def anglePlusPropModel(k3, k4):
    T = 0.1
    V = 0.1
    plant1 = sf.Cascade(sf.Gain(T),sf.FeedbackAdd(sf.R()))
    plant2 = sf.Cascade(sf.Gain(V*T),sf.FeedbackAdd(sf.R()))
    sys = sf.FeedbackSubtract(sf.Cascade(sf.Cascade(sf.Gain(k3),sf.FeedbackSubtract(plant1,sf.Gain(k4))),plant2))
    return sys


# Given k3, return the value of k4 for which the system converges most
# quickly, within the range k4Min, k4Max.  Should call optimize.optOverLine.

def bestk4(k3, k4Min, k4Max, numSteps):
    def objective(x):
        return anglePlusPropModel(k3, x).dominantPole()  
    return optimize.optOverLine(objective, k4Min, k4Max, numSteps)
