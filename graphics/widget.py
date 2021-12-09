import sys
sys.path.append('C:\\Users\\shrey\\python\\NEA\\graphics')
from graphics.pygameutil import *
import pygame as pg


class Grid:
    def __init__(self, screen, x, y, DIM, bg, lineC):
        self.display = screen
        self.rect = [x, y, DIM[0], DIM[1]]
        self.midpoint = [self.rect[0]+self.rect[2]/2, self.rect[1]+self.rect[3]/2]
        self.smallDim = min(self.rect[2], self.rect[3])
        self.contentSurface = pg.Surface(DIM)
        self.zlayer = 0
        self.scale = 0
        self.makingLine = False
        self.lastCell = None
        self.cells = []
        self.elements = []
        self.updateScale(len(zooms)-1)
        for y in range(-self.halfCellDim[1], self.halfCellDim[1]):
            row = []
            for x in range(-self.halfCellDim[0], self.halfCellDim[0]):
                c = Cell(self, x, y, bg, lineC)
                row.append(c)
            self.cells.append(row)
        self.updateScale(0)
        if isinstance(screen, Screen):
            self.display.addEmbed(self)

    def addElement(self, element):
        self.elements.append(element)

    def updateScale(self, scale):
        self.scale = min(max(scale, 0), len(zooms)-1)
        self.cellW = self.smallDim/(zooms[self.scale]*2)
        self.halfCellDim = [int(self.rect[2]/(self.cellW*2)), int(self.rect[3]/(self.cellW*2))]

    def clear(self):
        pass#self.contentSurface.fill(0)

    def isOver(self):
        x, y = pg.mouse.get_pos()
        if self.rect[0]<=x<=self.rect[0]+self.rect[2]:
            if self.rect[1]<=y<=self.rect[1]+self.rect[3]:
                return True
        return False

    def getOnCell(self):
        x, y = pg.mouse.get_pos()
        nx = (x - self.midpoint[0])//self.cellW
        ny = (y - self.midpoint[1])//self.cellW
        old = self.scale
        self.updateScale(len(zooms)-1)
        nx += self.halfCellDim[0]
        ny += self.halfCellDim[1]
        self.updateScale(old)
        nx = min(max(nx, 0), len(self.cells[0])-1)
        ny = min(max(ny, 0), len(self.cells)-1)
        return self.cells[int(ny)][int(nx)]

    def update(self, event):
        if event.type == pg.KEYDOWN:
            if self.isOver():
                if event.key == pg.K_m:
                    self.updateScale(self.scale-1)
                if self.scale <= len(zooms)-3:
                    if event.key == pg.K_p:
                        self.updateScale(self.scale+1)
                
                onCell = self.getOnCell()
                if event.key == pg.K_n:
                    NotGate(self, onCell.x, onCell.y)
                elif event.key == pg.K_a:
                    AndGate(self, onCell.x, onCell.y)
                elif event.key == pg.K_o:
                    OrGate(self, onCell.x, onCell.y)
                elif event.key == pg.K_s:
                    Switch(self, onCell.x, onCell.y)
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.isOver():    
                if event.button == 1:
                    self.makingLine = True
                    self.lastCell = self.getOnCell()
        if event.type == pg.MOUSEBUTTONUP:
            if self.isOver():    
                if event.button == 1:
                    self.makingLine = False
        if event.type == pg.MOUSEMOTION:
            if self.isOver():
                if self.makingLine: 
                    nc = self.getOnCell()
                    if nc != self.lastCell:
                        d = (nc.x-self.lastCell.x, nc.y-self.lastCell.y)
                        if d in directionIndex.keys():
                            di = directionIndex[d]
                            self.lastCell.setLine(di[0])
                            nc.setLine(di[1])
                            self.lastCell = nc  

        onCell = self.getOnCell()      
        for e in self.elements:
            e.update(event, onCell)       

    def show(self):
        for row in self.cells:
            for u in row:
                if -self.halfCellDim[0]-1<=u.x<=self.halfCellDim[0]+1 and -self.halfCellDim[1]-1<=u.y<=self.halfCellDim[1]+1:
                    u.show()
        for e in self.elements:
            if -self.halfCellDim[0]-1<=e.x<=self.halfCellDim[0]+1 and -self.halfCellDim[1]-1<=e.y<=self.halfCellDim[1]+1:
                e.show()
        self.display.blit(self.contentSurface, (self.rect[0],self.rect[1]))
    

