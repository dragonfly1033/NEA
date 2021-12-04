import sys
sys.path.append('C:\\Users\\shrey\\python\\NEA\\graphics')
from graphics import pygameutil as pgu
import pygame as pg

class Grid(pgu.TransformableSurface):
    def __init__(self, screen, x, y, DIM, bg, lineC, zlayer=0, maxScale=10):
        super().__init__(screen, x, y, DIM, bg, zlayer=0, maxScale=10, addSelf = False)
        self.lineC = lineC
        if isinstance(screen, pgu.Screen):
            self.display.addEmbed(self)

    def clear(self):
        super().clear()
        skip = 1#int(self.maxScale/self.scale)
        gridNo = 20
        gridNo2 = (self.contentRect[2]/self.contentRect[3])*gridNo
        for i in range(0, gridNo, skip):
            y = i*(self.contentRect[3]/gridNo)
            for x in range(0, i+1, skip):
                x = x*(self.contentRect[3]/gridNo)
                pg.draw.circle(self.contentSurface, self.lineC, (x, y), 2)
                if x != y:
                    pg.draw.circle(self.contentSurface, self.lineC, (y, x), 2)
        for i in range(gridNo, gridNo+int(gridNo2), skip):
            y = i*(self.contentRect[3]/gridNo)
            for x in range(0, i+1, skip):
                x = x*(self.contentRect[3]/gridNo)
                pg.draw.circle(self.contentSurface, self.lineC, (x, y), 2)
                if x != y:
                    pg.draw.circle(self.contentSurface, self.lineC, (y, x), 2)


class SubSwitch(pgu.Button):
    def __init__(self, screen, x, y, DIM, bg, inactiveColour, activeColour, borderColour, borderWidth = 3):
        self.display = screen
        self.rect = (x, y, DIM[0], DIM[1])
        self.DIM = DIM
        self.bg = bg
        self.colours = [inactiveColour, activeColour]
        self.borderColour = borderColour
        self.borderWidth = borderWidth
        self.func = self.toggle
        self.state = 0
        self.zlayer = 0
        if isinstance(screen, pgu.Screen):
            self.display.addWidget(self)

    def toggle(self):
        self.state = int(not self.state)

    def show(self):
        pg.draw.rect(self.display, self.borderColour, self.rect)
        pg.draw.rect(self.display, self.bg, (self.rect[0]+self.borderWidth, self.rect[1]+self.borderWidth, self.rect[2]-2*self.borderWidth, self.rect[3]-2*self.borderWidth))
        pg.draw.circle(self.display, self.borderColour, (self.rect[2]/2 + self.rect[0], self.rect[3]/2 + self.rect[1]), min(self.rect[2], self.rect[3])/2.66)
        pg.draw.circle(self.display, self.colours[self.state], (self.rect[2]/2 + self.rect[0], self.rect[3]/2 + self.rect[1]), min(self.rect[2], self.rect[3])/2.66 - self.borderWidth)
