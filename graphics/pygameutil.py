import pygame as pg
from pygame import gfxdraw as ppg #after the tk vs ttk convention
from operator import itemgetter
from math import sin, pi, sqrt
from collections import OrderedDict
from random import randint



class Button:
    def __init__(self, screen, text, rect, font, inactiveColour, activeColour, fg, borderColour, func, borderWidth=3, actionButton=False, parent=None, zlayer=0):
        self.display = screen
        self.colours = [inactiveColour, activeColour]
        self.rect = list(rect)
        self.labelRect = [self.rect[0]+(borderWidth*2), self.rect[1]+(borderWidth*2), self.rect[2]-(borderWidth*4), self.rect[3]-(borderWidth*4)]
        self.text = text
        self.fg = fg
        self.borderColour = borderColour
        self.borderWidth = borderWidth
        self.func = func
        self.font = font
        self.active = 0
        self.zlayer = zlayer
        if isinstance(screen, (Screen, ScrollableSurface, DropDown)):
            screen.addWidget(self)
            if actionButton:
                screen.actionButton = self
        self.show()

    def show(self):
        if isinstance(self.display, (ScrollableSurface, DropDown)):
            display = self.display.contentSurface
        else:
            display = self.display
        self.button_text1 = Label(display, self.text, self.labelRect, self.font, self.colours[self.active], self.fg, align='centre', justify='centre', addSelf=False)
        pg.draw.rect(display, self.borderColour, self.rect)
        pg.draw.rect(display, self.colours[self.active], (self.rect[0]+self.borderWidth, self.rect[1]+self.borderWidth, self.rect[2]-(2*self.borderWidth), self.rect[3]-(2*self.borderWidth)))
        self.button_text1.show()

    def isOver(self, x, y):
        if self.rect[0]<=x<=self.rect[0]+self.rect[2]:
            if self.rect[1]<=y<=self.rect[1]+self.rect[3]:
                return True
        return False

    def update(self, event):
        ret = False
        updatedBefore = self.display.getScreen().totalUpdates.count(True) > self.display.getScreen().layeredUpdates[self.zlayer].count(True)
        x, y = pg.mouse.get_pos()
        if isinstance(self.display, ScrollableSurface):
            x -= self.display.showRect[0]+self.display.offset[0]
            y -= self.display.showRect[1]+self.display.offset[1]
            if isinstance(self.display.display, DropDown):
                x -= self.display.display.rect[0]
                y -= self.display.display.rect[1]+self.display.display.rect[3]
        if isinstance(self.display, DropDown):
            x -= self.display.rect[0]
            y -= self.display.rect[1]+self.display.rect[3]
        over = self.isOver(x, y)
        if event.type == pg.MOUSEMOTION:
            if over:
                self.active = 1
            else:
                self.active = 0
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                if over and not updatedBefore:
                    ret = True
                    self.func()
        return ret


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
        self.endCursorPos = len(self.text)
        self.textR = self.font.render(self.text, False, self.colours[1])
        self.textOffset = 8
        self.charBuffer = 3
        self.zlayer = zlayer
        if isinstance(screen, (Screen, ScrollableSurface)):
            screen.addWidget(self)

    def reset(self):
        self.text = ''
        self.cursorPos = 0
        self.homeCursorPos = 0
        self.endCursorPos = 0
        self.textR = self.font.render(self.text, False, self.colours[1])
        self.active = 0
        self.activated = 0

    def getTextWidth(self):
        return self.font.size(self.text[self.homeCursorPos:self.endCursorPos+1])[0]

    def isWider(self):
        return self.getTextWidth() > self.rect[2] - (2*self.borderWidth) - self.textOffset

    def show(self):
        c = self.fg if self.activated > 0 else [min(255,(i+75)) for i in self.fg]
        self.textR = self.font.render(self.text[self.homeCursorPos:self.endCursorPos+1], True, c)
        if isinstance(self.display, ScrollableSurface):
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
        ret = False
        if event.type == pg.MOUSEBUTTONDOWN:
            x, y = pg.mouse.get_pos()
            if self.rect[0]<=x<=self.rect[0]+self.rect[2]:
                if self.rect[1]<=y<=self.rect[1]+self.rect[3]:
                    ret = True
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

                # print(self.homeCursorPos, self.cursorPos, self.endCursorPos, len(self.text))
        return ret


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
        if isinstance(self.display, ScrollableSurface):
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
        if isinstance(screen, (Screen, ScrollableSurface, DropDown)) and addSelf:
            screen.addWidget(self)

    def show(self):
        self.update()
        if isinstance(self.display, (ScrollableSurface, DropDown)):
            display = self.display.contentSurface
        else:
            display = self.display
        if self.border:
            borderColour = self.borderColour
        else:
            borderColour = self.bg
        try:
            pg.draw.rect(display, borderColour, self.rect)
            pg.draw.rect(display, self.bg, (self.rect[0]+self.borderWidth, self.rect[1]+self.borderWidth, self.rect[2]-2*self.borderWidth, self.rect[3]-2*self.borderWidth))
            display.blit(self.label, self.label_rect)
        except TypeError:
            return

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
        self.display.fill(0)
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


