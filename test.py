# 1. Identity, idempotent, union, intersection, double negation
# 2. De Morgans
# 3. associative, commutative
# 4. apply absorbtion
# 5. distributive property

import re


class Law:
    def __init__(self, name, regex, sub):
        self.name = name
        self.regex = regex
        self.sub = sub
        laws.append(self)

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

    for law in laws:
        old = s

        if law.name != 'distributive':
            s = re.sub(law.regex, law.sub, s)
        else:
            m = re.findall(law.regex, s)
            for mm in m:
                print(m)

        if old != s:
            print(f'{law.name}', s)

    return s

def collectLike(s):
    old = s
    braGroups = re.findall(r'\((.*)\)',s)
    sortedGroups = []#'+'.join(i.split('+').sort()) for i in braGroups]
    for g in braGroups:
        sortedGroup = g.split('+')
        sortedGroup.sort()
        sortedGroups.append('+'.join(sortedGroup))

    for i, v in enumerate(sortedGroups):
        s = s.replace(braGroups[i], v)

    if s != old:
        print('commutative: ', s)
    return s



laws = []

absorption01 = Law('absorption', r'\¬([A-Z])\*\(\1\+([A-Z])\)',  r'¬\1*\2') # ¬A(A+B)
absorption02 = Law('absorption', r'\¬([A-Z])\*\(([A-Z])\+\1\)',  r'¬\1*\2') # ¬A(B+A)

absorption03 = Law('absorption', r'([A-Z])\*\(\1\+[A-Z]\)',  r'\1') # A(A+B)
absorption04 = Law('absorption', r'([A-Z])\*\([A-Z]\+\1\)',  r'\1') # A(B+A)

absorption05 = Law('absorption', r'([A-Z])\*\(\¬\1\+([A-Z])\)',  r'\1*\2') # A(¬A+B)
absorption06 = Law('absorption', r'([A-Z])\*\(([A-Z])\+\¬\1\)',  r'\1*\2') # A(B+¬A)

absorption07 = Law('absorption', r'\(([A-Z])\+[A-Z]\)\*\1',  r'\1') # (A+B)A
absorption08 = Law('absorption', r'\([A-Z]\+([A-Z])\)\*\1',  r'\1') # (B+A)A

absorption09 = Law('absorption', r'\(([A-Z])\+([A-Z])\)\*\¬\1',  r'\2*¬\1') # (A+B)¬A
absorption10 = Law('absorption', r'\(([A-Z])\+([A-Z])\)\*\¬\2',  r'\1*¬\2') # (B+A)¬A

absorption11 = Law('absorption', r'\(\¬([A-Z])\+([A-Z])\)\*\1',  r'\2*\1') # (¬A+B)A
absorption12 = Law('absorption', r'\(([A-Z])\+\¬([A-Z])\)\*\2',  r'\2*\1') # (B+¬A)A

absorption13 = Law('absorption', r'\¬([A-Z])\+\(\1\*([A-Z])\)',  r'¬\1+\2') # ¬A+(AB)
absorption14 = Law('absorption', r'\¬([A-Z])\+\(([A-Z])\*\1\)',  r'¬\1+\2') # ¬A+(BA)
absorption15 = Law('absorption', r'\¬([A-Z])\+\1\*([A-Z])',  r'¬\1+\2') # ¬A+AB
absorption16 = Law('absorption', r'\¬([A-Z])\+([A-Z])\*\1',  r'¬\1+\2') # ¬A+BA

absorption17 = Law('absorption', r'([A-Z])\+\(\1\*[A-Z]\)',  r'\1') # A+(AB)
absorption18 = Law('absorption', r'([A-Z])\+\([A-Z]\*\1\)',  r'\1') # A+(BA)
absorption19 = Law('absorption', r'([A-Z])\+\1\*[A-Z]',  r'\1') # A+AB
absorption20 = Law('absorption', r'([A-Z])\+[A-Z]\*\1',  r'\1') # A+BA

