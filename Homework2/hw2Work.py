import lib601.sf as sf
import lib601.sig as sig
import lib601.ts as ts
import lib601.optimize as optimize
# 6.01 HomeWork 2 Skeleton File

#Constants relating to some properties of the motor
k_m = 1000
k_b = 0.5
k_s = 5
r_m = 20

def controllerAndSensorModel(k_c):
    return sf.Gain(k_c*k_s)
    pass #your code here

def integrator(T):
    return sf.Cascade(sf.Gain(T),sf.FeedbackAdd(sf.Gain(1),sf.R()))
    pass #your code here

def motorModel(T):
    return sf.Cascade(sf.Cascade
                      (sf.R(),
                       sf.Gain(float(T*k_m/r_m))),
                       sf.FeedbackSubtract
                       (sf.Gain(1),
                        sf.Cascade(sf.R(),
                                   sf.Gain(float(T*k_m*k_b/r_m)))))
    pass #your code here

def plantModel(T):
    return sf.Cascade(motorModel(T),integrator(T))
    pass #your code here

def lightTrackerModel(T,k_c):
    return sf.FeedbackSubtract(sf.Cascade(controllerAndSensorModel(k_c),
                                          plantModel(T)),sf.Gain(1))
    pass #your code here


def plotOutput(sfModel):
    """Plot the output of the given SF, with a unit-step signal as input"""
    smModel = sfModel.differenceEquation().stateMachine()
    outSig = ts.TransducedSignal(sig.StepSignal(), smModel)
    outSig.plot()

