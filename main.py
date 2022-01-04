import pygame as pg
import requests
from graphics import pygameutil as pgu
from graphics import widget as wid
from parsing import parse
from parsing.tokens import *

def changeSelectedWidget(new):
    wid.selectedWidget = new

def changeScreen(new):
    global curScreen
    if new == 'main':
        curScreen = mainScreen
    elif new == 'simplifier':
        curScreen = simplifierScreen
    elif new == 'logic':
        curScreen = logicScreen
    elif new == 'table':
        curScreen = tableScreen
    elif new == 'logicHelp':
        curScreen = logicHelpScreen
    elif new == 'syntaxHelp':
        curScreen = syntaxHelpScreen

def tableScreenSetup():
    def buttonFunc(s, tb):
        val = validateExpression(s)
        if not val:
            errorLabel.text = 'Error with input'
        else:
            errorLabel.text = ''
            drawTable(s, tb)
    buttonW = 600
    buttonH = 100
    gap = 30
    start = (DIM[1]-buttonH)/2 - 100
    tableScreen.fill(BACKGROUNDC)
    heading = pgu.Label(tableScreen, 'Truth Table', (0, 0, DIM[0], DIM[1]/3), subtitleFont, BACKGROUNDC, TEXTC, align='center', justify='center')
    homeButton = pgu.Button(tableScreen, 'Home', (20, 20, 125, 70), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeScreen('main'))
    entry = pgu.Input(tableScreen, ((DIM[0]-buttonW-150-gap)/2, start, buttonW, buttonH), vLargeFont, [BACKGROUNDC, HIGHLIGHT1], TEXTC, BORDERC, text='Enter Expression')
    errorLabel = pgu.Label(tableScreen, '', ((DIM[0]-buttonW-150-gap)/2 - gap - 150, start, 150, buttonH), largeFont, BACKGROUNDC, TEXTC, align='right')    
    tableBox = pgu.ScrollableSurface(tableScreen, (DIM[0]-buttonW-150-gap)/2, (DIM[1]-buttonH)/2 - 50 + buttonH + gap, (buttonW+200+gap, DIM[1]-((DIM[1]-buttonH)/2 -50 + buttonH + gap*2)), BACKGROUNDC, BORDERC, TEXTC)
    simplifyButton = pgu.Button(tableScreen, 'Simplify', ((DIM[0]-buttonW-150-gap)/2 + buttonW + gap, start, 150, buttonH), largeFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: buttonFunc(entry.text, tableBox), actionButton=True)

def logicScreenSetup():
    logicScreen.fill(BACKGROUNDC)
    ribbonBorder = pg.draw.rect(logicScreen, BORDERC, (0, 0, DIM[0], 80))
    ribbon = pg.draw.rect(logicScreen, HIGHLIGHT2, (0, 0, DIM[0], 80-3))
    homeButton = pgu.Button(logicScreen, 'Home', (15, 15, 125, 50), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeScreen('main'))
    helpButton = pgu.Button(logicScreen, 'Help', (DIM[0]-15-125, 15, 125, 50), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeScreen('logicHelp'))
    widgetBoxBorder = pg.draw.rect(logicScreen, BORDERC, (0, 80, 250, DIM[1]))
    widgetBox = pgu.ScrollableSurface(logicScreen, 0, 80, (250-3, DIM[1]-80), BACKGROUNDC, BORDERC, TEXTC, padding=8)
    sandboxWindow = wid.Grid(logicScreen, 250, 80, (DIM[0]-250, DIM[1]-80), BACKGROUNDC, TEXTC, TEXTC, HIGHLIGHT1, BORDERC)
    switchButton = pgu.Button(widgetBox, 'Switch', (0, (120+10)*0, 210, 120), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeSelectedWidget('switch'))
    bulbButton = pgu.Button(widgetBox, 'Bulb',     (0, (120+10)*1, 210, 120), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeSelectedWidget('bulb'))
    andButton = pgu.Button(widgetBox, 'And',       (0, (120+10)*2, 210, 120), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeSelectedWidget('and'))
    orButton = pgu.Button(widgetBox, 'Or',         (0, (120+10)*3, 210, 120), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeSelectedWidget('or'))
    notButton = pgu.Button(widgetBox, 'Not',       (0, (120+10)*4, 210, 120), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeSelectedWidget('not'))
    xorButton = pgu.Button(widgetBox, 'Xor',       (0, (120+10)*5, 210, 120), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeSelectedWidget('xor'))
    norButton = pgu.Button(widgetBox, 'Nor',       (0, (120+10)*6, 210, 120), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeSelectedWidget('nor'))
    nandButton = pgu.Button(widgetBox, 'Nand',       (0, (120+10)*7, 210, 120), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeSelectedWidget('nand'))

