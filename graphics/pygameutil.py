import pygame as pg
from pygame import gfxdraw as ppg #after the tk vs ttk convention
from operator import itemgetter
from math import sin, pi, sqrt
from copy import deepcopy



class Button:
    def __init__(self, screen, text, rect, font, inactiveColour, activeColour, fg, borderColour, func, borderWidth=3, actionButton=False, parent=None, zlayer=0):
        self.display = screen
        self.colours = [inactiveColour, activeColour]
        self.rect = list(rect)
        self.labelRect = [v+(borderWidth*2) if i ==1 else v+(borderWidth*2) if i==0 else v-(borderWidth*4) for i, v in enumerate(self.rect)]
        self.text = text
        self.fg = fg
        self.borderColour = borderColour
        self.borderWidth = borderWidth
        self.func = func
        self.font = font
        self.active = 0
        self.zlayer = zlayer
        if isinstance(screen, (Screen, ScrollableSurface, TransformableSurface)):
            screen.addWidget(self)
            if actionButton:
                screen.actionButton = self
        else:
            parent.addWidget(self)
            if actionButton:
                parent.actionButton = self
        self.show()

    def show(self):
        if isinstance(self.display, (ScrollableSurface, TransformableSurface)):
            display = self.display.contentSurface
        else:
            display = self.display
        pg.draw.rect(display, self.borderColour, self.rect)
        pg.draw.rect(display, self.colours[self.active], (self.rect[0]+self.borderWidth, self.rect[1]+self.borderWidth, self.rect[2]-(2*self.borderWidth), self.rect[3]-(2*self.borderWidth)))
        self.button_text1 = Label(display, self.text, self.labelRect, self.font, self.colours[self.active], self.fg, align='centre', justify='centre', addSelf=False)

    def isOver(self, x, y):
        if self.rect[0]<=x<=self.rect[0]+self.rect[2]:
            if self.rect[1]<=y<=self.rect[1]+self.rect[3]:
                return True
        return False

    def update(self, event):
        x, y = pg.mouse.get_pos()
        if isinstance(self.display, (ScrollableSurface, TransformableSurface)):
            x -= self.display.showRect[0]+self.display.offset[0]
            y -= self.display.showRect[1]+self.display.offset[1]
        over = self.isOver(x, y)
        if event.type == pg.MOUSEMOTION:
            if over:
                self.active = 1
            else:
                self.active = 0
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if over:
                    self.func()
        self.show()


class Input:
    def __init__(self, screen, rect, font, colours, fg, borderColour, borderWidth=3, text='', zlayer=0):
        self.display = screen
        self.rect = list(rect)
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
        if isinstance(screen, (Screen, ScrollableSurface, TransformableSurface)):
            screen.addWidget(self)
        self.show()

    def getTextWidth(self):
        return self.font.size(self.text[self.homeCursorPos:self.endCursorPos+1])[0]

    def isWider(self):
        return self.getTextWidth() > self.rect[2] - (2*self.borderWidth) - self.textOffset

    def show(self):
        if isinstance(self.display, (ScrollableSurface, TransformableSurface)):
            display = self.display.contentSurface
        else:
            display = self.display
        pg.draw.rect(display, self.borderColour, self.rect)
        pg.draw.rect(display, self.colours[self.active], (self.rect[0]+self.borderWidth, self.rect[1]+self.borderWidth, self.rect[2]-(2*self.borderWidth), self.rect[3]-(2*self.borderWidth)))
        self.text_dim = self.textR.get_rect()  
        new_h = (self.rect[3]/2)-(self.text_dim.height/2)+self.rect[1]
        display.blit(self.textR, (self.rect[0]+self.textOffset, new_h))
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


class ImageRect:
    def __init__(self, screen, image, x, y):
        self.display = screen
        self.image = image
        self.x = x
        self.y = y
        self.rect = (self.x, self.y, self.image.get_width(), self.image.get_height())
        self.zlayer = 0
        if isinstance(screen, (ScrollableSurface, Screen)):
            self.display.addWidget(self)

    def show(self):
        if isinstance(self.display, (ScrollableSurface, TransformableSurface)):
            display = self.display.contentSurface
        else:
            display = self.display
        display.blit(self.image, (self.x, self.y))


