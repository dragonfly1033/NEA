import sys
sys.path.insert(0, './parsing')
import pygame as pg
from graphics import pygameutil as pgu
from parsing import parse

def changeScreen(new):
    global curScreen
    if new == 'main':
        curScreen = mainScreen
    elif new == 'simplifier':
        curScreen = simplifierScreen


def simplifierScreenSetup():
    simplifierScreen.fill(BACKGROUNDC)
    buttonW = 600
    buttonH = 100
    gap = 30
    heading = pgu.Label(simplifierScreen, 'Boolean Simplification', (0, 0, DIM[0], DIM[1]/3), subtitleFont, BACKGROUNDC, TEXTC, align='center', justify='center')
    homeButton = pgu.Button(simplifierScreen, 'Home', (20, 20, 150, 50), medFont, BACKGROUNDC, LBLUE, TEXTC, BORDERC, lambda: changeScreen('main'))
    entry = pgu.Input(simplifierScreen, ((DIM[0]-buttonW)/2, (DIM[1]-buttonH)/2 - 50, buttonW, buttonH), vLargeFont, [BACKGROUNDC, LBLUE], TEXTC, BORDERC, text='Enter Expression')
    simplifyButton = pgu.Button(simplifierScreen, 'Simplify', ((DIM[0]-buttonW)/2 + buttonW + gap, (DIM[1]-buttonH)/2 - 50, 150, buttonH), medFont, BACKGROUNDC, LBLUE, TEXTC, BORDERC, lambda: simplify(entry.text), actionButton=True)


def mainScreenSetup():
    mainScreen.fill(BACKGROUNDC)
    buttonW = 600
    buttonH = 100
    gap = 30
    heading = pgu.Label(mainScreen, 'b L o g i c.', (0, 0, DIM[0], DIM[1]/3), titleFont, BACKGROUNDC, TEXTC, align='center', justify='center')
    simplifierButton = pgu.Button(mainScreen, 'Simplifier', ((DIM[0]-buttonW)/2, (DIM[1]-buttonH)/2, buttonW, buttonH), vLargeFont, BACKGROUNDC, LBLUE, TEXTC, BORDERC, lambda: changeScreen('simplifier'))
    logicSimButton = pgu.Button(mainScreen, 'Logic Simulator', ((DIM[0]-buttonW)/2, (DIM[1]-buttonH)/2 + (buttonH + gap), buttonW, buttonH), vLargeFont, BACKGROUNDC, LBLUE, TEXTC, BORDERC, lambda: print())
    loginButton = pgu.Button(mainScreen, 'Log In', ((DIM[0]-buttonW)/2, (DIM[1]-buttonH)/2 + (buttonH + gap)*2, buttonW, buttonH), vLargeFont, BACKGROUNDC, LBLUE, TEXTC, BORDERC, lambda: print())


def simplify(s):
    ss = parse.parse(s)
    ss.simplify()

pg.init()
pg.font.init()

smallFont = pg.font.SysFont('Calibri', 16)
medFont = pg.font.SysFont('Calibri', 24)
largeFont = pg.font.SysFont('Calibri', 36)
vLargeFont = pg.font.SysFont('Calibri', 48)
subtitleFont = pg.font.SysFont('Calibri', 86)
titleFont = pg.font.SysFont('Calibri', 121)

DIM = (1450, 725)

TEXTC = (73, 88, 103)
BORDERC = (254, 95, 85)
BACKGROUNDC = (247, 247, 255)
DBLUE = (87, 115, 153)
LBLUE = (189, 213, 234)

display = pg.display.set_mode(DIM)
clock = pg.time.Clock()

mainScreen = pgu.Screen(DIM)
mainScreenSetup()
simplifierScreen = pgu.Screen(DIM)
simplifierScreenSetup()


curScreen = mainScreen
run = True
while run:
    curScreen.fill(BACKGROUNDC)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        curScreen.event_update(event)
    curScreen.update()

    clock.tick(1000)
    display.blit(curScreen, (0,0))
    pg.display.update()

pg.quit()
quit()

