from tokens import *
from parse import *

def display(t):
    print(t, t.terms)

s = '(¬(A*¬(1))+¬(D*B))*B+C*D'

s = parse(s)
s.simplify()