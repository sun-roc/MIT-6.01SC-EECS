import lib601.search as search
import lib601.sm as sm

# Indices into the state tuple.
(farmer, goat, wolf, cabbage) = range(4)
class FarmerGoatWolfCabbage(sm.SM):
    startState = ("L","L","L","L")
    legalInputs = ["takeNone","takeGoat","takeWolf","takeCabbage"]
    def getNextValues(self, state, action):
        if action == "takeNone" :
            if legal(state):
                state = change(state,0)
        if action == "takeGoat":
            state = change(state,0,1)
            print state
        if action == "takeWolf":
            if legal(state):
                state = change(state,0,2)
        if action == "takeCabbage":
            if legal(state):
                state = change(state,0,3)
        return (state,state)
    def done(self, state):
        return state == ('R','R','R','R')
def legal(state):
    if state[wolf] == state[goat] or state[goat] == state[cabbage]:
        return False
    else :
        return True
def change(state,a,b= None):
    state = list(state)
    if b == None :
        state[a] = LR(state[a])
    if b != None :
        if state[a] == state[b]:
            state[a] = LR(state[a])
            state[b] = LR(state[b])
        else:
            pass
    state = tuple(state)
    return state

def LR(c):
    if c == "L":
        return "R"
    else:
        return "L"
print search.smSearch(FarmerGoatWolfCabbage(),depthFirst=False, DP=True)

