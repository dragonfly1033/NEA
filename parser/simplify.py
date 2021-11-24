from tokens import *
from parse import parse
from laws import *

s = '(C*(C*1+D*A)+B*B)*B+C*1'
obj = parse(s)
obj = Expression(obj)
obj.simplify()