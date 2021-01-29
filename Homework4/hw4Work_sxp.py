import operator
import lib601.util as util
import lib601.sig as sig
#-----------------------------------------------------------------------------

class DDist:
    """
    Discrete distribution represented as a dictionary.  Can be
    sparse, in the sense that elements that are not explicitly
    contained in the dictionary are assumed to have zero probability.
    """
    def __init__(self, dictionary):
        self.d = dictionary
        """ Dictionary whose keys are elements of the domain and values
        are their probabilities. """

    def dictCopy(self):
        """
        @returns: A copy of the dictionary for this distribution.
        """
        return self.d.copy()

    def prob(self, elt):
        """
        @param elt: an element of the domain of this distribution
        (does not need to be explicitly represented in the dictionary;
        in fact, for any element not in the dictionary, we return
        probability 0 without error.)
        @returns: the probability associated with C{elt}
        """
        if self.d.has_key(elt):
            return self.d[elt]
        else:
            return 0

    def support(self):
        """
        @returns: A list (in arbitrary order) of the elements of this
        distribution with non-zero probabability.
        """
        return [k for k in self.d.keys() if self.prob(k) > 0]

    def __repr__(self):
        if len(self.d.items()) == 0:
            return "Empty DDist"
        else:
            dictRepr = reduce(operator.add,
                              [util.prettyString(k)+": "+\
                               util.prettyString(p)+", " \
                               for (k, p) in self.d.items()])
            return "DDist(" + dictRepr[:-2] + ")"
    __str__ = __repr__

#-----------------------------------------------------------------------------

def incrDictEntry(d, k, v):
    """
    If dictionary C{d} has key C{k}, then increment C{d[k]} by C{v}.
    Else set C{d[k] = v}.
    
    @param d: dictionary
    @param k: legal dictionary key (doesn't have to be in C{d})
    @param v: numeric value
    """
    if d.has_key(k):
        d[k] += v
    else:
        d[k] = v


#-----------------------------------------------------------------------------

class MixtureDist:
    def __init__(self, d1, d2, p):
        self.d1 = d1.dictCopy()
        self.d2 = d2.dictCopy()
        self.p = float(p)
    def prob(self, elt):

        if self.d1.has_key(elt) and self.d2.has_key(elt):
            return self.d1[elt] * self.p + self.d2[elt] * (1-self.p)
        elif self.d1.has_key(elt):
            return self.d1[elt] * self.p 
        elif self.d2.has_key(elt):
            return self.d2[elt] * (1-self.p)
        else:
            return 0
    def support(self):
        list1 = []
        for k in self.d1.keys() :
            if self.prob(k) > 0 and k not in self.d2.keys() :
                list1.append(k)
        list2 = [k for k in self.d2.keys() if self.prob(k) > 0]
        listlast = list1+list2
        return listlast

    def __str__(self):
        result = 'MixtureDist({'
        elts = self.support()
        for x in elts[:-1]:
            result += str(x) + ' : ' + str(self.prob(x)) + ', '
        result += str(elts[-1]) + ' : ' + str(self.prob(elts[-1])) + '})'
        return result
    
    __repr__ = __str__



def squareDist(lo,hi,loLimit = None,hiLimit = None):
    p = 1.0/(hi-lo)
    maxvalue = max(lo,hi,loLimit,hiLimit)
    mylists = [0]*maxvalue
    dic = {}
    for i in range(lo,hi):
        mylists[i] = p
    if loLimit == None or hiLimit == None :
        pass
    if loLimit != None and loLimit > lo :
        if loLimit > hi:
            return DDist({loLimit : 1})
        else:
            mylists[loLimit] = sum(mylists[0:loLimit+1])
            mylists[0:loLimit] = [0]*loLimit
    if hiLimit != None and hiLimit <hi:
        if hiLimit <lo:
            return DDist({hiLimit: 1})
        else:
            mylists[hiLimit-1] = sum(mylists[hiLimit-1:])
            mylists[hiLimit:] = [0]*len(mylists[hiLimit:])
    for i  in range(0,maxvalue):
        if mylists[i] != 0:
            dic[i] = mylists[i]
    return DDist(dic)

def triangleDist(peak,halfWith,loLimit = None, hilimit = None):
    mylists = [0]*(peak + halfWith)
    
    lower = peak - halfWith +1
    higher = peak + halfWith -1
    for i in range(0,halfWith):
        mylists[peak+i] = float(halfWith-i)/(halfWith*halfWith)
        mylists[peak-i] = float(halfWith-i)/(halfWith*halfWith)
    dic = {}
    if loLimit == None or hilimit == None :
        pass
    if loLimit != None and loLimit > lower :
        if loLimit > higher:
            return DDist({loLimit : 1})
        else:
            mylists[loLimit] = sum(mylists[0:loLimit+1])
            mylists[0:loLimit] = [0]*loLimit
    if hilimit != None and hilimit <higher:
        if hilimit <lower:
            return DDist({hilimit : 1})
        else:
            mylists[hilimit] = sum(mylists[hilimit-1:])
            mylists[hiLimit:] = [0]*len(mylists[hiLimit:])
    for i in range(0,peak + halfWith):
        if mylists[i] != 0:
            dic[i] = mylists[i]
    return DDist(dic)
#print triangleDist(5,3)
#print triangleDist(5,3,6,10)
#print triangleDist(5,3,5,10)
#MixtureDist(squareDist(2,4),squareDist(10,12),0.5)
#MixtureDist(squareDist(2,4),squareDist(10,12),0.9)
#MixtureDist(squareDist(2,6),squareDist(4,8),0.5)



#-----------------------------------------------------------------------------
# If you want to plot your distributions for debugging, put this file
# in a directory that contains lib601, and where that lib601 contains
# sig.pyc.  Uncomment all of the following.  Then you can plot a
# distribution with something like:
# plotIntDist(MixtureDist(squareDist(2, 6), squareDist(4, 8), 0.5), 10)



class IntDistSignal(sig.Signal):
    def __init__(self, d):
        self.dist = d
    def sample(self, n):
        return self.dist.prob(n)
#plotIntDist(MixtureDist(squareDist(2, 6), squareDist(4, 8), 0.5), 10)