class Cell:
    def __init__(self, grid, x, y, bg, lineC):
        self.grid = grid
        self.x = x
        self.y = y
        self.bg = bg
        self.lineC = lineC
        self.setCol = None
        self.lines = [False, False, False, False] #NESW
        self.lineData = [[0.5, 0], [1, 0.5], [0.5, 1], [0, 0.5]]

    @property
    def drawCoord(self):
        x = self.grid.midpoint[0] + self.x*self.grid.cellW - self.grid.rect[0]
        y = self.grid.midpoint[1] + self.y*self.grid.cellW - self.grid.rect[1]
        return [x, y]

    @property
    def midpoint(self):
        x, y = self.drawCoord
        return x + self.grid.cellW/2, y + self.grid.cellW/2 

    def setLine(self, d):
        self.lines[d] = not self.lines[d]  
    
    def setImage(self, image):
        self.image = image

    def show(self):
        x, y = self.drawCoord
        w, h = self.grid.cellW+1, self.grid.cellW+1
        pg.draw.rect(self.grid.contentSurface, self.bg, (x, y, w, h))
        for i, line in enumerate(self.lines):
            if line:
                start = (self.lineData[i][0]*self.grid.cellW + self.drawCoord[0], self.lineData[i][1]*self.grid.cellW + self.drawCoord[1])
                pg.draw.line(self.grid.contentSurface, (0,0,0), start, self.midpoint)
        pg.draw.circle(self.grid.contentSurface, self.lineC, (x, y), 2)

class Element:
    def __init__(self, grid, x, y, imagePath):
        self.grid = grid
        self.setImage(imagePath)
        self.x = x
        self.y = y
        self.cellDim = [1, 1]
        self.imageSf = 0.8
        self.inputs = []
        self.outputs = []
        self.grid.addElement(self)

    def setImage(self, image):
        self.image = pg.image.load(f'C:\\Users\\shrey\\python\\NEA\\graphics\\{image}.png').convert()
        self.image.set_colorkey((255, 255, 255))
        self.image.set_colorkey((253, 253, 253))

    @property
    def drawCoord(self):
        x = self.grid.midpoint[0] + self.x*self.grid.cellW - self.grid.rect[0]
        y = self.grid.midpoint[1] + self.y*self.grid.cellW - self.grid.rect[1]
        return [x, y]
        
    @property
    def drawImage(self):
        image = pg.transform.smoothscale(self.image, (int(self.grid.cellW*self.cellDim[0]*self.imageSf), int(self.grid.cellW*self.cellDim[1]*self.imageSf)))
        return image

    @property
    def inputR(self):
        return 1/(len(self.inputs)+1)

    @property
    def outputR(self):
        return 1/(len(self.outputs)+1)

    def show(self):
        x, y = self.drawCoord
        off = self.cellDim[0]*(1-self.imageSf)*self.grid.cellW/2
        self.grid.contentSurface.blit(self.drawImage, (x+off, y+off))
        imageRect = self.drawImage.get_rect()
        for ind, i in enumerate(self.inputs):
            i.setRect((x, y+off+self.inputR*imageRect.height*(ind+1) - i.w/2, i.w, i.w))
            pg.draw.rect(self.grid.contentSurface, (255,0,0), i.rect)
        for ind, i in enumerate(self.outputs):
            i.setRect((x+off+imageRect.width - i.w/2, y+off+self.outputR*imageRect.height*(ind+1) - i.w/2, i.w, i.w))
            pg.draw.rect(self.grid.contentSurface, (0,255,255), i.rect)


    def update(self, event, onCell):
        for i in self.inputs:
            i.update(event, self)
        for i in self.outputs:
            i.update(event, self)

class NotGate(Element):
    def __init__(self, grid, x, y):
        super().__init__(grid, x, y, 'not_gate')
        self.inputs = [Node(mode='input') for _ in range(1)]
        self.outputs = [Node(mode='output') for _ in range(1)]

class AndGate(Element):
    def __init__(self, grid, x, y):
        super().__init__(grid, x, y, 'and_gate')
        self.inputs = [Node(mode='input') for _ in range(2)]
        self.outputs = [Node(mode='output') for _ in range(1)]

class OrGate(Element):
    def __init__(self, grid, x, y):
        super().__init__(grid, x, y, 'or_gate')
        self.inputs = [Node(mode='input') for _ in range(2)]
        self.outputs = [Node(mode='output') for _ in range(1)]

class Switch(Element):
    def __init__(self, grid, x, y):
        super().__init__(grid, x, y, 'switch_0')
        self.state = 0
        self.outputs = [Node(mode='output') for _ in range(1)]

    def update(self, event, onCell):
        if event.type == pg.MOUSEBUTTONDOWN:
            if onCell.x == self.x and onCell.y == self.y:
                if event.button == 1:
                    self.state = int(not self.state)
                    self.setImage(f'switch_{self.state}')

class Node:
    def __init__(self, mode=''):
        self.val = 0
        self.w = 10
        self.mode = mode
        self.rect = (0,0,0,0)

    def setVal(self, val):
        self.val = val

    def setRect(self, rect):
        self.rect = rect

    def isOver(self, element):
        x, y = pg.mouse.get_pos()
        x, y = x - element.grid.rect[0], y - element.grid.rect[1]
        if self.rect[0]<=x<=self.rect[0]+self.rect[2]:
            if self.rect[1]<=y<=self.rect[1]+self.rect[3]:
                return True
        return False

    def update(self, event, element):
        if self.isOver(element):
            print('on')


zooms = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,18, 19, 20]
directionIndex = {
    (0,-1): [0, 2],
    (1, 0): [1, 3],
    (0, 1): [2, 0],
    (-1,0): [3, 1]
}