absorption21 = Law('absorption', r'([A-Z])\+\(\¬\1\*([A-Z])\)',  r'\1+\2') # A+(¬AB)
absorption22 = Law('absorption', r'([A-Z])\+\(([A-Z])\*\¬\1\)',  r'\1+\2') # A+(B¬A)
absorption23 = Law('absorption', r'([A-Z])\+\¬\1\*([A-Z])',  r'\1+\2') # A+¬AB
absorption24 = Law('absorption', r'([A-Z])\+([A-Z])\*\¬\1',  r'\1+\2') # A+B¬A

absorption25 = Law('absorption', r'\([^¬]([A-Z])\*[A-Z]\)\+\1',  r'\1') # (AB)+A
absorption26 = Law('absorption', r'\([^¬][A-Z]\*([A-Z])\)\+\1',  r'\1') # (BA)+A
absorption27 = Law('absorption', r'[^¬]([A-Z])\*[A-Z]\+\1',  r'\1') # AB+A
absorption28 = Law('absorption', r'[^¬][A-Z]\*([A-Z])\+\1',  r'\1') # BA+A

absorption29 = Law('absorption', r'\(([A-Z])\*([A-Z])\)\+\¬\1',  r'\2+¬\1') # (AB)+¬A
absorption30 = Law('absorption', r'\(([A-Z])\*([A-Z])\)\+\¬\2',  r'\1+¬\2') # (BA)+¬A
absorption31 = Law('absorption', r'([A-Z])\*([A-Z])\+\¬\1',  r'\2+¬\1') # AB+¬A
absorption32 = Law('absorption', r'([A-Z])\*([A-Z])\+\¬\2',  r'\1+¬\2') # BA+¬A

absorption33 = Law('absorption', r'\(\¬([A-Z])\*([A-Z])\)\+\1',  r'\2+\1') # (¬AB)+A
absorption34 = Law('absorption', r'\(([A-Z])\*\¬([A-Z])\)\+\2',  r'\1+\2') # (B¬A)+A
absorption35 = Law('absorption', r'\¬([A-Z])\*([A-Z])\+\1',  r'\2+\1') # ¬AB+A
absorption36 = Law('absorption', r'([A-Z])\*\¬([A-Z])\+\2',  r'\1+\2') # B¬A+A

identity1 = Law('identity', r'([A-Z])\*1', r'\1') # A1
identity2 = Law('identity', r'1\*([A-Z])', r'\1') # 1A
identity3 = Law('identity', r'([A-Z])\+0', r'\1') # A+0
identity4 = Law('identity', r'0\+([A-Z])', r'\1') # 0+A
null1 = Law('null', r'([A-Z])\*0', r'0') # A0
null2 = Law('null', r'0\*([A-Z])', r'0') # 0A
null3 = Law('null', r'([A-Z])\+1', r'1') # A+1
null4 = Law('null', r'1\+([A-Z])', r'1') # 1+A
idempotent1 = Law('idempotent', r'([A-Z])\*\1', r'\1') # AA
idempotent2 = Law('idempotent', r'([A-Z])\+\1', r'\1') # A+A
inverse1 = Law('inverse', r'([A-Z])\*\¬\1', r'0') # A¬A
inverse2 = Law('inverse', r'\¬([A-Z])\*\1', r'0') # ¬AA
inverse3 = Law('inverse', r'([A-Z])\+\¬\1', r'1') # A+¬A
inverse4 = Law('inverse', r'\¬([A-Z])\+\1', r'1') # ¬A+A
de_morgans1 = Law('de morgans', r'\¬\(([A-Z])\*([A-Z])\)',  r'¬\1+¬\2') # ¬(AB)
de_morgans2 = Law('de morgans', r'\¬\(([A-Z])\+([A-Z])\)',  r'¬\1*¬\2') # ¬(A+B)

distributive1 = Law('distributive', r'\(([A-Z\*\¬\+]*)\)\*([A-Z])', r'')
distributive2 = Law('distributive', r'([A-Z])\*\(([A-Z\*\¬\+]*)\)', r'')
distributive3 = Law('distributive', r'\(([A-Z\*\¬\+]*)\)\+([A-Z])', r'')
distributive4 = Law('distributive', r'([A-Z])\+\(([A-Z\*\¬\+]*)\)', r'')

s = '(¬(C*D)+B*C)*D+A*A'

print('original: ', s)
for i in range(10):
    s = parse(s)
    s = collectLike(s)
