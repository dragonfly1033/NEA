
class Product:
    def __init__(self, *args):
        self.terms = list(args)

    def cluster(self):
        while True:
            old = [type(i) for i in self.terms]
            for i, t in enumerate(self.terms):
                if isinstance(t, Product):
                    self.terms.remove(t)
                    for n in t.terms:
                        self.terms.append(n)
                elif isinstance(t, Sum):
                    t.cluster()
            if old == [type(i) for i in self.terms]:
                break

    def show(self):
        return '(' + '*'.join([i.show() for i in self.terms]) + ')'

class Sum:
    def __init__(self, *args):
        self.terms = list(args)

    def cluster(self):
        while True:
            old = [type(i) for i in self.terms]
            for i, t in enumerate(self.terms):
                if isinstance(t, Sum):
                    self.terms.remove(t)
                    for n in t.terms:
                        self.terms.append(n)
                elif isinstance(t, Product):
                    t.cluster()
            if old == [type(i) for i in self.terms]:
                break

    def show(self):
        return '(' + '+'.join([i.show() for i in self.terms]) + ')'

class Not:
    def __init__(self, *args):
        self.terms = args

    def show(self):
        return f'¬({"".join([i.show() for i in self.terms])})'

class Var:
    def __init__(self, v):
        self.term = v

    def show(self):
        return self.term

class Expression:
    def __init__(self, expr):
        self.expr = expr

