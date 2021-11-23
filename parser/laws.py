import re


class Law:
    def __init__(self, name, regex, sub):
        self.name = name
        self.regex = regex
        self.sub = sub
        laws.append(self)

laws = []

de_morgans1 = Law('de morgans', r'\¬\(([A-Z])\*([A-Z])\)',  r'(¬\1+¬\2)') # ¬(AB)
de_morgans2 = Law('de morgans', r'\¬\(([A-Z])\+([A-Z])\)',  r'(¬\1*¬\2)') # ¬(A+B)
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

# distributive1 = Law('distributive', r'\(([A-Z\*\¬\+]*)\)\*([A-Z])', r'')
# distributive2 = Law('distributive', r'([A-Z])\*\(([A-Z\*\¬\+]*)\)', r'')
# distributive3 = Law('distributive', r'\(([A-Z\*\¬\+]*)\)\+([A-Z])', r'')
# distributive4 = Law('distributive', r'([A-Z])\+\(([A-Z\*\¬\+]*)\)', r'')

def applyLaws(s):
    for law in laws:
        old = s
        s = re.sub(law.regex, law.sub, s)
        if old != s:
            print(f'{law.name}', s)
            break
    return s

# Product([.0.]) = 0
# Sum([.1.]) = 1
# Product([.1.]) = Product([..])
# Sum([.0.]) = Sum([..])
# Product([...]) = Product(unique of [...])
# Sum([...]) = Sum(unique of [...])
# Product(Var, Not(Var)) = 0
# Sum(Var, Not(Var)) = 1
# Product(!Sum) = Product
# Sum(!Product) = Sum
# Not(Sum) = Product(Not)
# Not(Product) = Sum(Not)

# Sum(Var, Product(Var,)) = Var
# Product(Sum,...) => Sum(Product,...)



# 
# for each term in terms:
#   for subterm in term:
#       if term type == subterm type: 
#           remove subterm from term
#           append subterm terms into term
#       
#
#   if term is product:
#       if terms has 0:
#           replace term with 0
#       if term has 1:
#           remove 1    
#   if terms is sum:
#       if term has 1:
#           replace term with 1
#       if term has 0:
#           remove 0
#   unless term is Var: redo these steps for term
# 