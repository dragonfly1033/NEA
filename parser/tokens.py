

class Expression:
    def __init__(self, *args):
        self.terms = list(args)

    @property
    def rep(self):
        return ''.join([i.rep for i in self.terms])[1:-1]

    def cluster(self):
        for term in self.terms:
            if not isinstance(term, (Not, Var)):
                if len(term.terms) == 1:
                    self.terms.remove(term)
                    self.terms += term.terms
                    break

                for subterm in term.terms:
                    if type(subterm) == type(term):
                        term.terms.remove(subterm)
                        term.terms += subterm.terms
                term.cluster()

    def unique(self):
        tmp = []
        for i in self.terms:
            if i not in tmp: tmp.append(i)
            i.unique()
        self.terms = tmp

    def identities(self):
        for i in self.terms:
            if isinstance(i, Product):
                if VAR0 in i.terms:
                    self.terms.remove(i)
                    self.terms.append(VAR0)
                if VAR1 in i.terms:
                    i.terms.remove(VAR1)
            elif isinstance(i, Sum):
                if VAR1 in i.terms:
                    self.terms.remove(i)
                    self.terms.append(VAR1)
                if VAR0 in i.terms:
                    i.terms.remove(VAR0)
            if not isinstance(i, Var): i.identities()

class Product(Expression):
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def rep(self):
        return '*'.join([i.rep for i in self.terms])

class Sum(Expression):
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def rep(self):
        return '(' + '+'.join([i.rep for i in self.terms]) + ')'

class Not:
    def __init__(self, *args):
        self.terms = list(args)

    @property
    def rep(self):
        return f'¬({"".join([i.rep for i in self.terms])})'

    def unique(self):
        tmp = []
        for i in self.terms:
            if i not in tmp: tmp.append(i)
            i.unique()
        self.terms = tmp

class Var:
    def __init__(self, v):
        self.term = v

    def __eq__(self, other):
        if isinstance(other, Var):
            return self.term == other.term
        else:
            return NotImplemented

    @property
    def rep(self):
        return self.term    

    def unique(self):
        pass

VAR0 = Var('0')
VAR1 = Var('1')

