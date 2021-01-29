import pdb
#import lib601.sm as sm
import string
import operator

class BinaryOp:
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return self.opStr + '(' + \
               str(self.left) + ', ' +\
               str(self.right) + ')'
    __repr__ = __str__

class Sum(BinaryOp):
    opStr = 'Sum'
    def eval(self,env):
        myOP = operator.add
        sum_left = self.left.eval(env)  #函数应当有括号
        sum_right = self.right.eval(env)
        return myOP(sum_left,sum_right)

class Prod(BinaryOp):
    opStr = 'Prod'
    def eval(self,env):
        myOP = operator.div
        sum_left = self.left.eval(env)  #函数应当有括号
        sum_right = self.right.eval(env)
        return myOP(sum_left,sum_right)

class Quot(BinaryOp):
    opStr = 'Quot'
    def eval(self,env):
        myOP = operator.mul
        sum_left = self.left.eval(env)  #函数应当有括号
        sum_right = self.right.eval(env)
        return myOP(sum_left,sum_right)

class Diff(BinaryOp):
    opStr = 'Diff'
    def eval(self,env):
        myOP = operator.sub
        sum_left = self.left.eval(env)  #函数应当有括号
        sum_right = self.right.eval(env)
        return myOP(sum_left,sum_right)

class Assign(BinaryOp):
    opStr = 'Assign'
    def eval(self,env):
        env_name = self.left.name  #将传入变量的name和value提取出来
        env_value = self.right.eval(env)
        env["{0}".format(env_name)] = env_value

class Number:
    def __init__(self, val):
        self.value = val
    def __str__(self):
        return 'Num('+str(self.value)+')'
    __repr__ = __str__
    def eval(self,env):
        return self.value

class Variable:
    def __init__(self, name):
        self.name = name
    def __str__(self):
        return 'Var('+self.name+')'
    __repr__ = __str__
    def eval(self,en):
        return en["{0}".format(self.name)]
# characters that are single-character tokens
seps = ['(', ')', '+', '-', '*', '/', '=']

# Convert strings into a list of tokens (strings)
def tokenize(string):
    data = list(string)
    temporary = [] #中间变量,用于存储合成的单词
    blank_list = []
    judge = 0;
    for i in data:
        if i in seps:
            if judge == 1 :
                blank_list.append("".join(temporary).replace(" ", "")) #列表转字符串并将转换后的空格去掉
                temporary = []
                judge = 0
            blank_list.append(i)
        else:
            if i == " ":
                if "".join(temporary).replace(" ", "") =="":
                    pass
                else:
                    blank_list.append("".join(temporary).replace(" ", ""))
                    temporary = []
                    judge = 0
            else:
                judge = 1;
                temporary.append(i)
    if judge == 1 :
                blank_list.append("".join(temporary).replace(" ", ""))
                judge = 0 #最后再判断一次
    return blank_list

# tokens is a list of tokens
# returns a syntax tree:  an instance of {\tt Number}, {\tt Variable},
# or one of the subclasses of {\tt BinaryOp} 
def parse(tokens):
    def parseExp(index):
        if numberTok(tokens[index]):
            h=tokens[index]
            tokens[index]=float(h)
            tokens[index] = Number(tokens[index])
            return (tokens[index],index+1)
        elif variableTok(tokens[index]):
            tokens[index] = Variable(tokens[index])
            return (tokens[index],index+1)
        else:
            (lef,a)=parseExp(index+1)#反复递归调用,二叉树
            (righ,b)=parseExp(a+1)
            if tokens[a] == "+":
                new_value = Sum(lef,righ)
            if tokens[a] == "-":
                new_value = Diff(lef,righ)
            if tokens[a] == "*":
                new_value = Prod(lef,righ)
            if tokens[a] == "/":
                new_value = Quot(lef,righ)
            if tokens[a] == "=":
                new_value = Assign(lef,righ)
            return (new_value,a+3)
    (parsedExp, nextIndex) = parseExp(0)
    return parsedExp
# token is a string
# returns True if contains only digits
def numberTok(token):
    for char in token:
        if not char in string.digits: return False
    return True

# token is a string
# returns True its first character is a letter
def variableTok(token):
    for char in token:
        if char in string.letters: return True
    return False

# thing is any Python entity
# returns True if it is a number
def isNum(thing):
    return type(thing) == int or type(thing) == float

# Run calculator interactively
def calc():
    env = {}
    while True:
        e = raw_input('%')            # prints %, returns user input
        print '%',e
        print parse(tokenize(e)).eval(env)
        print '   env =', env

# exprs is a list of strings
# runs calculator on those strings, in sequence, using the same environment
def calcTest(exprs):
    env = {}
    for e in exprs:
        print '%', e                    # e is the experession 
        print parse(tokenize(e)).eval(env)
        print '   env =', env
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
    print tokenize('**-)(')
    print tokenize('( hi * ho )')
    print tokenize('(fred + george)')
    print tokenize('(hi*ho)')
    print tokenize('( fred+george )')
#testTokenize()

# Simple parsing tests from the handout
'''Answers are:
Var(a)
Num(888.0)
Sum(Var(fred), Var(george))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Quot(Prod(Var(a), Var(b)), Diff(Var(cee), Var(doh)))
Assign(Var(a), Prod(Num(3.0), Num(5.0)))
'''
def testParse():
    print parse(['a'])
    print parse(['888'])
    print parse(['(', 'fred', '+', 'george', ')'])
    print parse(['(', '(', 'a', '*', 'b', ')', '/', '(', 'cee', '-', 'doh', ')' ,')'])
    print parse(tokenize('((a * b) / (cee - doh))'))
    print parse(tokenize('(a = (3 * 5))'))
#testParse()

####################################################################
# Test cases for EAGER evaluator
####################################################################

def testEval():
    env = {}
    Assign(Variable("a"), Number(5.0)).eval(env)
    print Variable('a').eval(env)
    env['b'] = 2.0
    print Variable('b').eval(env)
    env['c'] = 4.0
    print Variable('c').eval(env)
    print Sum(Variable('a'), Variable('b')).eval(env)
    print Sum(Diff(Variable('a'), Variable('c')), Variable('b')).eval(env)
    Assign(Variable('a'), Sum(Variable('a'), Variable('b'))).eval(env)
    print Variable('a').eval(env)
    print env

# Basic calculator test cases (see handout)
testExprs = ['(2 + 5)',
             '(z = 6)',
             'z',
             '(w = (z + 1))',
             'w'
             ]
#calcTest(testExprs)

####################################################################
# Test cases for LAZY evaluator
####################################################################

# Simple lazy eval test cases from handout
'''Answers are:
Sum(Var(b), Var(c))
Sum(2.0, Var(c))
6.0
'''
def testLazyEval():
    env = {}
    Assign(Variable('a'), Sum(Variable('b'), Variable('c'))).eval(env)
    print Variable('a').eval(env)
    env['b'] = Number(2.0)
    print Variable('a').eval(env)
    env['c'] = Number(4.0)
    print Variable('a').eval(env)

# Lazy partial eval test cases (see handout)
lazyTestExprs = ['(a = (b + c))',
                  '(b = ((d * e) / 2))',
                  'a',
                  '(d = 6)',
                  '(e = 5)',
                  'a',
                  '(c = 9)',
                  'a',
                  '(d = 2)',
                  'a']
# calcTest(lazyTestExprs)

## More test cases (see handout)
partialTestExprs = ['(z = (y + w))',
                    'z',
                    '(y = 2)',
                    'z',
                    '(w = 4)',
                    'z',
                    '(w = 100)',
                    'z']

# calcTest(partialTestExprs)
