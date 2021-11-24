from tokens import *
from parse import *
from laws import *

def display(t):
    print(t, t.terms)

s = '¬(A+B)'
s = 'D*A+(D*B+0*0)*D'
s = parse(s)
s.simplify()
