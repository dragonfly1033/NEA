from tokens import *
from parse import parse
from laws import *

s = '(C*(C*1+D*A)+B*B)*B+C*1'
obj = parse(s)
obj = Expression(obj)
print(f'Original: {obj.rep}')

last = obj.rep
for _ in range(10):
    obj.cluster()
    if last != obj.rep:
        print(f'Associative: {obj.rep}')
        last = obj.rep
    obj.unique()
    if last != obj.rep:
        print(f'Idempotent: {obj.rep}')   
        last = obj.rep
    obj.identities()
    if last != obj.rep:
        print(f'Identity/Null: {obj.rep}')   
        last = obj.rep
