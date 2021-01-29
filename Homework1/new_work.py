import pdb
import lib601.sm as sm
import string
import operator
# characters that are single-character tokens
seps = ['(', ')', '+', '-', '*', '/', '=']

class Tokenizer(sm.SM): 
    startState= "none"
    def getNextValues(self, state, inp):
        if state == "none" :
            if inp in seps:
                return (inp,"")
            if inp == " " :
                return ("none","")
            else:
                return (inp,"")
        if state in seps :
            if inp in seps:
                return (inp,state)
            if inp == " ":
                return ("none",state)
            else :
                return(inp,state)
        else:
            if inp == " ":
                return ("none",state)
            if inp in seps :
                return(inp,state)
            else:
                state = state+inp
                return(state,"")
def tokenize(string):
    strings = Tokenizer().transduce(string)
    newstring = []
    for i in strings:
        if i == "":
            pass
        else :
            newstring.append(i)
    return newstring
    
    

# Simple tokenizer tests
'''Answers are:
['fred']
['777']
['777', 'hi', '33']
['*', '*', '-', ')', '(']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
['(', 'hi', '*', 'ho', ')']
['(', 'fred', '+', 'george', ')']
'''
def testTokenize():
    print tokenize('fred ')
    print tokenize('777 ')
    print tokenize('777 hi 33 ')
    print tokenize('**-)( ')
    print tokenize('( hi * ho ) ')
    print tokenize('(fred + george) ')
    print tokenize('(hi*ho) ')
    print tokenize('( fred+george ) ')
testTokenize()
