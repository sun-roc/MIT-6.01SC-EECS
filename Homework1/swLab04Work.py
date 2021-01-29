import lib601.poly as poly
import lib601.sig
from lib601.sig import *

## You can evaluate expressions that use any of the classes or
## functions from the sig module (Signals class, etc.).  You do not
## need to prefix them with "sig."

#持续脉冲函数
s = StepSignal()
#单位脉冲函数
u = UnitSampleSignal()


#第一问
#格式一
s1 = ScaledSignal(s,3)
r1= Rn(s1,3)
step1 = r1
#格式二
#step1 = Rn(ScaledSignal(s,3),3)
#画图查看
#s1.plot(-1,10) 

#第二问
#格式一
s2 = ScaledSignal(s,-3)
r2 = Rn(s2,7)
step2 = r2
#格式二
#step2 = Rn(ScaledSignal(s,-3),7)
#画图检测
#step2.plot(-3,10)

#第三问
stepUpDown = SummedSignal(step1,R(step2))
#画图检测
stepUpDown.plot(0,10)


#第四问
stepUpDownPoly = polyR(u,poly.Polynomial([5,0,3,0,1,0]))
#画图检测
#stepUpDownPoly.plot(0,10)


#打印检测的函数
def samplesInRange(signal,lo,hi):
    return [signal.sample(i) for i in range(lo,hi)]
#print samplesInRange(step2,0,10)
