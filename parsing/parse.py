if __name__ == '__main__':
    import binaryTree as bt
    from tokens import *
else:
    import parsing.binaryTree as bt
    from parsing.tokens import *
import re
from collections import OrderedDict


class Stack:
    def __init__(self, maxx=100):
        self.max = maxx
        self.vals = []

    def pop(self):
        if len(self.vals) > 0: return self.vals.pop()

    def push(self, val):
        if len(self.vals) < self.max: self.vals.append(val)

def tokenize(s):
    phrased = {}
    opened = Stack()
    for i, v in enumerate(s):
        if v == '(':
            opened.push(i)
        elif v == ')':
            start = opened.pop()
            expr = s[start:i+1]
            for i in phrased:
                expr = expr.replace(phrased[i][0], i)

            phrased[f'{{{len(phrased)}}}'] = [expr, len(opened.vals)]

    phrased = OrderedDict(sorted(phrased.items(), key=lambda x: x[1][1], reverse=True))
    return OrderedDict(zip(phrased.keys(), [i[0] for i in phrased.values()]))

def unitize(expr):
    def removeExtraBrackets(s):
        pairs = []
        openB = []
        new = ''
        toRemove = []
        for i, v in enumerate(s):
            if v == '(':
                openB.append(i)
            if v == ')':
                pairs.append([openB.pop(), i])

        for p in pairs:
            if p[0] == 0 and p[1] == len(s)-1:
                toRemove.append(p[0])
                toRemove.append(p[1])
                continue

            between = s[p[0]+1:p[1]]   
            if '+' in between or '*' in between or '¬' in between:
                continue
            toRemove.append(p[0])
            toRemove.append(p[1])

        for i, v in enumerate(s):
            if i not in toRemove:
                new += v

        return new

    new = removeExtraBrackets(expr)
    while expr != new:
        expr = new
        new = removeExtraBrackets(expr)
    
    return new


def hasRedundantBrackets(s):
    chars = []
    for i, ch in enumerate(s):
        if ch == ')':
            top = chars.pop()
            operator = False
            while top != '(':
                if top == '+' or top == '¬' or top == '*':
                    operator = True
                top = chars.pop()
            if not operator:
                return False
        else:
            chars.append(ch)
    return False

def isUnit(s):
    if len(s) == 1:
        return True
    else:
        return False

def findMinimumPriority(s):
    minn = (999,999)
    for i, v in enumerate(s):
        if v in ['¬','*','+']:
            base = 3 if v == '¬' else 2 if v == '*' else 1 if v == '+' else 999
            bracketBonus = 10 * (s[:i].count('(') - s[:i].count(')'))
            prio = base + bracketBonus
            if prio <= minn[0]:
                minn = (prio, i)
    return minn

def addExpr(s, node):
    s = unitize(s)
    if not isUnit(s):
        prio, index = findMinimumPriority(s)
        node.addVal(s[index])

        if s[index] == '¬':
            node.addChild('#')
            # under = re.findall(r'¬([A-Z10])', s[index:]) + re.findall(r'¬\(([A-Z*+¬()10]+)\)[+*]', s[index:]) + re.findall(r'¬\(([A-Z*+¬()10]+)\)(?:$)', s[index:])
            under = unitize(s[index+1:])
            # print(s, s[index], under)
            if not isUnit(under):
                node.addChild(None)
                under = addExpr(under, node.right)
            else:
                node.addChild(under)
        elif s[index] == '*' or s[index] == '+':
            left, right = s[:index], s[index+1:]
            if not isUnit(left):
                node.addChild(None)
                left = addExpr(left, node.left)
            else:
                node.addChild(left)
            if not isUnit(right):
                node.addChild(None)
                right = addExpr(right, node.right)
            else:
                node.addChild(right)
    else:
        node.addVal(s)

def buildTree(s):
    T = bt.BinaryTree()
    addExpr(s, T.root)
    return T
        
def parse(s):

    areNotValid = [i not in validChars for i in s]
    if any(areNotValid):
        raise ValueError
    if len(s) == 1:
        return Expression(Var(s))

    ast = buildTree(f'({s})')
    postfix = ast.traverse(order='pre')
    units = tokenize(postfix)
    for i in units:
        try:
            op, v1, v2 = unitize(units[i]).split(',')
        except ValueError:
            units[i] = units[units[i]]
            if isinstance(units[i], (Not, Expression, Product, Sum)):
                continue
            else:
                op, v1, v2 = unitize(units[i]).split(',')

        if v1 in units:
            v1 = units[v1]
        else:
            v1 = Var(v1)    

        if v2 in units:
            v2 = units[v2]
        else:
            v2 = Var(v2)

        if op == '*':
            units[i] = Product(v1, v2)
        elif op == '+':
            units[i] = Sum(v1, v2)
        elif op == '¬':
            units[i] = Not(v2)

    final = units.popitem()[1]
    final = Expression(final)
    return final

validChars = [chr(i) for i in range(65,91)]
validChars += [chr(i) for i in range(97, 123)]
validChars += ['0', '1']
validChars += ['+', '*', '¬', '(', ')']

# for i in d:
#     print(i[1].getLatex())

# s = '((0+0)*(¬(0)+¬(0)))'
# t = parse(s)