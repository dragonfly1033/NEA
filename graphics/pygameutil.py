import pygame as pg
from pygame import gfxdraw as ppg #after the tk vs ttk convention
from operator import itemgetter
from math import sin, pi, sqrt



class Button:
    def __init__(self, screen, text, rect, font, inactiveColour, activeColour, fg, borderColour, func, borderWidth=3, actionButton=False, parent=None, zlayer=0):
        self.display = screen
        self.colours = [inactiveColour, activeColour]
        self.rect = rect
        self.labelRect = [v+(borderWidth*2) if i ==1 else v+(borderWidth*2) if i==0 else v-(borderWidth*4) for i, v in enumerate(self.rect)]
        self.text = text
        self.fg = fg
        self.borderColour = borderColour
        self.borderWidth = borderWidth
        self.func = func
        self.font = font
        self.active = 0
        self.zlayer = zlayer
        if isinstance(screen, Screen):
            screen.addWidget(self)
            if actionButton:
                screen.actionButton = self
        else:
            parent.addWidget(self)
            if actionButton:
                parent.actionButton = self
        self.show()

    def show(self):
        pg.draw.rect(self.display, self.borderColour, self.rect)
        pg.draw.rect(self.display, self.colours[self.active], (self.rect[0]+self.borderWidth, self.rect[1]+self.borderWidth, self.rect[2]-(2*self.borderWidth), self.rect[3]-(2*self.borderWidth)))
        self.button_text1 = Label(self.display, self.text, self.labelRect, self.font, self.colours[self.active], self.fg, align='centre', justify='centre', addSelf=False)

    def isOver(self, x, y):
        if self.rect[0]<=x<=self.rect[0]+self.rect[2]:
            if self.rect[1]<=y<=self.rect[1]+self.rect[3]:
                return True

        return False

    def update(self, event):
        x, y = pg.mouse.get_pos()
        over = self.isOver(x, y)
        if event.type == pg.MOUSEMOTION:
            old = self.active
            if over:
                self.active = 1
            else:
                self.active = 0
        if event.type == pg.MOUSEBUTTONDOWN:
            if over:
                self.func()
        self.show()


