import re

class Law:
    def __init__(self, name, regex, sub):
        self.name = name
        self.regex = regex
        self.sub = sub
        laws.append(self)

class BinaryTree:
    def __init__(self, rootVal=None):
        self.root = Node(val=rootVal)

    def traverse(self):
        return self.root.traverse()

class Stack:
    def __init__(self, maxx=100):
        self.max = maxx
        self.vals = []

    def pop(self):
        if len(self.vals) > 0: return self.vals.pop()

    def push(self, val):
        if len(self.vals) < self.max: self.vals.append(val)


def spl(s):

    opened = Stack()
    sets = []
    for i, v in enumerate(s):
        if v == '(':
            opened.push(i)
        elif v == ')':
            op = opened.pop()
            sets.append((s[op+1:i], len(opened.vals)))
    
    return [i for i, ii in sorted(sets, key=lambda x: x[1], reverse=True)]

import test

s = test.s

s = test.parse(s)
s = spl(s)
print(s)

