import binaryTree as bt
from tokens import *
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

def isUnit(s):
    s = unitize(s)
    if len(s) == 1:
        return True
    if re.match(r'^\{\d+\}$', s):
        return True
    return False

def unitize(s):
    if s[0] == '(' and s[-1] == ')':
        return s[1:-1]
    return s

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
            node.addChild(re.findall(r'¬([A-Za-z0-9\(\)\{\}]*)[\+\*]?', s[index:])[0])
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

    ast = buildTree(f'({s})')

    postfix = ast.traverse(order='pre')
    units = tokenize(postfix)
    for i in units:
        try:
            op, v1, v2 = unitize(units[i]).split(',')
        except ValueError:
            units[i] = units[units[i]]
            #op, v1, v2 = unitize(units[i]).split(',')
            continue
        
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


# 1. De Morgans
# 2. Identity, idempotent, union, intersection, double negation
# 3. associative, commutative
# 4. apply absorbtion
# 5. distributive property