class DropDown:
    def __init__(self, screen, layer, rect, dropHeight, text, bg, fg, inactiveColour, activeColour, borderC, font, borderWidth=3, barWidth=5, padding=10, zlayer=0):
        self.display = screen
        self.rect = rect
        self.dropHeight = dropHeight
        self.text = text
        self.bg = bg
        self.fg = fg
        self.inactiveColour = inactiveColour
        self.activeColour = activeColour
        self.borderC = borderC
        self.font = font
        self.borderWidth = borderWidth
        self.barWidth = barWidth
        self.padding = padding
        self.zlayer = zlayer
        self.down = False
        self.contentSurface = pg.Surface((self.rect[2]-self.borderWidth*2, self.dropHeight-self.borderWidth*2))
        self.layer = layer
        self.widgets = []
        if isinstance(screen, Screen):
            self.display.addEmbed(self)

        self.label_rect = (self.rect[0], self.rect[1], self.rect[2]*0.8, self.rect[3])
        self.button_rect = (self.rect[0]+self.rect[2]*0.8-self.borderWidth, self.rect[1], self.rect[2]*0.2+self.borderWidth, self.rect[3]) 
        self.label = Label(self.display, self.text, self.label_rect, self.font, self.bg, self.fg, align='center', border=True, borderColour=self.borderC, borderWidth=self.borderWidth, zlayer=self.zlayer)
        self.button = Button(self.display, '\\/', self.button_rect, self.font, self.inactiveColour, self.activeColour, self.fg, self.borderC, lambda: self.flip(), borderWidth=self.borderWidth, zlayer=self.zlayer)

    def getScreen(self):
        if isinstance(self.display, Screen):
            return self.display
        else:
            return self.display.getScreen()

    def flip(self):
        self.down = not self.down
        if self.down:
            self.button.text = '/\\'
        else:
            self.button.text = '\\/'

    def addWidget(self, other):
        self.widgets.append(other)

    def clear(self):
        self.layer.fill(0)
        self.contentSurface.fill(self.bg)
        for i in self.widgets:
            if isinstance(i, ScrollableSurface):
                i.clear()

    def show(self):
        if self.down:
            pg.draw.rect(self.layer, self.borderC, (self.rect[0], self.rect[1]+self.rect[3]-self.borderWidth, self.rect[2], self.dropHeight))
            for i in self.widgets:
                i.show()
            self.layer.blit(self.contentSurface, (self.rect[0]+self.borderWidth, self.rect[1]+self.rect[3]))
            self.display.blit(self.layer, (0,0))
            
    def update(self, event):
        ret = False
        if self.down:
            for i in self.widgets:
                if not isinstance(i, (Label, ImageRect)):
                    ret = ret or i.update(event)
        return ret


class LayeredSurface(pg.Surface):
    def __init__(self, screen, DIM, zlayer=0, *args, **kwargs):
        super().__init__(DIM, *args, **kwargs)
        self.zlayer = zlayer
        self.parent = screen
        if isinstance(screen, Screen):
            screen.addWidget(self)
            