class Label:
    def __init__(self, screen, text, rect, font, bg, fg, align='left', justify='centre', zlayer=0, addSelf=True, border=False, borderWidth=3, borderColour=(0,0,0)):
        self.display = screen
        self.text = text
        self.font = font
        self.rect = list(rect)
        self.bg = bg
        self.fg = fg
        self.align = align
        self.justify = justify
        self.zlayer = zlayer
        self.border = border 
        self.borderWidth = borderWidth
        self.borderColour = borderColour
        self.update()
        if isinstance(screen, (Screen, ScrollableSurface, TransformableSurface)) and addSelf:
            screen.addWidget(self)

    def show(self):
        if isinstance(self.display, (ScrollableSurface, TransformableSurface)):
            display = self.display.contentSurface
        else:
            display = self.display
        if self.border:
            borderColour = self.borderColour
        else:
            borderColour = self.bg
        pg.draw.rect(display, borderColour, self.rect)
        pg.draw.rect(display, self.bg, (self.rect[0]+self.borderWidth, self.rect[1]+self.borderWidth, self.rect[2]-2*self.borderWidth, self.rect[3]-2*self.borderWidth))
        display.blit(self.label, self.label_rect)

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


class Screen(pg.Surface):
    def __init__(self, DIM):
        super().__init__(DIM)
        self.DIM = DIM
        self.widgets = []
        self.embed = []
        self.actionButton = None
        
    def addWidget(self, widget):
        self.widgets.append(widget)
        self.widgets = sorted(self.widgets, key=lambda x: x.zlayer)

    def addEmbed(self, embed):
        self.embed.append(embed)
        self.embed = sorted(self.embed, key=lambda x: x.zlayer)

    def clear(self):
        self.widgets.clear()

    def event_update(self, event):
        for embed in self.embed:
            embed.update(event)
        for widget in self.widgets:
            if isinstance(widget, (Input, Button)):
                widget.update(event)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                if self.actionButton != None:
                    self.actionButton.func()
    
    def update(self):
        for embed in self.embed:
            embed.clear()

        for widget in self.widgets:
            if isinstance(widget, (Input, Button, ImageRect)):
                widget.show()
            elif isinstance(widget, (Label,)):
                widget.update()

        for embed in self.embed:
            embed.show()