def logicHelpScreenSetup():
    logicHelpScreen.fill(BACKGROUNDC)
    heading = pgu.Label(logicHelpScreen, 'Logic Simulator Help', (0, 0, DIM[0], DIM[1]/3), subtitleFont, BACKGROUNDC, TEXTC, align='center', justify='center', addSelf=False)
    homeButton = pgu.Button(logicHelpScreen, 'Back', (15, 15, 125, 50), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeScreen('logic'))
    text = '''Click on a button in the scrollable side window to select the widget
The selected widget id indicated by a floating box next to the cursor in the grid window
Click somewhere in the grid to place the widget
To connect widgets click on outputs(right circles) and then separatley on inputs(left circles) no dragging is needed
To delete a connection hover over the line and press backspace
To delete a widget hover over it and press backspace
To toggle a switch click on it'''
    text = text.split('\n')
    h = 0
    for line in text:
        l = pgu.Label(logicHelpScreen, line, (150, 200+h, DIM[0]-300, 75), medFont, BACKGROUNDC, TEXTC, align='center', addSelf=False)
        h += 75
    pg.draw.rect(logicHelpScreen, TEXTC, (100, 185, DIM[0]-200, DIM[1]-200), 3)

def simplifierScreenSetup(steps=[]):
    def buttonFunc(e):
        val = validateExpression(e.text)
        if not val:
            errorLabel.text = 'Error with input'
        else:
            errorLabel.text = ''
            simplify(e.text)
            e.text = ''
    simplifierScreen.fill(BACKGROUNDC)
    buttonW = 600
    buttonH = 100
    gap = 30
    start = (DIM[1]-buttonH)/2 - 100
    heading = pgu.Label(simplifierScreen, 'Boolean Simplification', (0, 0, DIM[0], DIM[1]/3), subtitleFont, BACKGROUNDC, TEXTC, align='center', justify='center')
    homeButton = pgu.Button(simplifierScreen, 'Home', (20, 20, 125, 70), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeScreen('main'))
    entry = pgu.Input(simplifierScreen, ((DIM[0]-buttonW-150-gap)/2, start, buttonW, buttonH), vLargeFont, [BACKGROUNDC, HIGHLIGHT1], TEXTC, BORDERC, text='Enter Expression')
    simplifyButton = pgu.Button(simplifierScreen, 'Simplify', ((DIM[0]-buttonW-150-gap)/2 + buttonW + gap, start, 150, buttonH), largeFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: buttonFunc(entry), actionButton=True)
    errorLabel = pgu.Label(simplifierScreen, '', ((DIM[0]-buttonW-150-gap)/2 - gap - 150, start, 150, buttonH), medFont, BACKGROUNDC, TEXTC, align='right')    
    stepsBox = pgu.ScrollableSurface(simplifierScreen, (DIM[0]-buttonW-150-gap)/2, (DIM[1]-buttonH)/2 - 50 + buttonH + gap, (buttonW+200+gap, DIM[1]-((DIM[1]-buttonH)/2 -50 + buttonH + gap*2)), BACKGROUNDC, BORDERC, TEXTC)
    h=0
    for i, step in enumerate(steps[:-1]):
        createPNG(step[1])
        tmp = pg.image.load(f'tmpimages\\tmp.png')
        tmp = tmp.convert()
        tmp.set_colorkey((255,255,255))
        tmpl = pgu.Label(stepsBox, f'{step[0]}: ', (0, h, stepsBox.showRect[2], 50), medFont, BACKGROUNDC, TEXTC)
        tmpI = pgu.ImageRect(stepsBox, tmp, 0, h + 50)
        h += tmp.get_height() + stepsBox.padding/2 + 50

def syntaxHelpScreenSetup():
    syntaxHelpScreen.fill(BACKGROUNDC)
    heading = pgu.Label(syntaxHelpScreen, 'Syntax Help', (0, 0, DIM[0], DIM[1]/3), subtitleFont, BACKGROUNDC, TEXTC, align='center', justify='center', addSelf=False)
    homeButton = pgu.Button(syntaxHelpScreen, 'Back', (15, 15, 125, 50), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeScreen('main'))
    text = '''Operators: OR = +, AND = *, NOT = ¬
Bracket Rules: OR = (__+__), AND = (__*__) optional (), NOT = ¬(__) optional () if contents is a variable e.g. ¬(A) = ¬A
Otherwise regular order of operations rules apply.
Ensure all brackets are paired up properly.
Variables can be uppercase and lowercase characters only as well as the digits 0 and 1'''
    text = text.split('\n')
    h = 0
    for line in text:
        l = pgu.Label(syntaxHelpScreen, line, (15, 200+h, DIM[0], 100), medFont, BACKGROUNDC, TEXTC, align='center', addSelf=False)
        h += 100
    pg.draw.rect(syntaxHelpScreen, TEXTC, (100, 185, DIM[0]-200, DIM[1]-200), 3)

