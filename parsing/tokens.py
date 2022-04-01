from functools import reduce
from copy import deepcopy
from itertools import product as distributeList


class Expression:
    def __init__(self, *args):
        self.terms = list(args)
        self.oldRep = ""

    def __eq__(self, other):
        if isinstance(other, type(self)):
            return set(self.terms) == set(other.terms)
        return False

    def __hash__(self):
        if len(self.terms) > 1:
            return reduce(lambda i, j: hash(i) ^ hash(j), self.terms)
        else:
            return hash(self.terms[0])

    @property
    def rep(self):
        return "".join([i.rep for i in self.terms])

    def getLatex(self):
        if isinstance(self, Product):
            terms = [i.getLatex() for i in self.terms]
            return "".join(terms)
            # return '%20\\cdot%20'.join(terms)
        elif isinstance(self, Sum):
            terms = [i.getLatex() for i in self.terms]
            return "\\left(" + "+".join(terms) + "\\right)"
        elif isinstance(self, Not):
            term = self.term.getLatex()
            return f"\\overline{{{term}}}"
        elif isinstance(self, Var):
            return self.term
        elif isinstance(self, Expression):
            return self.terms[0].getLatex()

    def typeList(self):
        print(self.terms)
        for term in self.terms:
            if not isinstance(term, Var):
                try:
                    term.typeList()
                except:
                    print(term)

    def __repr__(self):
        if isinstance(self, Sum):
            return f'Sum({", ".join([term.repList() for term in self.terms])})'
        elif isinstance(self, Product):
            return f'Product({", ".join([term.repList() for term in self.terms])})'
        elif isinstance(self, Not):
            return f'Not({", ".join([term.repList() for term in self.terms])})'
        elif isinstance(self, Var):
            return f"Var({self.terms[0]})"
        else:
            return f'Expression({", ".join([term.repList() for term in self.terms])})'

    def getNot(self, obj):
        t = Expression(Not(obj))
        t.involution()
        t = t.terms[0]
        return t

    def unitize(self):
        for term in self.terms:
            if isinstance(term, (Sum, Product)) and len(term.terms) == 1:
                self.terms.remove(term)
                self.terms += term.terms

    def testLaw(self, name, law, printed, last):
        law()
        if last != self:
            # if name != 'Associative': print(f'{name}: {self.rep}')
            # print(f'{name}: {self.rep}')
            out = [name, deepcopy(self)]
            last = deepcopy(self)
            return True, last, out
        return printed, last, None

    def simplify(self):
        self.cluster()
        self.unitize()
        outs = [["Original", deepcopy(self)]]
        last = deepcopy(self)
        printed = True
        while printed:
            printed = False

            printed, last, out = self.testLaw(
                "Associative", self.cluster, printed, last
            )
            if printed:
                outs.append(out)
                continue
            printed, last, out = self.testLaw("Not", self.flip, printed, last)
            if printed:
                outs.append(out)
                continue
            printed, last, out = self.testLaw("Null", self.null, printed, last)
            if printed:
                outs.append(out)
                continue
            printed, last, out = self.testLaw("Identity", self.identity, printed, last)
            if printed:
                outs.append(out)
                continue
            printed, last, out = self.testLaw("Idempotent", self.unique, printed, last)
            if printed:
                outs.append(out)
                continue
            printed, last, out = self.testLaw(
                "Involution", self.involution, printed, last
            )
            if printed:
                outs.append(out)
                continue
            printed, last, out = self.testLaw("Inverse", self.inverse, printed, last)
            if printed:
                outs.append(out)
                continue
            printed, last, out = self.testLaw(
                "De Morgans", self.deMorgans, printed, last
            )
            if printed:
                outs.append(out)
                continue
            printed, last, out = self.testLaw("Absorption", self.absorb, printed, last)
            if printed:
                outs.append(out)
                continue
            printed, last, out = self.testLaw(
                "Distributive", self.distribute, printed, last
            )
            if printed:
                outs.append(out)
                continue
            outs.append(["", deepcopy(self)])
        self.unitize()
        outs[-1][1] = self
        return outs

    def flip(self):
        for term in self.terms:
            if isinstance(term, Not):
                if term.term == VAR0:
                    self.terms.remove(term)
                    self.terms.append(VAR1)
                elif term.term == VAR1:
                    self.terms.remove(term)
                    self.terms.append(VAR0)
            term.unitize()
            if not isinstance(term, Var):
                term.flip()

    def inverse(self):
        for term in self.terms:
            if isinstance(term, Product):
                for pterm in term.terms:
                    notted = self.getNot(pterm)
                    if notted in term.terms:
                        self.terms.remove(term)
                        self.terms.append(VAR0)
                        break
            elif isinstance(term, Sum):
                for pterm in term.terms:
                    notted = self.getNot(pterm)
                    if notted in term.terms:
                        self.terms.remove(term)
                        self.terms.append(VAR1)
                        break
            term.unitize()
            if not isinstance(term, Var):
                term.inverse()

    def involution(self):
        for term in self.terms:
            if isinstance(term, Not):
                if isinstance(term.term, Not):
                    self.terms.remove(term)
                    self.terms.append(term.term.term)
            term.unitize()
            if not isinstance(term, Var):
                term.involution()

    def deMorgans(self):
        for term in self.terms:
            if isinstance(term, Not):
                nterm = term.term
                if isinstance(nterm, Product):
                    self.terms.remove(term)
                    self.terms.append(Sum(*[Not(i) for i in nterm.terms]))
                elif isinstance(nterm, Sum):
                    self.terms.remove(term)
                    self.terms.append(Product(*[Not(i) for i in nterm.terms]))
            term.unitize()
            if not isinstance(term, Var):
                term.deMorgans()

    def cluster(self):
        for term in self.terms:
            if isinstance(term, Sum):
                tmp = term.terms.copy()
                for sterm in term.terms:
                    if isinstance(sterm, Sum):
                        ind = tmp.index(sterm)
                        tmp.remove(sterm)
                        for i in sterm.terms[::-1]:
                            tmp.insert(ind, i)
                term.terms = tmp.copy()
            elif isinstance(term, Product):
                tmp = term.terms.copy()
                for sterm in term.terms:
                    if isinstance(sterm, Product):
                        ind = tmp.index(sterm)
                        tmp.remove(sterm)
                        for i in sterm.terms[::-1]:
                            tmp.insert(ind, i)
                term.terms = tmp.copy()
            term.unitize()
            if not isinstance(term, Var):
                term.cluster()

    def unique(self):
        tmp = []
        for term in self.terms:
            if term not in tmp:
                tmp.append(term)
            term.unitize()
            if not isinstance(term, Var):
                term.unique()
        self.terms = tmp

    def identity(self):
        for term in self.terms:
            if isinstance(term, Product):
                if VAR1 in term.terms and len(term.terms) > 1:
                    term.terms.remove(VAR1)
            elif isinstance(term, Sum):
                if VAR0 in term.terms and len(term.terms) > 1:
                    term.terms.remove(VAR0)

            term.unitize()
            if not isinstance(term, Var):
                term.identity()

    def null(self):
        for term in self.terms:
            if isinstance(term, Product):
                if VAR0 in term.terms:
                    self.terms.remove(term)
                    self.terms.append(VAR0)
            elif isinstance(term, Sum):
                if VAR1 in term.terms:
                    self.terms.remove(term)
                    self.terms.append(VAR1)
            term.unitize()
            if not isinstance(term, Var):
                term.null()

    def absorb(self):
        for term in self.terms:
            if isinstance(term, Sum):
                for sterm in term.terms:
                    if isinstance(sterm, Product):
                        pterms = sterm.terms
                        notPterms = [self.getNot(i) for i in pterms]
                        rest = [i for i in term.terms if i != sterm]
                        for every in rest:
                            compareWith = (
                                every.terms if isinstance(every, Product) else [every]
                            )
                            match = [i for i in pterms if i in compareWith]
                            diff = [i for i in pterms if i not in compareWith]
                            notmatch = [i for i in notPterms if i in compareWith]
                            notdiff = [i for i in notPterms if i not in compareWith]
                            if match == compareWith:
                                self.terms.remove(term)
                                extra = [i for i in rest if i != every]
                                self.terms.append(Sum(Product(*match), *extra))
                                return

                            if notmatch == compareWith:
                                self.terms.remove(term)
                                extra = [i for i in rest if i != every]
                                self.terms.append(Sum(*notmatch, *diff, *extra))
                                return

            term.unitize()
            if not isinstance(term, Var):
                term.absorb()

    def distribute(self):
        for term in self.terms:
            if isinstance(term, Product):
                lov = []
                sums = 0
                for pterm in term.terms:
                    if isinstance(pterm, Sum):
                        lov.append(pterm.terms)
                        sums += 1
                    else:
                        lov.append([pterm])
                if sums > 0:
                    prod = list(distributeList(*lov))
                    fin = Sum(*[Product(*i) for i in prod])
                    self.terms.remove(term)
                    self.terms.append(fin)
            term.unitize()
            if not isinstance(term, Var):
                term.distribute()


class Product(Expression):
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def rep(self):
        return "(" + "*".join([i.rep for i in self.terms]) + ")"


class Sum(Expression):
    def __init__(self, *args):
        super().__init__(*args)

    @property
    def rep(self):
        return "(" + "+".join([i.rep for i in self.terms]) + ")"


class Not(Expression):
    def __init__(self, *args):
        super().__init__(*args)
        if len(self.terms) > 1:
            raise ValueError(f"Not object has too many terms: {self.terms}")

    @property
    def rep(self):
        return f'¬({"".join([i.rep for i in self.terms])})'

    @property
    def term(self):
        return self.terms[0]


class Var(Expression):
    def __init__(self, *args):
        super().__init__(*args)
        if len(self.terms) > 1:
            raise ValueError(f"Var object has too many terms: {self.terms}")

    @property
    def rep(self):
        return self.term

    @property
    def term(self):
        return self.terms[0]


VAR0 = Var("0")
VAR1 = Var("1")