class ScrollableSurface(pg.Surface):
    def __init__(self, screen, x, y, DIM, bg, inactiveColour, activeColour, barWidth=5, padding=10):
        super().__init__(DIM)
        self.display = screen
        self.showRect = (int(x), int(y), int(DIM[0]), int(DIM[1]))
        self.bg = bg
        self.colours = [inactiveColour, activeColour]
        self.zlayer = 0
        self.scrollv = 0.04
        self.widgets = []
        self.contentSurface = pg.Surface(DIM)
        self.padding = padding
        self.excess = [0,0]
        self.offset = [self.padding, self.padding]
        self.barHeight = 0
        self.barw = barWidth
        self.barStart = self.padding
        self.barSnap = 5
        self.barGrab = 0
        self.ratio = 1
        if isinstance(self.display, Screen):
            self.display.addEmbed(self)
    
    @property
    def contentRect(self):
        try:
            minx = min(self.widgets, key=lambda x: x.rect[0]).rect[0]
            miny = min(self.widgets, key=lambda x: x.rect[1]).rect[1]
            maxx = max(self.widgets, key=lambda x: x.rect[0]+x.rect[2])
            maxy = max(self.widgets, key=lambda x: x.rect[1]+x.rect[3])
            maxx = maxx.rect[0]+maxx.rect[2]
            maxy = maxy.rect[1]+maxy.rect[3]

            x = minx + self.showRect[0]
            y = miny + self.showRect[1]
            w = maxx
            h = maxy

            w = min(w, self.showRect[2]-(3*self.padding)-self.barw)

            return (int(x), int(y), int(w), int(h))
        except:
            return self.showRect

    def addWidget(self, other):
        self.widgets.append(other)
        self.display.addWidget(other)
        self.contentSurface = pg.transform.scale(self.contentSurface, (self.contentRect[2], self.contentRect[3]))
        self.excess = [self.contentRect[2] + self.padding - self.showRect[2], self.contentRect[3] + self.padding - self.showRect[3]]
        self.barHeight = (self.showRect[3]**2)//(self.contentRect[3])
        if self.barHeight < 20:
            self.barHeight = 20

    def isOver(self):
        x, y = pg.mouse.get_pos()
        if self.showRect[0]<=x<=self.showRect[0]+self.showRect[2]:
            if self.showRect[1]<=y<=self.showRect[1]+self.showRect[3]:
                return True
        return False

    def clear(self):
        self.fill(self.bg)
        self.contentSurface.fill(self.bg)

    def removeAll(self):
        for i in self.widgets:
            self.display.widgets.remove(i)
        self.widgets.clear()

    def update(self, event):
        keys = pg.key.get_pressed()
        xstrength = 1
        ystrength = 1
        if event.type == pg.MOUSEWHEEL:
            xstrength = abs(event.x)
            ystrength = abs(event.y)
            if xstrength == 0: xstrength = 1
            if ystrength == 0: ystrength = 1

        if event.type == pg.MOUSEBUTTONDOWN:
            if self.isOver():
                if event.button == 4:
                    if keys[pg.K_RCTRL]:
                        self.ratio += self.scrollv * xstrength
                    else:
                        self.ratio += self.scrollv * ystrength
                if event.button == 5:
                    if keys[pg.K_RCTRL]:
                        self.ratio -= self.scrollv * xstrength
                    else:
                        self.ratio -= self.scrollv * ystrength

                self.ratio = min(max(self.ratio, 0), 1)

            if event.button == 1:
                x, y = pg.mouse.get_pos()
                x, y = x - self.showRect[0], y - self.showRect[1]
                if self.bar.width < 7:
                    bx, by = self.bar.x, self.bar.y
                    dx = abs(x-bx)
                    if dx < self.barSnap and by<y<by+self.bar.height:
                        self.barGrab = 1
                else:
                    if self.bar.collidepoint(x, y):
                        self.barGrab = 1
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                if self.barGrab:
                    self.barGrab = 0
        if event.type == pg.MOUSEMOTION:
            if self.barGrab:
                x, y = pg.mouse.get_pos()
                y -= self.showRect[1]
                self.ratio = 1 - (y-(2*self.padding))/(self.showRect[3]-(2*self.padding)-self.barHeight)
                self.ratio = min(max(self.ratio, 0), 1)
                self.show()

    def show(self):
        barx = self.showRect[2]-self.padding-self.barw
        self.offset[1] = (self.ratio) * (self.padding + self.excess[1]) - self.excess[1]
        self.barStart = (1-self.ratio) * (self.showRect[3]-(2*self.padding)-self.barHeight) + self.padding
        self.blit(self.contentSurface, (self.offset[0], self.offset[1]))
        self.bar = pg.draw.rect(self, self.colours[self.barGrab], (barx, self.barStart, self.barw, self.barHeight))
        self.display.blit(self, (self.showRect[0], self.showRect[1]))


