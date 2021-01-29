"""
Signals, represented implicitly, with plotting and combinations.
"""

import pickle
import math
import lib601.util as util

import lib601.gw as gw

# define size of graphing window 
# graphwidth = 400 # old value
graphwidth = 570
graphheight = 300

# NOTE: Ideally, graphwidth should be tuned to the number of samples in such a way
# that samples are an integer number of pixels apart on the screen.
# 570 seems to be just right for 250 samples (1000 steps and subsample 4).
# Samples are two pixels apart and there is space on the left for caption.
# Adjusting window width to get integer pixel spacing has now been
# automated in __init__ method of class GraphCanvas of gw.py

class Signal:
    """
    Represent infinite signals.  This is a generic superclass that
    provides some basic operations.  Every subclass must provide a
    C{sample} method.

    Be sure to start idle with the C{-n} flag, if you want to make
    plots of signals from inside idle.
    """
    
    __w = None
    """ Currently active plotting window.  Not for users."""

    def plot(self, start = 0, end = 100, newWindow = 'Signal value versus time',
             color = 'blue', parent = None, ps = None,
             xminlabel = 0, xmaxlabel = 0,
             yOrigin = None): # bkph
        """
        Make a plot of this signal.
        @param start: first value to plot; defaults to 0
        @param end: last value to plot; defaults to 100; must be > start
        @param newWindow: makes a new window with this value as title,
        unless the value is False, in which case it plots the signal
        in the currently active plotting window
        @param color: string specifying color of plot; all simple
        color names work
        @param parent: An instance of C{tk.tk}.  You probably should
        just leave this at the default unless you're making plots
        from another application.
        @param ps: If not C{None}, then it should be a pathname;
             we'll write a postscript version of this graph to that path.
        """
        samples = [self.sample(i) for i in range(start, end)]
        if len(samples) == 0:
            raise Exception, 'Plot range is empty'
        if yOrigin == None:
            minY = min(samples)
        else:
            minY = yOrigin
        maxY = max(samples)
        if maxY == minY:
            margin = 1.0
        else:
#           margin = (maxY - minY) * 0.05
            margin = 0 # override bkph
        
        if newWindow == True or newWindow == False:
            title = 'Signal value vs time'
        else:
            title = newWindow
            
        if parent:
            # Make a window under a different tk parent
            w = gw.GraphingWindow(\
                     graphwidth, graphheight, start, end,
                     minY-margin, maxY+margin, title, parent,
                     xminlabel = xminlabel, xmaxlabel = xmaxlabel) # bkph
        else:
            # Use this class's tk instance
            if  newWindow or Signal.__w == None:
                Signal.__w = gw.GraphingWindow(\
                     graphwidth, graphheight, start, end,
                     minY-margin, maxY+margin, title,
                     xminlabel = xminlabel, xmaxlabel = xmaxlabel) # bkph
            w = Signal.__w
            
        w.graphDiscrete(lambda n: samples[n - start], color)
        if ps:
            w.postscript(ps)

    def __add__(self, other):
        """
        @param other: C{Signal}
        @return: New signal that is the sum of C{self} and C{other}.
        
        Does not modify either argument.
        """
        return SummedSignal(self, other)
    
    def __rmul__(self, scalar):
        """
        @param scalar: number
        @return: New signal that is C{self} scaled by a constant.
        
        Does not modify C{self}
        """
        return ScaledSignal(self, scalar)

    def __mul__(self, scalar):
        """
        @param scalar: number
        @return: New signal that is C{self} scaled by a constant.
        
        Does not modify C{self}
        """
        return ScaledSignal(self, scalar)

    def period(self, n = None, z = None):
        """
        @param n: number of samples to use to estimate the period;  if
        not provided, it will look for a C{length} attribute of C{self}
        @param z: zero value to use when looking for zero-crossings of
        the signal;  will use the mean by default.
        @return: an estimate of the period of the signal, or
        'aperiodic' if it can't get a good estimate
        """
        if n == None:
            n = self.length
        crossingsD = self.crossings(n, z)
        if len(crossingsD) < 2:
            return 'aperiodic'
        else:
            return listMean(gaps(crossingsD))*2

    def crossings(self, n = None, z = None):
        """
        @param n: number of samples to use;  if
        not provided, it will look for a C{length} attribute of C{self}
        @param z: zero value to use when looking for zero-crossings of
        the signal;  will use the mean by default.
        @return: a list of indices into the data where the signal crosses the
        z value, up through time n
        """
        if n == None: n = self.length
        if z == None: z = self.mean(n)
        samples = self.samplesInRange(0, n)
        return [i for i in range(n-1) if \
                   samples[i] > z and samples[i+1] < z or\
                   samples[i] < z and samples[i+1] > z]

    def mean(self, n = None):
        """
        @param n: number of samples to use to estimate the mean;  if
        not provided, it will look for a C{length} attribute of C{self}
        @return: sample mean of the values of the signal from 0 to n
        """
        if n == None: n = self.length
        return listMean(self.samplesInRange(0, n))

    def samplesInRange(self, lo, hi):
        """
        @return: list of samples of this signal, from C{lo} to C{hi-1}
        """
        return [self.sample(i) for i in range(lo, hi)]    
    

class CosineSignal(Signal):
    """
    Primitive family of sinusoidal signals.
    """
    def __init__(self, omega = 1, phase = 0):
        """
        @parameter omega: frequency
        @parameter phase: phase in radians
        """
        self.omega = omega
        self.phase = phase
    def sample(self, n):
        return math.cos(self.omega * n + self.phase)
    def __str__(self):
        return 'CosineSignal(omega=%f,phase=%f)'%(self.omega, self.phase)

class UnitSampleSignal(Signal):
    """
    Primitive unit sample signal has value 1 at time 0 and value 0
    elsewhere.
    """
    def sample(self, n):
        if n == 0:
            return 1
        else:
            return 0
    def __str__(self):
        return 'UnitSampleSignal'

us = UnitSampleSignal()
"""Unit sample signal instance"""

class ConstantSignal(Signal):
    """
    Primitive constant sample signal.
    """
    def __init__(self, c):
        """
        param c: value of signal at all times
        """
        self.c = c
    def sample(self, n):
        return self.c
    def __str__(self):
        return 'ConstantSignal(%f)'%(self.c)

################
# Your code here
################