class ScrollableSurface(pg.Surface):
    def __init__(self, screen, x, y, DIM, bg, inactiveColour, activeColour, barWidth=5, padding=10, addSelf=True, zlayer=0):
        super().__init__(DIM)
        self.display = screen
        self.showRect = (int(x), int(y), int(DIM[0]), int(DIM[1]))
        self.bg = bg
        self.colours = [inactiveColour, activeColour]
        self.zlayer = zlayer
        self.scrollv = 0.18
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
        if isinstance(self.display, Screen) and addSelf:
            self.display.addEmbed(self)
        elif isinstance(self.display, DropDown) and addSelf:
            self.display.addWidget(self)
    
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

    def getScreen(self):
        if isinstance(self.display, Screen):
            return self.display
        else:
            return self.display.getScreen()

    def addWidget(self, other):
        self.widgets.append(other)
        self.contentSurface = pg.transform.scale(self.contentSurface, (self.contentRect[2], self.contentRect[3]))
        self.excess = [self.contentRect[2] + self.padding - self.showRect[2], self.contentRect[3] + self.padding - self.showRect[3]]
        self.barHeight = (self.showRect[3]**2)//(self.contentRect[3])
        if self.barHeight < 20:
            self.barHeight = 20

    def isOver(self):
        x, y = pg.mouse.get_pos()
        if isinstance(self.display, DropDown):
            x, y = x-self.display.rect[0]-self.display.borderWidth, y-self.display.rect[1]-self.display.rect[3]
        if self.showRect[0]<=x<=self.showRect[0]+self.showRect[2]:
            if self.showRect[1]<=y<=self.showRect[1]+self.showRect[3]:
                return True
        return False

    def clear(self):
        self.fill(self.bg)
        self.contentSurface.fill(self.bg)

    def removeAll(self):
        self.widgets.clear()

    def update(self, event):
        ret = False
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
                    ret = True
                    if keys[pg.K_RCTRL]:
                        self.ratio += self.scrollv * xstrength
                    else:
                        self.ratio += self.scrollv * ystrength
                if event.button == 5:
                    ret = True
                    if keys[pg.K_RCTRL]:
                        self.ratio -= self.scrollv * xstrength
                    else:
                        self.ratio -= self.scrollv * ystrength

                self.ratio = min(max(self.ratio, 0), 1)

                if event.button == 1:
                    x, y = pg.mouse.get_pos()
                    x, y = x - self.showRect[0], y - self.showRect[1]
                    if isinstance(self.display, DropDown):
                        x, y = x-self.display.rect[0]-self.display.borderWidth, y-self.display.rect[1]-self.display.rect[3]
                    if self.bar.width < 7:
                        bx, by = self.bar.x, self.bar.y
                        dx = abs(x-bx)
                        if dx < self.barSnap and by<y<by+self.bar.height:
                            ret = True
                            self.barGrab = 1
                    else:
                        if self.bar.collidepoint(x, y):
                            self.barGrab = 1
                            ret = True
        if event.type == pg.MOUSEBUTTONUP:
            if event.button == 1:
                if self.barGrab:
                    self.barGrab = 0
        if event.type == pg.MOUSEMOTION:
            if self.barGrab:
                x, y = pg.mouse.get_pos()
                y -= self.showRect[1]
                if isinstance(self.display, DropDown):
                    y = y-self.display.rect[1]-self.display.rect[3]
                self.ratio = 1 - (y-(2*self.padding))/(self.showRect[3]-(2*self.padding)-self.barHeight)
                self.ratio = min(max(self.ratio, 0), 1)
                self.show()

        for i in self.widgets:
            if not isinstance(i, (Label, ImageRect)): 
                ret = ret or i.update(event)
        return ret

    def show(self):
        for i in self.widgets:
            i.show()
        barx = self.showRect[2]-self.padding-self.barw
        self.offset[1] = (self.ratio) * (self.padding + self.excess[1]) - self.excess[1]
        self.barStart = (1-self.ratio) * (self.showRect[3]-(2*self.padding)-self.barHeight) + self.padding
        self.blit(self.contentSurface, (self.offset[0], self.offset[1]))
        self.bar = pg.draw.rect(self, self.colours[self.barGrab], (barx, self.barStart, self.barw, self.barHeight))
        if isinstance(self.display, Screen):
            display = self.display
        else:
            display = self.display.contentSurface
        display.blit(self, (self.showRect[0], self.showRect[1]))


class Screen(pg.Surface):
    def __init__(self, DIM):
        super().__init__(DIM)
        self.DIM = DIM
        self.widgets = OrderedDict()
        self.embed = OrderedDict()
        self.actionButton = None
        self.info = {}

    def redraw(self):
        pass
        
    def addWidget(self, widget):
        try:
            self.widgets[widget.zlayer].append(widget)
        except KeyError:
            self.widgets[widget.zlayer] = [widget]

    def addEmbed(self, embed):
        try:
            self.embed[embed.zlayer].append(embed)
        except KeyError:
            self.embed[embed.zlayer] = [embed]

    def getScreen(self):
        return self

    def clear(self):
        self.widgets.clear()
        self.embed.clear()
        self.info = {}
        self.actionButton = None

    def event_update(self, event):
        self.totalUpdates = []
        self.layeredUpdates = {}
        embedKeys = reversed(list(self.embed))
        widgetsKeys = reversed(list(self.widgets))

        for layer in embedKeys:
            if layer not in self.layeredUpdates: self.layeredUpdates[layer] = []
            for embed in self.embed[layer]:
                v = embed.update(event)
                self.totalUpdates.append(v)
                self.layeredUpdates[layer].append(v)

        for layer in widgetsKeys:
            if layer not in self.layeredUpdates: self.layeredUpdates[layer] = []
            for widget in self.widgets[layer]:
                if isinstance(widget, (Input, Button, DraggablePoint, DraggableRect)):
                    v = widget.update(event)
                    self.totalUpdates.append(v)
                    self.layeredUpdates[layer].append(v)

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_RETURN:
                if self.actionButton != None:
                    self.actionButton.func()

    
    def update(self):
        for layer in self.embed:
            for embed in self.embed[layer]:
                embed.clear()

        for layer in self.widgets:
            for widget in self.widgets[layer]:
                if isinstance(widget, (Input, DraggablePoint, DraggableRect, Button, ImageRect, Label)):
                    widget.show()
                elif isinstance(widget, (LayeredSurface,)):
                    self.blit(widget, (0,0))

        for layer in self.embed:
            for embed in self.embed[layer]:
                embed.show()



def doNothing():
	pass

def template():
    print(boilerplate)

def boilerPlate():
    print(boilerplate)


boilerplate = '''
import pygame as pg
import pygameutil as pgu

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