class TransformableSurface(pg.Surface):
    def __init__(self, screen, x, y, DIM, bg, zlayer=0, maxScale=10, addSelf=True):
        super().__init__(DIM)
        self.display = screen
        self.showRect = (x, y, DIM[0], DIM[1])
        self.contentSurface = pg.Surface(DIM)
        self.bg = bg
        self.widgets = []
        self.scale = maxScale
        self.maxScale = maxScale
        self.origin = [-self.showRect[2]*(self.scale-1)/2, -self.showRect[3]*(self.scale-1)/2]
        self.zlayer = zlayer
        self.grabbed = False
        if isinstance(screen, Screen) and addSelf:
            self.display.addEmbed(self)

    @property
    def contentRect(self):
        return (0, 0, int(self.showRect[2]*self.scale), int(self.showRect[3]*self.scale))

    def addWidget(self, obj):
        self.display.addWidget(obj)
        self.widgets.append(obj)
        self.contentSurface = pg.transform.scale(self.contentSurface, (self.contentRect[2], self.contentRect[3]))

    def clear(self):
        self.fill(0)
        self.contentSurface.fill(self.bg)

    def removeAll(self):
        for i in self.widgets:
            self.display.widgets.remove(i)
        self.widgets.clear()

    def show(self):
        self.blit(self.contentSurface, self.origin)
        self.display.blit(self, (self.showRect[0], self.showRect[1]))

    def update(self, event):
        global count
        contentRectCopy = self.contentRect
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            x, y = x - self.showRect[0], y - self.showRect[1]
            dz = 0
            if event.button == 1:
                self.grabbed = True
                self.oldpos = pg.mouse.get_pos()
            if event.button == 4:
                dz = 1.05
            if event.button == 5:
                dz = 1/1.05
            
            if dz != 0 and 0<=x-self.origin[0]<=contentRectCopy[2] and 0<=y-self.origin[1]<=contentRectCopy[3]:
                count += 1
                # print(count)
                oldscale = self.scale
                oldorigin = self.origin.copy()
                self.scale *= dz
                self.origin[0] = dz*(self.origin[0]-x) + x
                self.origin[1] = dz*(self.origin[1]-y) + y
                contentRectCopy = self.contentRect
                if  (self.origin[0] > 0 or self.origin[1] > 0 or 
                    self.showRect[0]+self.origin[0]+contentRectCopy[2] < self.showRect[0]+self.showRect[2] or
                    self.showRect[1]+self.origin[1]+contentRectCopy[3] < self.showRect[1]+self.showRect[3] or
                    self.scale > self.maxScale):
                    self.scale = oldscale
                    self.origin = oldorigin
                self.contentSurface = pg.transform.smoothscale(self.contentSurface, (self.contentRect[2], self.contentRect[3]))

        if event.type == pg.MOUSEBUTTONUP:
            if self.grabbed and event.button == 1:
                self.grabbed = False

        if event.type == pg.MOUSEMOTION:
            if self.grabbed:
                x, y = pg.mouse.get_pos()
                dx, dy = x - self.oldpos[0], y - self.oldpos[1]
                oldorigin = self.origin.copy()
                self.oldpos = (x, y)
                self.origin[0] += dx
                self.origin[1] += dy
                print(self.scale, self.showRect[0]+self.origin[0]+contentRectCopy[2], self.showRect[0]+self.showRect[2])
                if  (self.origin[0] > 0 or self.origin[1] > 0 or 
                    self.showRect[0]+self.origin[0]+contentRectCopy[2] < self.showRect[0]+self.showRect[2] or
                    self.showRect[1]+self.origin[1]+contentRectCopy[3] < self.showRect[1]+self.showRect[3]):
                    self.origin = oldorigin

def doNothing():
	pass

def template():
    print(boilerplate)

def boilerPlate():
    print(boilerplate)

count = 0

boilerplate = '''
import pygame as pg
import pygameutil as pgu
       

def mainScreenSetup():
    mainScreen.fill((0, 0, 0))

pg.init()
pg.font.init()

smallFont = pg.font.SysFont('Calibri', 16)
medFont = pg.font.SysFont('Calibri', 24)
largeFont = pg.font.SysFont('Calibri', 36)
vLargeFont = pg.font.SysFont('Calibri', 48)
subtitleFont = pg.font.SysFont('Calibri', 86)
titleFont = pg.font.SysFont('Calibri', 121)

DIM = (1450, 725)

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