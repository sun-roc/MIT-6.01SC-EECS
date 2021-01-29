import lib601.sig as sig
import lib601.ts as ts
import lib601.poly as poly
import lib601.sf as sf
k =1
def controller(k):
   return sf.Gain(k)

def plant1(T):
   return sf.Cascade(sf.Gain(T),sf.FeedbackAdd(sf.R()))

def plant2(T, V):
   return sf.Cascade(sf.Gain(V*T),sf.FeedbackAdd(sf.R()))
1
def wallFollowerModel(k, T, V):
   return  sf.FeedbackSubtract( sf.Cascade( sf.Cascade(controller(k),plant1(T)),plant2(T,V)))

print wallFollowerModel(1,0.1,0.1).dominantPole()