def mainScreenSetup():
    mainScreen.fill(BACKGROUNDC)
    buttonW = 600
    buttonH = 100
    gap = 30
    start = (DIM[1]-buttonH)/2 - buttonH
    heading = pgu.Label(mainScreen, 'b L o g i c.', (0, 0, DIM[0], DIM[1]/3), titleFont, BACKGROUNDC, TEXTC, align='center', justify='center')
    simplifierButton = pgu.Button(mainScreen, 'Simplifier', ((DIM[0]-buttonW)/2, start, buttonW, buttonH), vLargeFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeScreen('simplifier'))
    logicSimButton = pgu.Button(mainScreen, 'Logic Simulator', ((DIM[0]-buttonW)/2, start + (buttonH + gap), buttonW, buttonH), vLargeFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeScreen('logic'))
    tableButton = pgu.Button(mainScreen, 'Truth Table', ((DIM[0]-buttonW)/2, start + (buttonH + gap)*2, buttonW, buttonH), vLargeFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeScreen('table'))
    syntaxButton = pgu.Button(mainScreen, 'Syntax Help', ((DIM[0]-buttonW)/2, start + (buttonH + gap)*3, buttonW, buttonH), vLargeFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeScreen('syntaxHelp'))

def createPNG(step):
    latex = step.getLatex()
    r = requests.get(f'https://latex.codecogs.com/png.image?\\dpi{{300}}{latex}')
    with open(f'tmpimages\\tmp.png', 'wb') as f:
        f.write(r.content)

def simplify(s):
    if validateExpression(s):
        ss = parse.parse(s)
        steps = ss.simplify()
        simplifierScreenSetup(steps=steps)
        return True
    else:
        return False

def drawTable(s, tb):
    tb.removeAll()
    totalW = tb.showRect[2]
    varss = s.replace('(','').replace(')','').replace('¬','').replace('*','').replace('+','')
    varss = list(set(list(varss)))
    varss = sorted(varss)
    noOfVars = len(varss)
    maxLen = len(bin(2**noOfVars - 1)[2:])
    cellW = totalW//(noOfVars+3)
    new = s
    for i, v in enumerate(varss):
        pgu.Label(tb, v, ((cellW-3)*i, 0, cellW, cellW), smallFont, BACKGROUNDC, TEXTC, align='centre', border=True, borderColour=BORDERC)
    pgu.Label(tb, 'Output', ((cellW-3)*noOfVars, 0, cellW*2, cellW), smallFont, BACKGROUNDC, TEXTC, align='centre', border=True, borderColour=BORDERC)
    for y in range(2**noOfVars):
        b = str(bin(y))[2:]
        b = '0'*(maxLen-len(b)) + b
        vals = list(b)
        for ind, var in enumerate(varss):
            new = new.replace(var, vals[ind])
        tmp = parse.parse(new)
        ans = tmp.simplify()
        new = s
        output = ans[-1][1].terms[0].rep
        for x in range(len(vals)):
            pgu.Label(tb, vals[x], ((cellW-3)*x, cellW - 3 + (cellW-3)*y, cellW, cellW), smallFont, BACKGROUNDC, TEXTC, align='centre', border=True, borderColour=BORDERC)
        pgu.Label(tb, output, ((cellW-3)*len(vals), cellW - 3 + (cellW-3)*y, cellW*2, cellW), smallFont, BACKGROUNDC, TEXTC, align='centre', border=True, borderColour=BORDERC)

def validateExpression(s):
    try:
        ss = parse.parse(s)
        return True
    except:
        return False


pg.init()
pg.font.init()

smallFont = pg.font.SysFont('Calibri', 16)
medFont = pg.font.SysFont('Calibri', 24)
largeFont = pg.font.SysFont('Calibri', 36)
vLargeFont = pg.font.SysFont('Calibri', 48)
subtitleFont = pg.font.SysFont('Calibri', 86)
titleFont = pg.font.SysFont('Calibri', 121)

DIM = (1450, 725)

testc = [(0.05+0.1*i, 0.05+0.1*i, 0.1*(i+1)) for i in range(10)]
testc = [[round(k*255) for k in i] for i in testc]

BORDERC = (199, 81, 70)#testc[3]
BACKGROUNDC = testc[8]
HIGHLIGHT1 = testc[6]
HIGHLIGHT2 = testc[7]
TEXTC = testc[2]

print(BORDERC, BACKGROUNDC, HIGHLIGHT1, HIGHLIGHT2, TEXTC)
display = pg.display.set_mode(DIM)
clock = pg.time.Clock()

mainScreen = pgu.Screen(DIM)
mainScreenSetup()
simplifierScreen = pgu.Screen(DIM)
simplifierScreenSetup()
logicScreen = pgu.Screen(DIM)
logicScreenSetup()
tableScreen = pgu.Screen(DIM)
tableScreenSetup()
logicHelpScreen = pgu.Screen(DIM)
logicHelpScreenSetup()
syntaxHelpScreen = pgu.Screen(DIM)
syntaxHelpScreenSetup()

curScreen = mainScreen
run = True
while run:
    # curScreen.fill(BACKGROUNDC)
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

