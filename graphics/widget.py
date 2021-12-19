import sys
sys.path.append('C:\\Users\\shrey\\python\\NEA\\graphics')
sys.path.append('C:\\Users\\shrey\\python\\NEA\\parsing')
from graphics import pygameutil as pgu
import pygame as pg
import random as r
from parsing import parse
from parsing.tokens import *



class Grid:
    def __init__(self, screen, x, y, DIM, bg, lineC):
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

        self.scale = 1
        self.updateScale()
        for y in range(self.cellDim[1]):
            row = []
            for x in range(self.cellDim[0]):
                row.append(Cell(self, x, y))
            self.cells.append(row)
        self.scale = self.maxZoom
        self.updateScale()

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
        if self.isOver():
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
                oldscale = self.scale
                oldorigin = self.origin.copy()
                if event.key == pg.K_p:
                    self.scale *= 1.05
                if event.key == pg.K_m:
                    self.scale /= 1.05
                self.scale = min(max(self.scale, 1), self.maxZoom)
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
        c = self.getOnCell()
        if c != None: c.update(event)

    def show(self):
        for row in self.cells:
            for c in row:
                c.show()
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
        self.backreference = None

    def setBackreference(self, other, el):
        self.backreference = other if other != None else self
        self.element = el

    def update(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_q:
                s = f'({self.x}, {self.y}), {None if self.element == None else self.element.IO}'
                print(s)
            if event.key == pg.K_d:
                self.element.clearBackreferences()
                self.element = None
            if self.backreference == None:
                if event.key == pg.K_a:
                    self.element = AndElement(self)
                if event.key == pg.K_o:
                    self.element = OrElement(self)
                if event.key == pg.K_n:
                    self.element = NotElement(self)
                if event.key == pg.K_x:
                    self.element = XorElement(self)
                if event.key == pg.K_s:
                    self.element = SwitchElement(self)
                if event.key == pg.K_b:
                    self.element = BulbElement(self)
        if self.element != None: self.element.update(event)          

    def show(self):
        x = self.grid.cellW * self.x
        y = self.grid.cellW * self.y
        w = h = self.grid.cellW
        # pg.draw.rect(self.grid.contentSurface, self.c, (x, y, w, h), 1)
        pg.draw.circle(self.grid.contentSurface, self.grid.lineC, (x, y), 1)
        if self.element != None: self.element.show()


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
        self.imageSurface.fill(self.cell.grid.lineC)
        l = pgu.Label(self, self.text, (0,0,self.imDim[0],self.imDim[1]), font, (255,0,0), self.cell.grid.bg, align='centre', addSelf=False)
        self.imageSurface.blit(l.label, l.label_rect)
        self.colour = (255,0,0)
        self.inputs = []
        self.outputs = []

        for i in range(self.noOfinputs):
            self.inputs.append(Node(self, 'input', i))  
        for i in range(self.noOfoutputs): 
            self.outputs.append(Node(self, 'output', i))  

        for y in range(self.cellh):
            c1 = self.cell.grid.cells[self.cell.y+y][self.cell.x]   
            c2 = self.cell.grid.cells[self.cell.y+y][self.cell.x+1]
            if y > 0: c1.setBackreference(self.cell, self)
            c2.setBackreference(self.cell, self)

        self.updateOutputs()

    def clearBackreferences(self):
        for y in range(self.cellh):
            c1 = self.cell.grid.cells[self.cell.y+y][self.cell.x]   
            c2 = self.cell.grid.cells[self.cell.y+y][self.cell.x+1]
            if y > 0: c1.setBackreference(None, None)
            c2.setBackreference(None, None)     

    def convert_pos(self, val):
        return ((val/self.scale)-((1-self.scale)/(2*self.scale)))/self.cellh

    def updateOutputs(self):
        pass

    def update(self, event):
        for i in self.inputs:
            i.update(event)
        for i in self.outputs: 
            i.update(event)           

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
        self.center = None
        self.r = 1
        self.colour = (255,0,0) if self.type == 'input' else r.choice(COLOURS)#(r.randint(0,255),r.randint(0,255),r.randint(0,255))
        self.active = 0
        self.v = 0
        self.number = number
        self.backreference = self

    def setBackreference(self, other):
        self.backreference = other

    def setV(self, v):
        self.v = v
        if self.type == 'input':
            print(not self.val)
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

    def isOver(self):
        x, y = pg.mouse.get_pos()
        x, y = x-self.element.cell.grid.rect[0]-self.element.cell.grid.origin[0], y-self.element.cell.grid.rect[1]-self.element.cell.grid.origin[1]
        if self.center[0]-self.r<=x<=self.center[0]+self.r:
            if self.center[1]-self.r<=y<=self.center[1]+self.r:
                return True
        return False

    def update(self, event):
        global CONNECTIONS
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
                            self.element.cell.grid.selected = None

    def show(self):
        if self.type == 'input':    
            self.center = (self.element.drawx + self.element.drawxoff + self.r, self.element.drawy + self.element.cell.grid.cellW*0.5 + self.element.cell.grid.cellW*self.number)
        elif self.type == 'output':    
            self.center = (self.element.drawx + self.element.cell.grid.cellW*self.element.cellw - self.element.drawxoff - self.r, self.element.drawy + self.element.cell.grid.cellW*0.5 + self.element.cell.grid.cellW*self.number)
        colour = (255,0,0) if not self.active or self.colour == None else self.colour
        self.r = 0.8 * self.element.cell.grid.scale
        if type(self.center[0]) != int: 
            pg.draw.circle(self.element.cell.grid.contentSurface, colour, self.center, self.r)
            l = pgu.Label(self, f'{self.val}', (self.center[0]-self.r, self.center[1]-self.r, self.r*2, self.r*2), smallfont, colour, self.element.cell.grid.lineC, align='center', addSelf=False)
            self.element.cell.grid.contentSurface.blit(l.label, l.label_rect)


class NotElement(Element):
    def __init__(self, cell):
        super().__init__(cell, 'Not', 1, 1)

    def updateOutputs(self):
        self.outputs[0].setV(int(not self.inputs[0].val))

class AndElement(Element):
    def __init__(self, cell):
        super().__init__(cell, 'And', 2, 1)

    def updateOutputs(self):
        self.outputs[0].setV(int(self.inputs[0].val and self.inputs[1].val))
        
class OrElement(Element):
    def __init__(self, cell):
        super().__init__(cell, 'Or', 2, 1)

    def updateOutputs(self):
        self.outputs[0].setV(int(self.inputs[0].val or self.inputs[1].val))

class XorElement(Element):
    def __init__(self, cell):
        super().__init__(cell, 'Xor', 2, 1)

    def updateOutputs(self):
        self.outputs[0].setV(int(self.inputs[0].val ^ self.inputs[1].val))
        
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
            if self.isOver():
                self.outputs[0].setV(int(not self.outputs[0].val))

    def updateOutputs(self):
        pass

class BulbElement(Element):
    def __init__(self, cell):
        super().__init__(cell, 'Bulb', 1, 0)

    def updateOutputs(self):
        pass
        

pg.font.init()
font = pg.font.SysFont('Calibri Bold', 64)
smallfont = pg.font.SysFont('Calibri', 12)

from colorsys import hls_to_rgb
COLOURS = []
da = 137.507/360
for i in range(100):
    h = i*da
    l = r.randint(30, 80)/100
    s = r.randint(30, 100)/100
    c = [x*255 for x in hls_to_rgb(h, s, l)]
    COLOURS.append(c)
