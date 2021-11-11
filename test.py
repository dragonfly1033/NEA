import re

class BinaryTree:
    def __init__(self, rootVal):
        self.root = Node(val=rootVal)

    def traverse(self):
        return self.root.traverse()

class Node:
    def __init__(self, parent=None, val=None):
        self.parent = parent
        self.val = val
        self.left = None
        self.right = None

    def traverse(self):
        if self.val is None:
            return
        if self.left is None:
            return self.val
        val = str(self.left.traverse()) + ',' + str(self.val)
        if self.right is None:
            return val
        val += ',' + str(self.right.traverse())
        return val

def fakePopulate():
    global T

    T = BinaryTree(1)

    T.root.left = Node(val=2)
    T.root.left.left = Node(val=4)
    T.root.left.left.left = Node(val=8)
    T.root.left.left.right = Node(val=9)
    T.root.left.right = Node(val=5)
    T.root.left.right.left = Node(val=10)
    T.root.left.right.right = Node(val=11)

    T.root.right = Node(val=3)
    T.root.right.left = Node(val=6)
    T.root.right.left.left = Node(val=12)
    T.root.right.left.right = Node(val=13)
    T.root.right.right = Node(val=7)
    T.root.right.right.left = Node(val=14)
    T.root.right.right.right = Node(val=15)


def parse(s):
    identity1 = (r'([A-Z])\*1', r'\1')
    identity2 = (r'1\*([A-Z])', r'\1')
    identity3 = (r'([A-Z])\+0', r'\1')
    identity4 = (r'0\+([A-Z])', r'\1')
    null1 = (r'([A-Z])\*0', r'0')
    null2 = (r'0\*([A-Z])', r'0')
    null3 = (r'([A-Z])\+1', r'1')
    null4 = (r'1\+([A-Z])', r'1')
    idempotent1 = (r'([A-Z])\*\1', r'\1')
    idempotent2 = (r'([A-Z])\+\1', r'\1')
    inverse1 = (r'([A-Z])\*\¬\1', r'0')
    inverse2 = (r'\¬([A-Z])\*\1', r'0')
    inverse3 = (r'([A-Z])\+\¬\1', r'1')
    inverse4 = (r'\¬([A-Z])\+\1', r'1')
    absorption1 = (r'([A-Z])\*\(\1\+[A-Z]\)',  r'\1')
    absorption2 = (r'([A-Z])\*\([A-Z]\+\1\)',  r'\1')
    absorption3 = (r'([A-Z])\+\(?\1\*[A-Z]\)?',  r'\1')
    absorption4 = (r'([A-Z])\+\(?[A-Z]\*\1\)?',  r'\1')
    de_morgans1 = (r'\¬\(([A-Z])\*([A-Z])\)',  r'¬\1+¬\2')
    de_morgans2 = (r'\¬\(([A-Z])\+([A-Z])\)',  r'¬\1*¬\2')

    laws = [identity1, identity2, identity3, identity4, null1, null2, null3, null4,
            idempotent1, idempotent2, inverse1, inverse2, inverse3, inverse4,
            absorption1, absorption2, absorption3, absorption4, de_morgans1, de_morgans2]

    for lawReg, lawSub in laws:
        s = re.sub(lawReg, lawSub, s)

    return s

def collectLike(s):
    braGroups = re.compile(r'\((.*)\)')
    braGroups = braGroups.findall((r'\1'.split('+')),s)
    sNoBra = re.sub(r'(\(.*\))','',s)
    print(braGroups)
    #for g in braGroups:
    #    units = g.split('+')
    #    unit = '+'.join(units.sort())

s = '(¬(C*D)+B*C)*D+A*A'

pre = parse(s)
print('pre: ', pre)
new = collectLike(pre)
