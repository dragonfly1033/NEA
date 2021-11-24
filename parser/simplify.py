from tokens import *
from parse import *
from laws import *

s = '(C*(C*1+D*A)+B*B)*B+C*1'
obj = parse(s)
obj.simplify()