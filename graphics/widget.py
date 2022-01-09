from graphics import pygameutil as pgu
import pygame as pg
import random as r
from parsing import parse
from parsing.tokens import *
import math


class Line:
    def __init__(self, node1, node2, c, bc):
        self.node1 = node1
        self.node2 = node2
        self.res = 20
        self.bc = bc
        self.c = c
        self.calcPoints()

    def isOver(self):
        lineOver = []
        x, y = pg.mouse.get_pos()
        x, y = x-self.node1.element.cell.grid.rect[0]-self.node1.element.cell.grid.origin[0], y-self.node1.element.cell.grid.rect[1]-self.node1.element.cell.grid.origin[1]
        for l in range(len(self.ps)-1):
            p1 = self.ps[l]
            p2 = self.ps[l+1]
            d1 = math.sqrt((p1[0]-x)**2 + (p1[1]-y)**2)
            d2 = math.sqrt((p2[0]-x)**2 + (p2[1]-y)**2)
            d3 = math.sqrt((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)
            lineOver.append(-5<d1+d2-d3<5)
        return any(lineOver)

    def destroy(self):
        self.node1.line = None
        self.node2.line = None
        self.node1.element.cell.grid.pathLines.remove(self)
        self.node1.active = False
        self.node2.colour = None

    def update(self, event):
        if event.type == pg.KEYDOWN: 
            if event.key == pg.K_BACKSPACE:
                if self.isOver():
                    self.destroy()

    def calcPoints(self):
        self.p1 = self.node1.center
        self.p4 = self.node2.center
        self.p2 = (0.5*(self.p1[0]+self.p4[0]), self.p1[1])
        self.p3 = (0.5*(self.p1[0]+self.p4[0]), self.p4[1])
        self.ps = []
        t = 0
        for i in range(self.res+1):
            q0 = list(map(lambda x: ((1-t)**3)*x, self.p1))
            q1 = list(map(lambda x: ((1-t)**2)*t*3*x, self.p2))
            q2 = list(map(lambda x: ((1-t)**1)*t*t*3*x, self.p3))
            q3 = list(map(lambda x: t*t*t*x, self.p4))
            nx = q0[0] + q1[0] + q2[0] + q3[0]
            ny = q0[1] + q1[1] + q2[1] + q3[1]
            self.ps.append((nx, ny))

            t += 1/self.res

    def show(self):
        self.calcPoints()
        c = self.c if self.node2.val == 1 else self.bc
        pg.draw.lines(self.node1.element.cell.grid.contentSurface, self.bc, False, self.ps, 5)
        pg.draw.lines(self.node1.element.cell.grid.contentSurface, c, False, self.ps, 3)
        # x, y = pg.mouse.get_pos()
        # x, y = x-self.node1.element.cell.grid.rect[0], y-self.node1.element.cell.grid.rect[1]
        # x, y = x-self.node1.element.cell.grid.origin[0], y-self.node1.element.cell.grid.origin[1]
        # x, y = round(x), round(y)
        # print(self.ps, (x, y))


class Grid:
    def __init__(self, screen, x, y, DIM, bg, lineC, widgetC, nodeC, onC):
        self.display = screen
        self.rect = [x, y, DIM[0], DIM[1]]
        self.minDim = min(self.rect[2:])
        self.bg = bg
        self.lineC = lineC
        self.showSurface = pg.Surface(DIM)
        self.contentSurface = pg.Surface(DIM)
        self.cells = []
        self.isDragging = False
        self.lastoff = [0,0]
        self.maxZoom = 10
        self.minCellDim = 8
        self.zlayer = 0
        self.scale = self.maxZoom
        sf = 0.5*(1-self.scale)
        self.origin = [self.rect[2]*sf, self.rect[3]*sf]
        self.display.addEmbed(self)
        self.minCellW = self.minDim/(self.minCellDim*self.maxZoom)
        self.selected = None
        self.pathLines = []
        self.widgetC = widgetC
        self.nodeC = nodeC
        self.onC = onC
        self.selectedWidget = None
        self.noOfNodes = 0

        self.scale = 1
        self.updateScale()
        for y in range(self.cellDim[1]):
            row = []
            for x in range(self.cellDim[0]):
                row.append(Cell(self, x, y))
            self.cells.append(row)
        self.scale = self.maxZoom
        self.updateScale()

    def clearCells(self):
        for row in self.cells:
            for c in row:
                c.element = None
                c.backreference = c
        self.pathLines.clear()

    def getScreen(self):
        if isinstance(self.display, Screen):
            return self.display
        else:
            return self.display.getScreen()

    def updateScale(self):
        nw = round(self.rect[2] * self.scale)
        nh = round(self.rect[3] * self.scale)
        self.contentSurface = pg.transform.scale(self.contentSurface, (nw, nh))
        self.cellW = round(self.scale*self.minCellW)
        self.cellDim =  [round(self.rect[2]/self.cellW), round(self.rect[3]/self.cellW)]
    
    def clear(self):
        self.showSurface.fill(0)
        self.contentSurface.fill(self.bg)

    def isOver(self):
        x, y = pg.mouse.get_pos()
        if self.rect[0]<=x<=self.rect[0]+self.rect[2]:
            if self.rect[1]<=y<=self.rect[1]+self.rect[3]:
                return True
        return False

    def getOnCell(self):
        x, y = pg.mouse.get_pos()
        x, y = x-self.rect[0]-self.origin[0], y-self.rect[1]-self.origin[1]
        x, y = x/self.cellW, y/self.cellW
        c = self.cells[int(y)][int(x)]
        return c

    def update(self, event):
        ret = False
        updatedBefore = self.display.getScreen().totalUpdates.count(True) > self.display.getScreen().layeredUpdates[self.zlayer].count(True)
        if self.isOver() and not updatedBefore:
            ret = True
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.isDragging = True
                    self.lastoff = pg.mouse.get_pos()

                oldscale = self.scale
                oldorigin = self.origin.copy()
                if event.button == 4:
                    self.scale *= 1.05
                if event.button == 5:
                    self.scale /= 1.05
                self.scale = min(max(self.scale, 5), self.maxZoom)
                if oldscale != self.scale:
                    x, y = pg.mouse.get_pos()
                    dz = self.scale/oldscale
                    self.origin[0] = dz*(self.origin[0] - (x - self.rect[0])) + (x - self.rect[0])
                    self.origin[1] = dz*(self.origin[1] - (y - self.rect[1])) + (y - self.rect[1])
                    self.updateScale()
                    cw, ch = self.contentSurface.get_width(), self.contentSurface.get_height()
                    if not (self.origin[0] <= 0 and self.origin[1] <= 0 and 
                        self.origin[0]+cw >= self.rect[0]+self.rect[2] and
                        self.origin[1]+ch >= self.rect[1]+self.rect[3]
                        ):
                        self.scale = oldscale
                        self.origin = oldorigin.copy()

            if event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    self.isDragging = False
            if event.type == pg.MOUSEMOTION:
                x, y = pg.mouse.get_pos()
                cw, ch = self.contentSurface.get_width(), self.contentSurface.get_height()
                if self.isDragging:
                    x, y = pg.mouse.get_pos()
                    dx, dy = x-self.lastoff[0], y-self.lastoff[1]
                    oldorigin = self.origin.copy()
                    self.origin[0] += dx
                    self.origin[1] += dy
                    self.lastoff = [x, y]
                    if not (self.origin[0] <= 0 and self.origin[1] <= 0 and 
                        self.origin[0]+cw >= self.rect[0]+self.rect[2] and
                        self.origin[1]+ch >= self.rect[1]+self.rect[3]
                        ):
                        self.origin = oldorigin.copy()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.selectedWidget = None

            c = self.getOnCell()
            if c != None: c.update(event)

            for l in self.pathLines:
                l.update(event)
        return ret

    def show(self):
        for i in self.pathLines:
            i.show()
        for row in self.cells:
            for c in row:
                c.show()
        if self.selectedWidget != None:
            x, y = pg.mouse.get_pos()
            x, y = x-self.rect[0]-self.origin[0],y-self.rect[1]-self.origin[1]
            icon = pg.Surface((50,50))
            icon.fill((150,150,150))
            l = pgu.Label(self, self.selectedWidget, (0,0, 50,50), smallFont, (0,255,255), (0,0,0), addSelf=False, align='center')
            icon.blit(l.label, l.label_rect)
            self.contentSurface.blit(icon, (x+10, y+10))
        self.showSurface.blit(self.contentSurface, self.origin)
        self.display.blit(self.showSurface, self.rect[:2])


class Cell:
    def __init__(self, grid, x, y):
        self.grid = grid
        self.x = x
        self.y = y
        self.w = 1
        self.c = self.grid.lineC#(r.randint(0,255),r.randint(0,255),r.randint(0,255))
        self.element = None
        self.backreference = self
        self.last_pos = None

    def __repr__(self):
        return f'({self.x},{self.y})'
    
    def setBackreference(self, other, el):
        self.backreference = other if other != None else self
        self.element = el

    def update(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                print(self, self.backreference, self.element)
            if event.key == pg.K_BACKSPACE:
                if self.element != None:
                    for i in self.element.inputs+self.element.outputs:
                        if i.line != None:
                            i.line.destroy()
                    self.element.clearBackreferences()
                    self.element = None
                    self.grid.selected = None
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.last_pos = pg.mouse.get_pos()
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                nx, ny = pg.mouse.get_pos()
                if self.last_pos != None:    
                    dx, dy = nx-self.last_pos[0], ny-self.last_pos[1]
                else:
                    dx = dy = 0
                if dx < self.grid.cellW/2 and dy < self.grid.cellW/2:
                    if self.element == None:
                        if self.grid.selectedWidget == 'switch':
                            try:
                                self.element = SwitchElement(self)
                            except OverflowError:
                                self.element = None
                        elif self.grid.selectedWidget == 'bulb':
                            try:
                                self.element = BulbElement(self)
                            except OverflowError:
                                self.element = None
                        elif self.grid.selectedWidget == 'and':
                            try:
                                self.element = AndElement(self)
                            except OverflowError:
                                self.element = None
                        elif self.grid.selectedWidget == 'or':
                            try:
                                self.element = OrElement(self)
                            except OverflowError:
                                self.element = None
                        elif self.grid.selectedWidget == 'not':
                            try:
                                self.element = NotElement(self)
                            except OverflowError:
                                self.element = None
                        elif self.grid.selectedWidget == 'xor':
                            try:
                                self.element = XorElement(self)
                            except OverflowError:
                                self.element = None
                        elif self.grid.selectedWidget == 'nor':
                            try:
                                self.element = NorElement(self)
                            except OverflowError:
                                self.element = None
                        elif self.grid.selectedWidget == 'nand':
                            try:
                                self.element = NandElement(self)
                            except OverflowError:
                                self.element = None
        if self.element != None: self.element.update(event)          

    def show(self):
        x = self.grid.cellW * self.x
        y = self.grid.cellW * self.y
        w = h = self.grid.cellW
        pg.draw.circle(self.grid.contentSurface, self.grid.lineC, (x, y), 1)
        if self.element != None and self.backreference == self: self.element.show()


class Element:
    def __init__(self, cell, text, noOfinputs, noOfoutputs):
        self.cell = cell
        self.text = text
        self.cellw = 2
        self.scale = 0.6
        self.nodeR = 8
        self.cellh = max(noOfinputs, noOfoutputs)
        self.noOfoutputs = noOfoutputs
        self.noOfinputs = noOfinputs
        scale = 100
        self.imDim = [self.cellw*scale, self.cellh*scale]
        self.imageSurface = pg.Surface(self.imDim)
        self.makeImage()
        self.colour = (255,0,0)
        self.inputs = []
        self.outputs = []

        for i in range(self.noOfinputs):
            self.inputs.append(Node(self, 'input', i))  
        for i in range(self.noOfoutputs): 
            self.outputs.append(Node(self, 'output', i))  

        self.intersectCells = []
        for y in range(self.cellh):
            c1 = self.cell.grid.cells[self.cell.y+y][self.cell.x]   
            c2 = self.cell.grid.cells[self.cell.y+y][self.cell.x+1]
            self.intersectCells.append(c1)
            self.intersectCells.append(c2)

        self.isEmpty = [i.element == None for i in self.intersectCells]
        if all(self.isEmpty):
            for c in self.intersectCells:
                c.setBackreference(self.cell, self)
        else:
            raise OverflowError

        self.updateOutputs()

    def clearBackreferences(self):
        for c in self.intersectCells:
            c.setBackreference(None, None)    

    def updateOutputs(self):
        rep = self.expr.rep
        for i in range(len(self.inputs)):
            rep = rep.replace(alph[i], str(self.inputs[i].val))
        exp = parse.parse(rep)
        ans = exp.simplify()
        ans = ans[-1][1].terms[0].rep
        self.outputs[0].setV(int(ans))

    def update(self, event):
        for i in self.inputs:
            i.update(event)
        for i in self.outputs: 
            i.update(event)   

    def makeImage(self):
        self.imageSurface.fill(self.cell.grid.widgetC)
        l = pgu.Label(self, self.text, (0,0,self.imDim[0],self.imDim[1]), font, (255,0,0), self.cell.grid.bg, align='centre', addSelf=False)
        self.imageSurface.blit(l.label, l.label_rect)        

    @property
    def IO(self):
        return '('+','.join([i.val for i in self.inputs])+')'+',('+','.join([i.val for i in self.outputs])+')'

    @property
    def drawx(self):
        return self.cell.grid.cellW * self.cell.x  
    
    @property
    def drawy(self):
        return self.cell.grid.cellW * self.cell.y

    @property
    def draww(self):
        return round(self.cell.grid.cellW * (self.cellw - (1-self.scale))) 

    @property
    def drawh(self):
        return round(self.cell.grid.cellW * (self.cellh - (1-self.scale))) 

    @property
    def drawxoff(self):
        return round((self.cell.grid.cellW*(1-self.scale))/2)

    @property
    def drawyoff(self):
        return round((self.cell.grid.cellW*(1-self.scale))/2)

    def show(self):
        image = pg.transform.scale(self.imageSurface, (self.draww, self.drawh))
        self.cell.grid.contentSurface.blit(image, (self.drawx+self.drawxoff, self.drawy+self.drawyoff))
        for i in self.inputs:
            i.show()
        for i in self.outputs:
            i.show()


class Node:
    def __init__(self, element, typee, number):
        self.element = element
        self.type = typee
        self.colour = (255,0,0) if self.type == 'input' else COLOURS[self.element.cell.grid.noOfNodes]#(r.randint(0,255),r.randint(0,255),r.randint(0,255))
        self.active = 0
        self.v = 0
        self.number = number
        self.backreference = self
        self.line = None
        self.element.cell.grid.noOfNodes += 1

    def setBackreference(self, other):
        self.backreference = other

    def setV(self, v):
        self.v = v
        if self.type == 'input':
            self.element.updateOutputs()


    @property
    def val(self):
        if self.type == 'input':
            ret = self.backreference.val if self.backreference != self else self.v
            if ret != self.v:
                self.setV(ret)
        elif self.type == 'output':
            ret = self.v
        return ret

    @property
    def r(self):
        return 0.8 * self.element.cell.grid.scale

    @property
    def center(self):
        if self.type == 'input':    
            ret = (self.element.drawx + self.element.drawxoff + self.r, self.element.drawy + self.element.cell.grid.cellW*0.5 + self.element.cell.grid.cellW*self.number)
        elif self.type == 'output':    
            ret = (self.element.drawx + self.element.cell.grid.cellW*self.element.cellw - self.element.drawxoff - self.r, self.element.drawy + self.element.cell.grid.cellW*0.5 + self.element.cell.grid.cellW*self.number)
        return ret

    def isOver(self):
        x, y = pg.mouse.get_pos()
        x, y = x-self.element.cell.grid.rect[0]-self.element.cell.grid.origin[0], y-self.element.cell.grid.rect[1]-self.element.cell.grid.origin[1]
        if self.center[0]-self.r<=x<=self.center[0]+self.r:
            if self.center[1]-self.r<=y<=self.center[1]+self.r:
                return True
        return False

    def update(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if self.isOver():
                    if self.type == 'output':
                        try:
                            cond = self.element.cell.grid.selected.type != 'output'
                            selfcond = self.element.cell.grid.selected.element == self
                        except AttributeError:
                            cond = True
                            selfcond = False    
                        if cond:
                            if selfcond:
                                self.active = int(not self.active)
                            else:
                                self.active = 1
                            self.element.cell.grid.selected = self
                    elif self.type == 'input':
                        try:
                            cond = self.element.cell.grid.selected.type == 'output'
                        except AttributeError:
                            cond = False    
                        if cond:
                            self.active = int(not self.active)
                            self.colour = self.element.cell.grid.selected.colour
                            self.setBackreference(self.element.cell.grid.selected)
                            self.line = Line(self.element.cell.grid.selected, self, self.colour, self.element.cell.grid.lineC)
                            self.element.cell.grid.selected.line = self.line
                            self.element.cell.grid.pathLines.append(self.line)
                            self.element.cell.grid.selected = None

    def show(self):
        colour = self.element.cell.grid.nodeC if not self.active or self.colour == None else self.colour
        if type(self.center[0]) != int: 
            pg.draw.circle(self.element.cell.grid.contentSurface, colour, self.center, self.r)
            # l = pgu.Label(self, f'{self.val}', (self.center[0]-self.r, self.center[1]-self.r, self.r*2, self.r*2), smallFont, colour, self.element.cell.grid.lineC, align='center', addSelf=False)
            # self.element.cell.grid.contentSurface.blit(l.label, l.label_rect)


class NotElement(Element):
    def __init__(self, cell):
        self.expr = Expression(Not(Var('A')))
        super().__init__(cell, 'Not', 1, 1)

class AndElement(Element):
    def __init__(self, cell):
        self.expr = Expression(Product(Var('A'), Var('B')))
        super().__init__(cell, 'And', 2, 1)
        
class OrElement(Element):
    def __init__(self, cell):
        self.expr = Expression(Sum(Var('A'), Var('B')))
        super().__init__(cell, 'Or', 2, 1)

class XorElement(Element):
    def __init__(self, cell):
        self.expr = Expression(Product(Sum(Var('A'), Var('B')), Sum(Not(Var('A')), Not(Var('B')))))
        super().__init__(cell, 'Xor', 2, 1)

class NorElement(Element):
    def __init__(self, cell):
        self.expr = Expression(Not(Sum(Var('A'), Var('B'))))
        super().__init__(cell, 'Nor', 2, 1)

class NandElement(Element):
    def __init__(self, cell):
        self.expr = Expression(Not(Product(Var('A'), Var('B'))))
        super().__init__(cell, 'Nand', 2, 1)
        
class SwitchElement(Element):
    def __init__(self, cell):
        super().__init__(cell, 'Switch', 0, 1)

    def isOver(self):
        x, y = pg.mouse.get_pos()
        x, y = x-self.cell.grid.rect[0]-self.cell.grid.origin[0], y-self.cell.grid.rect[1]-self.cell.grid.origin[1]
        if self.drawx+self.drawxoff<=x<=self.drawx+self.drawxoff+self.draww:
            if self.drawy+self.drawyoff<=y<=self.drawy+self.drawyoff+self.drawh:
                if not self.outputs[0].isOver():
                    return True
        return False

    def update(self, event):
        super().update(event)
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.isOver() and event.button == 1:
                self.outputs[0].setV(int(not self.outputs[0].val))
                c = self.cell.grid.lineC if not self.outputs[0].val else self.cell.grid.onC
                self.imageSurface.fill(c)
                l = pgu.Label(self, self.text, (0,0,self.imDim[0],self.imDim[1]), font, c, self.cell.grid.bg, align='centre', addSelf=False)
                self.imageSurface.blit(l.label, l.label_rect)

    def updateOutputs(self):
        pass

class BulbElement(Element):
    def __init__(self, cell):
        super().__init__(cell, 'Bulb', 1, 0)

    def updateOutputs(self):
        c = self.cell.grid.lineC if not self.inputs[0].val else self.cell.grid.onC
        self.imageSurface.fill(c)
        l = pgu.Label(self, self.text, (0,0,self.imDim[0],self.imDim[1]), font, c, self.cell.grid.bg, align='centre', addSelf=False)
        self.imageSurface.blit(l.label, l.label_rect)
        

pg.font.init()
font = pg.font.SysFont('Calibri Bold', 64)
smallFont = pg.font.SysFont('Calibri', 12)
vsmallFont = pg.font.SysFont('Calibri', 6)

alph = [chr(i) for i in range(65, 91)]

from colorsys import hls_to_rgb
COLOURS = []
da = 137.507/360
for i in range(100):
    h = i*da
    l = r.randint(30, 80)/100
    s = r.randint(30, 100)/100
    c = [x*255 for x in hls_to_rgb(h, l, s)]
    COLOURS.append(c)

HEIGHTS = {
    AndElement:2,
    OrElement:2,
    NotElement:1,
    NandElement:2,
    NorElement:2,
    SwitchElement:1,
    BulbElement:1,
    XorElement:2
}
