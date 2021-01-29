import lib601.search as search
import lib601.sm as sm

# Indices into the state tuple.
(farmer, goat, wolf, cabbage) = range(4)

class FarmerGoatWolfCabbage(sm.SM):
   startState = None
   legalInputs = None
   def getNextValues(self, state, action):
      pass
   def done(self, state):
      pass
  
