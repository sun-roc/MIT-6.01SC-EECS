import lib601.search as search
import lib601.sm as sm

# Indices into the state tuple.
(farmer, goat, wolf, cabbage) = range(4)

class FarmerGoatWolfCabbage(sm.SM):
   startState = ('L','L','L','L')
   legalInputs = ['takeNone','takeGoat','takeWolf','takeCabbage']
   def getNextValues(self, state, action):
      if action == 'takeNone':
         if state[goat] == state[cabbage] or state[goat] == state[wolf]:
            pass
         else :
            state = change(state,farmer)
      if action == 'takeGoat':
         if state[farmer] != state[goat]:
            pass
         else :
            state = change(state,farmer,goat)
      if action == 'takeWolf':
         if state[farmer] != state[wolf] or state[goat] == state[cabbage]:
            pass
         else:
            state = change(state,farmer,wolf)
      if action == 'takeCabbage':
         if state[farmer] != state[cabbage] or state[goat] == state[wolf]:
            pass
         else :
            state = change(state,farmer,cabbage)
      return (state,state)
   def done(self, state):
      return state == ('R','R','R','R')
def change(state,a0,a = None):
   state = list(state)
   if a != None:
      if state[a] == 'L':
         state[a] = 'R'
      else :
         state[a] = 'L'
   if state[a0] == 'L':
      state[a0] = 'R'
   else :
      state[a0] = 'L'
   state = tuple(state)
   return state

print search.smSearch(FarmerGoatWolfCabbage(),depthFirst=False, DP=True)
