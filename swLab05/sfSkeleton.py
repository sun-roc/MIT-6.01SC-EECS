# -*- coding: GBK -*- 
"""
Class and some supporting functions for representing and manipulating system functions. 
"""

import math
import lib601.poly as poly
import lib601.util as util

class SystemFunction:
    """
    Represent a system function as a ratio of polynomials in R
    """
    #将分子和分母的Polynomial class 传入
    def __init__(self,numeratorPoly,denominatorPoly):
        self.numerator = numeratorPoly
        self.denominator = denominatorPoly
    #对分母取1/z并求根获得极点
    def poles(self):
        t = self.denominator.coeffs[:] #将分母的系数提出来传入一个新的列表当中去
        t.reverse()   #对分母的系数取倒序获得r= 1/z之后的式子的系数
        return poly.Polynomial(t).roots()  #将列表传入Polynomial当中去,并对其求根
    #对极点取绝对值获得极点的幅值
    def poleMagnitudes(self):
        m = []
        for i in self.poles():
            m.append(abs(i))
        return m
    #通过argmax方法将极点传入取绝对值,然后将获得的最大的那个幅值所对应的极点返回
    def dominantPole(self):
        def k(self):
            return abs(self)
        return util.argmax(self.poles(),k)

    def __str__(self):
        return 'SF(' + self.numerator.__str__('R') + \
               '/' + self.denominator.__str__('R') + ')'

    __repr__ = __str__


def Cascade(sf1, sf2):
    pass

def FeedbackSubtract(sf1, sf2=None):
    pass