class Input:
    def __init__(self, screen, rect, font, colours, fg, borderColour, borderWidth=3, text='', zlayer=0):
        self.display = screen
        self.rect = rect
        self.active = 0
        self.activated = 0
        self.cursorSpeed = 500
        self.text = text
        self.font = font
        self.colours = colours
        self.fg = fg
        self.borderColour = borderColour
        self.borderWidth = borderWidth
        self.cursorPos = 0
        self.homeCursorPos = 0
        self.endCursorPos = 0
        self.textOffset = 8
        self.charBuffer = 3
        self.textR = self.font.render(self.text, False, self.colours[1])
        self.zlayer = zlayer
        if isinstance(screen, Screen):
            screen.addWidget(self)
        self.show()

    def getTextWidth(self):
        return self.font.size(self.text[self.homeCursorPos:self.endCursorPos+1])[0]

    def isWider(self):
        return self.getTextWidth() > self.rect[2] - (2*self.borderWidth) - self.textOffset

    def show(self):
        pg.draw.rect(self.display, self.borderColour, self.rect)
        pg.draw.rect(self.display, self.colours[self.active], (self.rect[0]+self.borderWidth, self.rect[1]+self.borderWidth, self.rect[2]-(2*self.borderWidth), self.rect[3]-(2*self.borderWidth)))
        self.text_dim = self.textR.get_rect()  
        new_h = (self.rect[3]/2)-(self.text_dim.height/2)+self.rect[1]
        self.display.blit(self.textR, (self.rect[0]+self.textOffset, new_h))
        self.show_cursor()
    
    def show_cursor(self):
        if self.active and sin(pg.time.get_ticks()*pi/self.cursorSpeed) > 0:
            lineHeight = self.font.size('|')[1]
            textWidth = self.font.size(self.text[self.homeCursorPos:self.cursorPos])[0]+self.borderWidth+5
            pg.draw.line(self.display, self.fg, (self.rect[0]+textWidth, self.rect[3]/2 - lineHeight/2 + self.rect[1]), (self.rect[0]+textWidth, self.rect[3]/2 + lineHeight/2 + self.rect[1]))
            self.cursorTime = 0

    def update(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            if self.rect[0]<=x<=self.rect[0]+self.rect[2]:
                if self.rect[1]<=y<=self.rect[1]+self.rect[3]:
                    self.active = 1
                    if self.activated == 0:
                        self.text = ''
                    self.activated += 1
                    self.textR = self.font.render(self.text, True, self.fg)
                else:
                    self.active = 0
            else:
                self.active = 0
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_BACKSPACE:
                    if self.cursorPos != 0:
                        self.text = self.text[:self.cursorPos-1] + self.text[self.cursorPos:]
                        if self.cursorPos < self.homeCursorPos + self.charBuffer:
                            self.cursorPos = self.homeCursorPos + self.charBuffer
                        if self.cursorPos == self.homeCursorPos + self.charBuffer:
                            self.homeCursorPos -= 1
                            self.endCursorPos -= 1
                        self.cursorPos -= 1
                elif event.key == pg.K_DELETE:
                    if self.cursorPos < len(self.text):
                        self.text = self.text[:self.cursorPos] + self.text[self.cursorPos+1:]
                        if self.endCursorPos == len(self.text):
                            self.endCursorPos -= 1
                        while self.isWider():
                            self.endCursorPos -= 1 
                elif event.key == pg.K_HOME:
                    self.endCursorPos -= self.homeCursorPos
                    self.homeCursorPos = 0
                    self.cursorPos = self.homeCursorPos
                    while self.isWider():
                        self.endCursorPos -= 1 
                elif event.key == pg.K_END:
                    diff = len(self.text) - self.endCursorPos
                    self.endCursorPos += diff
                    self.homeCursorPos += diff
                    self.cursorPos = self.endCursorPos
                    while self.isWider():
                        self.homeCursorPos += 1 
                elif event.key == pg.K_LEFT:
                    if self.cursorPos == self.homeCursorPos and self.homeCursorPos > 0:
                        self.homeCursorPos -= 1
                    while self.isWider():
                        self.endCursorPos -= 1              
                    self.cursorPos -= 1
                elif event.key == pg.K_RIGHT:
                    if self.cursorPos == self.endCursorPos and self.endCursorPos < len(self.text):
                        self.endCursorPos += 1
                    while self.isWider():
                        self.homeCursorPos += 1  
                    self.cursorPos += 1
                else:
                    if len(event.unicode) > 0:
                        self.text = self.text[:self.cursorPos] + event.unicode + self.text[self.cursorPos:]
                        self.cursorPos += 1
                        self.endCursorPos += 1
                        while self.isWider():
                            self.homeCursorPos += 1
                

                if self.cursorPos < 0: self.cursorPos = 0
                if self.homeCursorPos < 0: self.homeCursorPos = 0
                if self.endCursorPos < 0: self.endCursorPos = 0
                if self.cursorPos > len(self.text): self.cursorPos = len(self.text)
                if self.homeCursorPos > len(self.text): self.homeCursorPos = len(self.text) 
                if self.endCursorPos > len(self.text): self.endCursorPos = len(self.text) 

                self.textR = self.font.render(self.text[self.homeCursorPos:self.endCursorPos+1], True, self.fg)
                # print(self.homeCursorPos, self.cursorPos, self.endCursorPos, len(self.text))

    
class Label:
    def __init__(self, screen, text, rect, font, bg, fg, align='left', justify='centre', zlayer=0, addSelf=True):
        self.display = screen
        self.text = text
        self.font = font
        self.rect = rect
        self.bg = bg
        self.fg = fg
        self.align = align
        self.justify = justify
        self.zlayer = zlayer
        self.update()
        if isinstance(screen, Screen) and addSelf:
            screen.addWidget(self)

    def show(self):
        pg.draw.rect(self.display, self.bg, self.rect)
        self.display.blit(self.label, self.label_rect)

    def update(self):
        
        self.label = self.font.render(self.text, True, self.fg)
        self.label_rect = self.label.get_rect()

        self.label_rect.x = self.rect[0]
        self.label_rect.y = self.rect[1]

        if self.align == 'right':
            self.label_rect.right = self.rect[0] + self.rect[2]
        elif self.align == 'left':
            self.label_rect.left = self.rect[0]
        elif self.align in ['centre','center']:
            self.label_rect.left = self.rect[0] + ((self.rect[2]/2) - (self.label_rect.width/2))//1
            
        if self.justify == 'top':
            self.label_rect.top = self.rect[1]
        elif self.justify == 'bottom':
            self.label_rect.bottom = self.rect[1] + self.rect[3]
        elif self.justify in ['centre','center']:
            self.label_rect.top = self.rect[1] + ((self.rect[3]/2) - (self.label_rect.height/2))//1

        self.show()

      
class DraggablePoint:
    def __init__(self, screen, x, y, r, inactiveColour, activeColour, zlayer=0):
        self.display = screen
        self.x = x
        self.y = y
        self.r = r
        self.oldx = x
        self.oldy = y
        self.oldr = r
        self.active = 0
        self.colours = [inactiveColour + (255,), activeColour + (255,)]
        self.zlayer = zlayer
        if isinstance(screen, LayeredSurface):
            screen.parent.addWidget(self)

    def show(self):
        if self.oldx != self.x or self.oldy != self.y or self.oldr != self.r:
            pg.draw.circle(self.display, (0,0,0,0), (self.oldx, self.oldy), self.oldr)
        pg.draw.circle(self.display, self.colours[self.active], (self.x, self.y), self.r)

    def isOver(self):
        x, y = pg.mouse.get_pos()
        return sqrt((x-self.x)**2+(y-self.y)**2) <= self.r

    def update(self, event):
        self.oldx = self.x
        self.oldy = self.y
        self.oldr = self.r
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.isOver():
                self.active = 1
                self.r += 2
            else:
                self.active = 0
        if event.type == pg.MOUSEBUTTONUP:
            if self.active:
                self.active = 0
                self.r -= 2
        if event.type == pg.MOUSEMOTION:
            if self.active:
                self.x, self.y = pg.mouse.get_pos()

        self.show()

class DraggableRect:
    def __init__(self, screen, x, y, w, h, inactiveColour, activeColour, zlayer=0):
        self.display = screen
        self.x = x
        self.y = y
        self.dim = [w, h]
        self.oldx = x
        self.oldy = y
        self.oldDim = self.dim
        self.active = 0
        self.colours = [inactiveColour + (255,), activeColour + (255,)]
        self.zlayer = zlayer
        if isinstance(screen, LayeredSurface):
            screen.parent.addWidget(self)

    def show(self):
        if self.oldx != self.x or self.oldy != self.y or self.oldDim != self.dim:
            pg.draw.rect(self.display, (0,0,0,0), (self.oldx, self.oldy, self.oldDim[0], self.oldDim[1]))
        pg.draw.rect(self.display, self.colours[self.active], (self.x, self.y, self.dim[0], self.dim[1]))

    def isOver(self):
        x, y = pg.mouse.get_pos()
        if self.x<=x<=self.x+self.dim[0]:
            if self.y<=y<=self.y+self.dim[1]:
                return True
        return False

    def update(self, event):
        self.oldx = self.x
        self.oldy = self.y
        self.oldDim = self.dim
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.isOver():
                self.active = 1
                self.dim[0] += 2
                self.dim[1] += 2
            else:
                self.active = 0
        if event.type == pg.MOUSEBUTTONUP:
            if self.active:
                self.active = 0
                self.dim[0] -= 2
                self.dim[1] -= 2
        if event.type == pg.MOUSEMOTION:
            x, y = pg.mouse.get_pos()
            if self.active:
                self.x = x - self.dim[0]/2
                self.y = y - self.dim[1]/2
            if self.onDrag != None:
                self.onDrag()
            
        self.show()


class LayeredSurface(pg.Surface):
    def __init__(self, screen, DIM, zlayer=0, *args, **kwargs):
        print(Screen)
        super().__init__(DIM, *args, **kwargs)
        self.zlayer = zlayer
        self.parent = screen
        if isinstance(screen, Screen):
            screen.addWidget(self)
            

class Screen(pg.Surface):
    def __init__(self, DIM):
        super().__init__(DIM)
        self.DIM = DIM
        self.widgets = []
        self.actionButton = None
        
    def addWidget(self, widget):
        self.widgets.append(widget)
        self.widgets = sorted(self.widgets, key=lambda x: x.zlayer)

    def clear(self):
        self.widgets.clear()

    def event_update(self, event):
        rets = []
        for widget in self.widgets:
            if isinstance(widget, (Input, Button, DraggablePoint, DraggableRect)):
                widget.update(event)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                if self.actionButton != None:
                    self.actionButton.func()
    
    def update(self):
        for widget in self.widgets:
            if isinstance(widget, (Input, DraggablePoint, DraggableRect, Button)):
                widget.show()
            elif isinstance(widget, (Label,)):
                widget.update()
            elif isinstance(widget, (LayeredSurface,)):
                self.blit(widget, (0,0))


def doNothing():
	pass

def template():
    print(boilerplate)

def boilerPlate():
    print(boilerplate)



boilerplate = '''
import pygame as pg
import pygameutil as pgu
       

def mainScreenSetup():
    mainScreen.fill((0, 0, 0))

pg.init()
pg.font.init()

smallFont = pg.font.SysFont('Calibri', 12)
medFont = pg.font.SysFont('Calibri', 24)
largeFont = pg.font.SysFont('Calibri', 36)
DIM = (1520, 600)

display = pg.display.set_mode(DIM)
clock = pg.time.Clock()

mainScreen = pgu.Screen(DIM)
mainScreenSetup()

curScreen = mainScreen
run = True
while run:
    display.fill((0,0,0))
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        curScreen.event_update(event)
    curScreen.update()

    clock.tick(60)
    display.blit(curScreen, (0,0))
    pg.display.update()

pg.quit()
quit()
'''