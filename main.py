import pygame as pg
import urllib.request
import hashlib
from graphics import pygameutil as pgu
from graphics import widget as wid
from parsing import parse
from parsing.tokens import *
import accounts.sql as sql

def changeSelectedWidget(sw, new):
    sw.selectedWidget = new

def validateExpression(s):
    try:
        ss = parse.parse(s)
        return True
    except:
        return False

def changeScreen(new, *args):
    global curScreen
    if new == 'main':
        curScreen = mainScreen
        mainScreenSetup(*args)
    elif new == 'simplifier':
        curScreen = simplifierScreen
        simplifierScreenSetup(*args)
    elif new == 'logic':
        curScreen = logicScreen
        logicScreenSetup(*args)
    elif new == 'table':
        curScreen = tableScreen
        tableScreenSetup(*args)
    elif new == 'logicHelp':
        curScreen = logicHelpScreen
        logicHelpScreenSetup(*args)
    elif new == 'syntaxHelp':
        curScreen = syntaxHelpScreen
        syntaxHelpScreenSetup(*args)
    elif new == 'login':
        curScreen = loginScreen
        loginScreenSetup(*args)
    # curScreen.switchTo()

def logicHelpScreenSetup(*args):
    logicHelpScreen.clear()
    logicHelpScreen.fill(BACKGROUNDC)
    logicHelpScreen.redraw = lambda: pg.draw.rect(logicHelpScreen, TEXTC, (100, 185, DIM[0]-200, DIM[1]-200), 3)
    logicHelpScreen.redraw()
    heading = pgu.Label(logicHelpScreen, 'Logic Simulator Help', (0, 100, DIM[0], DIM[1]/3 - 200), subtitleFont, BACKGROUNDC, TEXTC, align='center', justify='center')
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
        l = pgu.Label(logicHelpScreen, line, (106, 190+h, DIM[0]-212, 80), medFont, BACKGROUNDC, TEXTC, align='center')
        h += 72

def syntaxHelpScreenSetup(*args):
    syntaxHelpScreen.clear()
    syntaxHelpScreen.fill(BACKGROUNDC)
    syntaxHelpScreen.redraw = lambda: pg.draw.rect(syntaxHelpScreen, TEXTC, (100, 185, DIM[0]-200, DIM[1]-200), 3)
    syntaxHelpScreen.redraw()
    heading = pgu.Label(syntaxHelpScreen, 'Syntax Help', (0, 100, DIM[0], DIM[1]/3 - 200), subtitleFont, BACKGROUNDC, TEXTC, align='center', justify='center')
    homeButton = pgu.Button(syntaxHelpScreen, 'Back', (15, 15, 125, 50), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeScreen('main'))
    text = '''Operators: OR = +, AND = *, NOT = ¬
Bracket Rules: OR = (_+_), AND = (_*_) optional (), NOT = ¬(_) optional () if contents is a variable e.g. ¬(A) = ¬A
Otherwise regular order of operations rules apply.
Ensure all brackets are paired up properly.
Variables can be uppercase and lowercase characters only as well as the digits 0 and 1'''
    text = text.split('\n')
    h = 0
    for line in text:
        l = pgu.Label(syntaxHelpScreen, line, (106, 190+h, DIM[0]-212, 100), medFont, BACKGROUNDC, TEXTC, align='center')
        h += 100

def tableScreenSetup(*args):
    tableScreen.clear()
    def buttonFunc(s, tb, screen):
        val = validateExpression(s.text)
        if not val:
            errorLabel.text = 'Error with input'
            screen.info['expr'] = None
        else:
            errorLabel.text = ''
            setLoading(drawTable, s.text, tb, errorLabel)
            screen.info['expr'] = parse.parse(s.text)
        s.reset()

    def buttonFunc2(errorLabel, screen):
        if 'expr' in screen.info:
            expr = parse.parse(screen.info['expr'].rep)
        else:
            expr = None
        exprToLogic(expr, errorLabel)

    def buttonFunc3(errorLabel, screen):
        if 'expr' in screen.info:
            expr = screen.info['expr']
        else:
            expr = None
        exprToSimplify(expr, errorLabel)
    
    def saveExprWrapper(el, screen):
        if 'expr' in screen.info:
            expr = screen.info['expr']
            saveExpr(expr.rep)
            tableScreenSetup()
        else:
            el.text = 'No Answer'
        
    buttonW = 600
    buttonH = 100
    gap = 30
    start = (DIM[1]-buttonH)/2 - 100
    tableScreen.fill(BACKGROUNDC)
    heading = pgu.Label(tableScreen, 'Truth Table', (0, 0, DIM[0], DIM[1]/3), subtitleFont, BACKGROUNDC, TEXTC, align='center', justify='center')
    homeButton = pgu.Button(tableScreen, 'Home', (20, 20, 125, 70), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeScreen('main'))
    entry = pgu.Input(tableScreen, ((DIM[0]-buttonW-150-gap)/2, start, buttonW, buttonH), vLargeFont, [BACKGROUNDC, HIGHLIGHT1], TEXTC, BORDERC, text='Enter Expression')
    errorLabel = pgu.Label(tableScreen, '', ((DIM[0]-buttonW-150-gap)/2 - gap - 275, start, 275, buttonH), medFont, BACKGROUNDC, TEXTC, align='right')    
    tableBox = pgu.ScrollableSurface(tableScreen, (DIM[0]-buttonW-150-gap)/2, start + buttonH + gap - 10, (buttonW+150+gap, DIM[1]-(start+buttonH+gap-10+gap)), BACKGROUNDC, BORDERC, TEXTC, barWidth=10)
    tabulateButton = pgu.Button(tableScreen, 'Tabulate', ((DIM[0]-buttonW-150-gap)/2 + buttonW + gap, start, 150, buttonH), largeFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: buttonFunc(entry, tableBox, tableScreen), actionButton=True)
    
    logicConvertButton = pgu.Button(tableScreen, 'Answer => Logic Gates', ((DIM[0]-buttonW-150-gap)/2 + buttonW + gap + 150 + gap , start, 275, buttonH), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: buttonFunc2(errorLabel, tableScreen))
    simplifyConvertButton = pgu.Button(tableScreen, 'Answer => Simplify', ((DIM[0]-buttonW-150-gap)/2 + buttonW + gap + 150 + gap , start+buttonH+gap, 275, buttonH), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: buttonFunc3(errorLabel, tableScreen))

    if len(args) > 0:
        entry.text = args[0]
        buttonFunc(entry, tableBox, tableScreen)

    if loggedInAs != None:
        l = pgu.LayeredSurface(tableScreen, DIM, 3, pg.SRCALPHA)
        d = pgu.DropDown(tableScreen, l, (20, start + buttonH + gap - 10, 275,  buttonH), DIM[1]-(start+buttonH*2+gap+10), 'User Expressions', BACKGROUNDC, TEXTC, BACKGROUNDC, HIGHLIGHT1, BORDERC, medFont)
        s = pgu.ScrollableSurface(d, 0, 0, (270, DIM[1]-(start+buttonH*2+gap+15)), BACKGROUNDC, BORDERC, HIGHLIGHT1)
        exprs = getUserExprs()
        for i, v in enumerate(exprs):
            b = pgu.Button(s, v, (0, i*55, 230, 50), smallFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda v=v: changeScreen('table', v))
        saveExprButton = pgu.Button(tableScreen, 'Save Expression', ((DIM[0]-buttonW-150-gap)/2 + buttonW + gap + 150 + gap , start+(buttonH+gap)*2, 275, buttonH), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: saveExprWrapper(errorLabel, tableScreen))

def logicScreenSetup(*args):
    global sandboxWindow
    def exprToTable(expr, errorLabel):
        if expr == None:
            errorLabel.text = 'No Circuits'
            return
        if len(expr) > 1:
            for i in logicScreen.widgets:
                if i in toRemove:
                    logicScreen.widgets.remove(i)
            for i in logicScreen.embed:
                if i in toRemove:
                    logicScreen.embed.remove(i)
            toRemove.clear()
            errorLabel.text = 'Multiple Circuits Detected'
            layer = pgu.LayeredSurface(logicHelpScreen, DIM, 3, pg.SRCALPHA)
            d = pgu.DropDown(logicScreen, layer, (655, 15, 205, 50), 200, 'Select Circuit', BACKGROUNDC, TEXTC, BACKGROUNDC, HIGHLIGHT1, BORDERC, medFont, zlayer=3)
            s = pgu.ScrollableSurface(d, 0, 0, (200, 195), BACKGROUNDC, BORDERC, HIGHLIGHT1, barWidth=5, zlayer=3)
            for i, e in enumerate(expr):
                n = pgu.Button(s, e.rep, (0, 55*i, 160, 50), smallFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda e=e: changeScreen('table', e.rep), zlayer=3) 
                toRemove.append(n)
            toRemove.append(d)
            toRemove.append(s)
        else:
            changeScreen('table', expr[0].rep)
    
    def exprToSimplifyWrapper(expr, errorLabel):
        if expr == None:
            errorLabel.text = 'No Circuits'
            return
        if len(expr) > 1:
            for i in logicScreen.widgets:
                if i in toRemove:
                    logicScreen.widgets.remove(i)
            for i in logicScreen.embed:
                if i in toRemove:
                    logicScreen.embed.remove(i)
            toRemove.clear()
            errorLabel.text = 'Multiple Circuits Detected'
            layer = pgu.LayeredSurface(logicHelpScreen, DIM, 3, pg.SRCALPHA)
            d = pgu.DropDown(logicScreen, layer, (655, 15, 205, 50), 200, 'Select Circuit', BACKGROUNDC, TEXTC, BACKGROUNDC, HIGHLIGHT1, BORDERC, medFont, zlayer=3)
            s = pgu.ScrollableSurface(d, 0, 0, (200, 195), BACKGROUNDC, BORDERC, HIGHLIGHT1, barWidth=5, zlayer=3)
            for i, e in enumerate(expr):
                n = pgu.Button(s, e.rep, (0, 55*i, 160, 50), smallFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda e=e: setExpr(e.simplify()[-1][1].rep, errorLabel), zlayer=3) 
                toRemove.append(n)
            toRemove.append(d)
            toRemove.append(s)
        else:
            setExpr(expr[0].simplify()[-1][1].rep, errorLabel)

    def saveExprWrapper(errorLabel):     
        expr = gatesToExpr()

        if expr == None:
            errorLabel.text = 'No Circuits'
            return
        if len(expr) > 1:
            for i in logicScreen.widgets:
                if i in toRemove:
                    logicScreen.widgets.remove(i)
            for i in logicScreen.embed:
                if i in toRemove:
                    logicScreen.embed.remove(i)
            toRemove.clear()
            errorLabel.text = 'Multiple Circuits Detected'
            layer = pgu.LayeredSurface(logicHelpScreen, DIM, 3, pg.SRCALPHA)
            d = pgu.DropDown(logicScreen, layer, (655, 15, 205, 50), 200, 'Select Circuit', BACKGROUNDC, TEXTC, BACKGROUNDC, HIGHLIGHT1, BORDERC, medFont, zlayer=3)
            s = pgu.ScrollableSurface(d, 0, 0, (200, 195), BACKGROUNDC, BORDERC, HIGHLIGHT1, barWidth=5, zlayer=3)
            for i, e in enumerate(expr):
                n = pgu.Button(s, e.rep, (0, 55*i, 160, 50), smallFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda e=e: saveExpr(e.rep), zlayer=3) 
                toRemove.append(n)
            toRemove.append(d)
            toRemove.append(s)
        else:
            saveExpr(expr[0].rep)
        logicScreenSetup()

    def setExpr(expr, errorLabel):
        expr = parse.parse(expr)
        exprToLogic(expr, errorLabel)

    def redraw():
        ribbonBorder = pg.draw.rect(logicScreen, BORDERC, (0, 0, DIM[0], 80))
        ribbon = pg.draw.rect(logicScreen, HIGHLIGHT1, (0, 0, DIM[0], 80-3))
        widgetBoxBorder = pg.draw.rect(logicScreen, BORDERC, (0, 80, 250, DIM[1]))
        # pg.draw.rect(logicScreen, HIGHLIGHT1, (655, 15, 205, 50))
    
    logicScreen.redraw = redraw
    logicScreen.clear()
    logicScreen.fill(BACKGROUNDC)
    logicScreen.redraw()
    homeButton = pgu.Button(logicScreen, 'Home', (15, 15, 125, 50), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeScreen('main'))
    helpButton = pgu.Button(logicScreen, 'Help', (DIM[0]-15-125, 15, 125, 50), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeScreen('logicHelp'))
    widgetBox = pgu.ScrollableSurface(logicScreen, 0, 80, (250-3, DIM[1]-80), BACKGROUNDC, BORDERC, TEXTC, padding=8)
    sandboxWindow = wid.Grid(logicScreen, 250, 80, (DIM[0]-250, DIM[1]-80), BACKGROUNDC, TEXTC, TEXTC, HIGHLIGHT1, BORDERC)
    switchButton = pgu.Button(widgetBox, 'Switch', (0, (80+10)*0, 210, 80), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeSelectedWidget(sandboxWindow, 'switch'))
    bulbButton = pgu.Button(widgetBox, 'Bulb',     (0, (80+10)*1, 210, 80), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeSelectedWidget(sandboxWindow, 'bulb'))
    andButton = pgu.Button(widgetBox, 'And',       (0, (80+10)*2, 210, 80), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeSelectedWidget(sandboxWindow, 'and'))
    orButton = pgu.Button(widgetBox, 'Or',         (0, (80+10)*3, 210, 80), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeSelectedWidget(sandboxWindow, 'or'))
    notButton = pgu.Button(widgetBox, 'Not',       (0, (80+10)*4, 210, 80), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeSelectedWidget(sandboxWindow, 'not'))
    xorButton = pgu.Button(widgetBox, 'Xor',       (0, (80+10)*5, 210, 80), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeSelectedWidget(sandboxWindow, 'xor'))
    norButton = pgu.Button(widgetBox, 'Nor',       (0, (80+10)*6, 210, 80), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeSelectedWidget(sandboxWindow, 'nor'))
    nandButton = pgu.Button(widgetBox, 'Nand',     (0, (80+10)*7, 210, 80), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeSelectedWidget(sandboxWindow, 'nand'))
    highButton = pgu.Button(widgetBox, '1',        (0, (80+10)*8, 210, 80), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeSelectedWidget(sandboxWindow, 'high'))
    lowButton = pgu.Button(widgetBox, '0',         (0, (80+10)*9, 210, 80), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeSelectedWidget(sandboxWindow, 'low'))
    
    errorLabel = pgu.Label(logicScreen, '', (435, 15, 205, 50), smallMedFont, HIGHLIGHT1, TEXTC, align='center')    
    simplifyButton = pgu.Button(logicScreen, 'Simplify', (155, 15, 125, 50), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: exprToSimplifyWrapper(gatesToExpr(), errorLabel))
    tabulateButton = pgu.Button(logicScreen, 'Tabulate', (295, 15, 125, 50), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: exprToTable(gatesToExpr(), errorLabel))

    if loggedInAs != None:
        l = pgu.LayeredSurface(logicScreen, DIM, 3, pg.SRCALPHA)
        d = pgu.DropDown(logicScreen, l, (DIM[0]-15-125-15-205, 15, 205, 50), 250, 'User Expressions', BACKGROUNDC, TEXTC, BACKGROUNDC, HIGHLIGHT1, BORDERC, smallMedFont, zlayer=3)
        s = pgu.ScrollableSurface(d, 0, 0, (200, 240), BACKGROUNDC, BORDERC, HIGHLIGHT1, zlayer=3)
        exprs = getUserExprs()
        for i, v in enumerate(exprs):
            b = pgu.Button(s, v, (0, i*55, 160, 50), smallFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda v=v: setExpr(v, errorLabel), zlayer=3)
        saveExprButton = pgu.Button(logicScreen, 'Save Expression', (DIM[0]-15-125-15-205-15-205, 15, 205, 50), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: saveExprWrapper(errorLabel))

def simplifierScreenSetup(*args, steps=[]):
    global tableScreen
    simplifierScreen.clear()
    def buttonFunc(e):
        s = e.text.strip().replace(' ', '')
        val = validateExpression(s)
        if not val:
            errorLabel.text = 'Error with input'
        else:
            errorLabel.text = ''
            simplify(s)
        e.reset()
    
    def tableConvert(expr, el):
        if expr == None:
            el.text = 'No Answer'
        else:
            changeScreen('table', expr.rep)

    def saveExprWrapper(expr, el):
        if expr == None:
            el.text = 'No Answer'
        else:
            saveExpr(expr.rep)
            simplifierScreenSetup()

    def setExpr(e, v):
        e.text = v
        e.show()
        buttonFunc(e)

    simplifierScreen.fill(BACKGROUNDC)
    buttonW = 600
    buttonH = 100
    gap = 30
    start = (DIM[1]-buttonH)/2 - buttonH
    heading = pgu.Label(simplifierScreen, 'Boolean Simplification', (0, 0, DIM[0], DIM[1]/3), subtitleFont, BACKGROUNDC, TEXTC, align='center', justify='center')
    homeButton = pgu.Button(simplifierScreen, 'Home', (20, 20, 125, 70), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeScreen('main'))
    entry = pgu.Input(simplifierScreen, ((DIM[0]-buttonW-150-gap)/2, start, buttonW, buttonH), vLargeFont, [BACKGROUNDC, HIGHLIGHT1], TEXTC, BORDERC, text='Enter Expression')
    simplifyButton = pgu.Button(simplifierScreen, 'Simplify', ((DIM[0]-buttonW-150-gap)/2 + buttonW + gap, start, 150, buttonH), largeFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: buttonFunc(entry), actionButton=True)
    errorLabel = pgu.Label(simplifierScreen, '', ((DIM[0]-buttonW-150-gap)/2 - gap - 275, start, 275, buttonH), medFont, BACKGROUNDC, TEXTC, align='right')    
    stepsBox = pgu.ScrollableSurface(simplifierScreen, (DIM[0]-buttonW-150-gap)/2, start + buttonH + gap - 10, (buttonW+150+gap,  DIM[1]-(start+buttonH+gap-10+gap)), BACKGROUNDC, BORDERC, TEXTC, barWidth=10)
    h=0
    for i, step in enumerate(steps[:-1]):
        createPNG(step[1])
        tmp = pg.image.load(f'tmpimages\\tmp.png')
        tmp = tmp.convert()
        tmp.set_colorkey((255,255,255))
        tmpl = pgu.Label(stepsBox, f'{step[0]}: ', (0, h, stepsBox.showRect[2], 50), medFont, BACKGROUNDC, TEXTC)
        tmpI = pgu.ImageRect(stepsBox, tmp, 0, h + 50)
        h += tmp.get_height() + stepsBox.padding/2 + 50

    if len(steps) > 0:
        expr = parse.parse(steps[-1][1].rep)
    else:
        expr = None
    logicConvertButton = pgu.Button(simplifierScreen, 'Answer => Logic Gates', ((DIM[0]-buttonW-150-gap)/2 + buttonW + gap + 150 + gap , start, 275, buttonH), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: exprToLogic(expr, errorLabel))
    tableConvertButton = pgu.Button(simplifierScreen, 'Answer => Truth Table', ((DIM[0]-buttonW-150-gap)/2 + buttonW + gap + 150 + gap , start+buttonH+gap, 275, buttonH), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: tableConvert(expr, errorLabel))

    if loggedInAs != None:
        l = pgu.LayeredSurface(simplifierScreen, DIM, 3, pg.SRCALPHA)
        d = pgu.DropDown(simplifierScreen, l, (20, start + buttonH + gap - 10, 275,  buttonH), DIM[1]-(start+buttonH*2+gap+10), 'User Expressions', BACKGROUNDC, TEXTC, BACKGROUNDC, HIGHLIGHT1, BORDERC, medFont)
        s = pgu.ScrollableSurface(d, 0, 0, (270, DIM[1]-(start+buttonH*2+gap+15)), BACKGROUNDC, BORDERC, HIGHLIGHT1)
        exprs = getUserExprs()
        for i, v in enumerate(exprs):
            b = pgu.Button(s, v, (0, i*55, 230, 50), smallFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda v=v: setExpr(entry, v))
        saveExprButton = pgu.Button(simplifierScreen, 'Save Expression', ((DIM[0]-buttonW-150-gap)/2 + buttonW + gap + 150 + gap , start+(buttonH+gap)*2, 275, buttonH), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: saveExprWrapper(expr, errorLabel))

def loginScreenSetup(*args):
    loginScreen.clear()
    loginScreen.fill(BACKGROUNDC)
    buttonW = 600
    buttonH = 100
    gap = 30
    start = (DIM[1]-buttonH)/2 - 75
    heading = pgu.Label(loginScreen, 'Login', (0, 0, DIM[0], DIM[1]/3), titleFont, BACKGROUNDC, TEXTC, align='center', justify='center')
    homeButton = pgu.Button(loginScreen, 'Home', (20, 20, 125, 70), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeScreen('main'))
    uname = pgu.Input(loginScreen, ((DIM[0]-buttonW)/2, start, buttonW, buttonH), vLargeFont, [BACKGROUNDC, HIGHLIGHT1], TEXTC, BORDERC, text='Enter Username')
    passwd = pgu.Input(loginScreen, ((DIM[0]-buttonW)/2, start + buttonH + gap, buttonW, buttonH), vLargeFont, [BACKGROUNDC, HIGHLIGHT1], TEXTC, BORDERC, text='Enter Password')

    loginErrorLabel = pgu.Label(loginScreen, '', ((DIM[0]-buttonW)/2 - 350 - gap, start + buttonH*2.5 + gap*2, 350, buttonH), medFont, BACKGROUNDC, TEXTC, align='right')
    registerErrorLabel = pgu.Label(loginScreen, '', ((DIM[0]-buttonW)/2 + buttonW + gap, start + buttonH*2.5 + gap*2, 350, buttonH), medFont, BACKGROUNDC, TEXTC, align='left')
    
    loginButton = pgu.Button(loginScreen, 'Login', ((DIM[0]-buttonW)/2, start + buttonH*2 + gap*2 + buttonH/2, (buttonW-gap)/2, buttonH), vLargeFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: login(uname, passwd, loginErrorLabel))
    registerButton = pgu.Button(loginScreen, 'Register', ((DIM[0]-buttonW)/2 + (buttonW-gap)/2 + gap, start + buttonH*2 + gap*2 + buttonH/2, (buttonW-gap)/2, buttonH), vLargeFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: register(uname, passwd, registerErrorLabel))

def mainScreenSetup(*args):
    mainScreen.clear()
    mainScreen.fill(BACKGROUNDC)
    buttonW = 600
    buttonH = 100
    gap = 40
    start = (DIM[1]-buttonH)/2 - buttonH + 75
    heading = pgu.Label(mainScreen, 'b L o g i c.', (0, 0, DIM[0], DIM[1]/3), titleFont, BACKGROUNDC, TEXTC, align='center', justify='center')
    simplifierButton = pgu.Button(mainScreen, 'Simplifier', ((DIM[0]-buttonW)/2, start, buttonW, buttonH), largeFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeScreen('simplifier'))
    logicSimButton = pgu.Button(mainScreen, 'Logic Simulator', ((DIM[0]-buttonW)/2, start + (buttonH + gap), buttonW, buttonH), largeFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeScreen('logic'))
    tableButton = pgu.Button(mainScreen, 'Truth Table', ((DIM[0]-buttonW)/2, start + (buttonH + gap)*2, buttonW, buttonH), largeFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeScreen('table'))
    syntaxButton = pgu.Button(mainScreen, 'Syntax Help', (DIM[0]-20-200, 20, 200, buttonH*0.8), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeScreen('syntaxHelp'))
    
    if curTheme == 'light':
        themeButton = pgu.Button(mainScreen, 'Dark Mode', (DIM[0]-20-200, DIM[1]-20-buttonH*0.8, 200, buttonH*0.8), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: setTheme('dark'))
    elif curTheme == 'dark':
        themeButton = pgu.Button(mainScreen, 'Light Mode', (DIM[0]-20-200, DIM[1]-20-buttonH*0.8, 200, buttonH*0.8), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: setTheme('light'))
    
    if loggedInAs == None:
        loginButton = pgu.Button(mainScreen, 'Login', (20, 20, 200, buttonH*0.8), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: changeScreen('login'))
    else:
        userLabel = pgu.Label(mainScreen, loggedInAs, (20, DIM[1]-buttonH*0.8-20, 200, buttonH*0.8), medFont, BACKGROUNDC, TEXTC, border=True, borderColour=BORDERC, align='center')
        logoutButton = pgu.Button(mainScreen, 'Log Out', (20, 20, 200, buttonH*0.8), medFont, BACKGROUNDC, HIGHLIGHT1, TEXTC, BORDERC, lambda: logout())

def createPNG(step):
    global loading
    latex = step.getLatex()
    link = f'https://latex.codecogs.com/png.image?\\dpi{{300}}{latex}'
    #r = requests.get(link)
    #with open(f'tmpimages\\tmp.png', 'wb') as f:
    #    f.write(r.content)
    f = open('tmpimages\\tmp.png', 'wb')
    f.write(urllib.request.urlopen(link).read())
    f.close()

def simplify(s):
    if validateExpression(s):
        ss = parse.parse(s)
        steps = ss.simplify()
        setLoading(simplifierScreenSetup, [], steps=steps)
        return True
    else:
        return False


def drawTable(s, tb, errorLabel):
    tb.removeAll()
    totalW = tb.showRect[2]
    varss = s.replace('(','').replace(')','').replace('¬','').replace('*','').replace('+','').replace('1','').replace('0','')
    varss = list(set(list(varss)))
    varss = sorted(varss)
    noOfVars = len(varss)
    if noOfVars > 6:
        errorLabel.text = 'Too Many Variables'
        return
    maxLen = len(bin(2**noOfVars - 1)[2:])
    cellW = totalW//(noOfVars+3)
    cellH = totalW//(8)
    new = s
    for i, v in enumerate(varss):
        pgu.Label(tb, v, ((cellW-3)*i, 0, cellW, cellH), medFont, HIGHLIGHT2, TEXTC, align='centre', border=True, borderColour=BORDERC)
    pgu.Label(tb, 'Output', ((cellW-3)*noOfVars, 0, cellW*2, cellH), medFont, HIGHLIGHT2, TEXTC, align='centre', border=True, borderColour=BORDERC)
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
            pgu.Label(tb, vals[x], ((cellW-3)*x, cellH - 3 + (cellH-3)*y, cellW, cellH), medFont, BACKGROUNDC, TEXTC, align='centre', border=True, borderColour=BORDERC)
        pgu.Label(tb, output, ((cellW-3)*len(vals), cellH - 3 + (cellH-3)*y, cellW*2, cellH), medFont, BACKGROUNDC, TEXTC, align='centre', border=True, borderColour=BORDERC)


def exprToLogic(expr, errorLabel):
    if expr == None:
        errorLabel.text = 'No Answer'
        return

    gates, links, switches, depth, depths, heights = exprToGates(expr, [], [], [], 0, [] ,{})
    gates, links, depths, heights, switches = resolveDuplicates(gates, links, switches, depths, heights)
    # print(gates, links, depths, heights, switches)
    coords = getCoords(gates, links, depths, heights)
    # print(f'P={coords}\nH={[wid.HEIGHTS[i] for i in gates]}')
    plotLogicFromExpr(gates, links, coords, switches)

def exprToGates(expr, gates=[], links=[], switches=[], depth=0, depths=[], heights={}): 
    depth += 1
    ind = len(gates)
    if isinstance(expr, Sum):
        t1 = expr.terms[0]
        t2 = expr.terms[1]
        gates.append(wid.OrElement)
        links.append([ind+1, ind+2])
        switches.append(None)
        depths.append(depth)
        gates, links, switches, depth, depths, heights = exprToGates(t1, gates, links, switches, depth, depths, heights)
        depth -= 1 
        newind = len(gates)
        links[ind][1] = newind
        gates, links, switches, depth, depths, heights = exprToGates(t2, gates, links, switches, depth, depths, heights)
        depth -= 1
        if depth in heights: heights[depth] += 2
        else: heights[depth] = 2
        return gates, links, switches, depth, depths, heights
    elif isinstance(expr, Product):
        t1 = expr.terms[0]
        t2 = expr.terms[1]
        gates.append(wid.AndElement)
        links.append([ind+1, ind+2])
        switches.append(None)
        depths.append(depth)
        gates, links, switches, depth, depths, heights = exprToGates(t1, gates, links, switches, depth, depths, heights)
        depth -= 1 
        newind = len(gates)
        links[ind][1] = newind
        gates, links, switches, depth, depths, heights = exprToGates(t2, gates, links, switches, depth, depths, heights)
        depth -= 1
        if depth in heights: heights[depth] += 2
        else: heights[depth] = 2
        return gates, links, switches, depth, depths, heights
    elif isinstance(expr, Not):
        t1 = expr.terms[0]
        gates.append(wid.NotElement)
        links.append([ind+1])
        switches.append(None)
        depths.append(depth)
        gates, links, switches, depth, depths, heights = exprToGates(t1, gates, links, switches, depth, depths, heights)
        depth -= 1 
        if depth in heights: heights[depth] += 1
        else: heights[depth] = 1
        return gates, links, switches, depth, depths, heights
    elif isinstance(expr, Var):
        if expr.terms[0] == '0':
            gates.append(wid.LowElement)
        elif expr.terms[0] == '1':
            gates.append(wid.HighElement)
        else:
            gates.append(wid.SwitchElement)
        switches.append(expr.terms[0])
        links.append([None])
        depths.append(depth)
        if depth in heights: heights[depth] += 1
        else: heights[depth] = 1
        return gates, links, switches, depth, depths, heights
    else:
        t1 = expr.terms[0]
        gates.append(wid.BulbElement)
        links.append([ind+1])
        switches.append(None)
        depths.append(depth)
        gates, links, switches, depth, depths, heights = exprToGates(t1, gates, links, switches, depth, depths, heights)
        depth -= 1 
        if depth in heights: heights[depth] += 1
        else: heights[depth] = 1
        return gates, links, switches, depth, depths, heights

def resolveDuplicates(gates, links, switches, depths, heights):
    gateIDs = [i if switches[i] == None else switches[i] for i in range(len(switches))]
    newSw = []
    count = 0
    for i, v in enumerate(gateIDs):
        if v not in newSw:
            newSw.append(v)
        else:
            if depths[i-count]>depths[newSw.index(v)-count]:
                ind = newSw.index(v)
                newSw = newSw[:ind] + newSw[ind+1:]
                newSw.append(v)
            else:
                ind = i-count
            heights[depths[ind]] -= wid.HEIGHTS[gates[ind]]
            gates = gates[:ind] + gates[ind+1:]
            switches = switches[:ind] + switches[ind+1:]
            links = links[:ind] + links[ind+1:]
            depths = depths[:ind] + depths[ind+1:]
            count += 1
    for i in range(len(links)):
        for j in range(len(links[i])):
            if links[i][j] != None:
                val = gateIDs[links[i][j]]
                if val != None:
                    links[i][j] = newSw.index(val)
    return gates, links, depths, heights, switches

def getCoords(gates, links, depths, heights):
    coords = []
    doneHeights = {k:0 for k in heights.keys()}
    for i in range(len(gates)):
        depth = depths[i]
        x = 79 - 2*(depth-1)
        y = 39 - round(heights[depth]/2) + doneHeights[depth]
        doneHeights[depth] += wid.HEIGHTS[gates[i]]
        coords.append((x, y))
    return coords
        
def plotLogicFromExpr(gates, links, coords, switches):
    changeScreen('logic')
    gateElements = []
    for i in range(len(gates)):
        x, y = coords[i]
        gate = gates[i]
        cell = sandboxWindow.cells[y][x]
        try:
            if gate == wid.SwitchElement:
                cell.element = gate(cell, name=switches[i])
            else:
                cell.element = gate(cell)
        except OverflowError:
            cell.element = None
        gateElements.append(cell.element)

    for i in range(len(gates)):
        x, y = coords[i]
        element = sandboxWindow.cells[y][x].element
        if links[i][0] != None and element != None:
            for ind, l in enumerate(links[i]):
                n1 = element.inputs[ind]
                n2 = gateElements[l].outputs[0]
                n2.active = 1
                n1.active = 1
                n1.colour = n2.colour
                n1.setBackreference(n2)
                n1.line = wid.Line(n2, n1, n1.colour, sandboxWindow.lineC)
                n2.line = n1.line
                sandboxWindow.pathLines.append(n1.line)


def exprToSimplify(expr, errorLabel):
    if expr == None:
        errorLabel.text = 'No Answer'
        return
    changeScreen('simplifier')
    simplify(expr.rep)


def gatesToExpr():
    circuits = []
    for row in sandboxWindow.cells:
        for cell in row:
            if type(cell.element) == wid.BulbElement and cell.backreference == cell:
                c = buildExpression(cell.element, {})
                if c != None: circuits.append(c[0])
    if len(circuits) > 0:
        return circuits
    else:
        return None

def buildExpression(element, count={}):
    if isinstance(element, wid.BulbElement):
        if all([i.line != None for i in element.inputs]):
            n1 = element.inputs[0].line.node1.element
            obj, count = buildExpression(n1, count)
            return Expression(obj), count
    elif isinstance(element, wid.AndElement):
        if all([i.line != None for i in element.inputs]):
            n1 = element.inputs[0].line.node1.element
            obj1, count = buildExpression(n1, count)
            n2 = element.inputs[1].line.node1.element
            obj2, count = buildExpression(n2, count)
            return Product(obj1, obj2), count
    elif isinstance(element, wid.OrElement):
        if all([i.line != None for i in element.inputs]):
            n1 = element.inputs[0].line.node1.element
            obj1, count = buildExpression(n1, count)
            n2 = element.inputs[1].line.node1.element
            obj2, count = buildExpression(n2, count)
            return Sum(obj1, obj2), count
    elif isinstance(element, wid.NotElement):
        if all([i.line != None for i in element.inputs]):
            n1 = element.inputs[0].line.node1.element
            obj, count = buildExpression(n1, count)
            return Not(obj), count
    elif isinstance(element, wid.NandElement):
        if all([i.line != None for i in element.inputs]):
            n1 = element.inputs[0].line.node1.element
            obj1, count = buildExpression(n1, count)
            n2 = element.inputs[1].line.node1.element
            obj2, count = buildExpression(n2, count)
            return Not(Product(obj1, obj2)), count
    elif isinstance(element, wid.NorElement):
        if all([i.line != None for i in element.inputs]):
            n1 = element.inputs[0].line.node1.element
            obj1, count = buildExpression(n1, count)
            n2 = element.inputs[1].line.node1.element
            obj2, count = buildExpression(n2, count)
            return Not(Sum(obj1, obj2)), count
    elif isinstance(element, wid.XorElement):
        if all([i.line != None for i in element.inputs]):
            n1 = element.inputs[0].line.node1.element
            obj1, count = buildExpression(n1, count)
            n2 = element.inputs[1].line.node1.element
            obj2, count = buildExpression(n2, count)
            return Product(Sum(obj1, obj2), Sum(Not(obj1), Not(obj2))), count
    elif isinstance(element, wid.SwitchElement):
        if element not in count: 
            letter = chr(65+len(count))
            count[element] = letter
        else:
            letter = count[element]
        return Var(letter), count
    elif isinstance(element, wid.HighElement):
        return Var('1'), count
    elif isinstance(element, wid.LowElement):
        return Var('0'), count


def register(uname, passwd, errorLabel):
    if uname.text in blank and passwd.text in blank:
        errorLabel.text = 'Username and Password are blank'
        return
    elif uname.text in blank:
        errorLabel.text = 'Username is blank'
        return
    elif passwd.text in blank:
        errorLabel.text = 'Password is blank'
        return
    else:
        errorLabel.text = ''
    curNames = sql.runCommand('user_data', 'SELECT uname FROM login')
    curNames = [i[0] for i in curNames]
    if uname.text in curNames:
        errorLabel.text = 'Username Taken'
    else:
        errorLabel.text = ''
        sql.insertUser('user_data', uname.text, str(hashlib.sha256(passwd.text.encode('utf-8')).hexdigest()))

def login(uname, passwd, errorLabel):
    global loggedInAs
    if uname.text == '' and passwd.text == '':
        errorLabel.text = 'Username and Password are blank'
        return
    elif uname.text == '':
        errorLabel.text = 'Username is blank'
        return
    elif passwd.text == '':
        errorLabel.text = 'Password is blank'
        return
    else:
        errorLabel.text = ''
    curNames = sql.runCommand('user_data', 'SELECT uname FROM login')
    curNames = [i[0] for i in curNames]
    if uname.text in curNames:
        passwdHash = str(hashlib.sha256(passwd.text.encode('utf-8')).hexdigest())
        trueHash = sql.runCommand('user_data', f'SELECT pass FROM login WHERE uname="{uname.text}"')[0][0]
        if passwdHash == trueHash:
            loggedInAs = uname.text
            changeScreen('main')
        else:
            errorLabel.text = 'Incorrect Password'
    else:
        errorLabel.text = 'No Such Username'

def logout():
    global loggedInAs
    loggedInAs = None
    mainScreenSetup()

def getUserExprs():
    exprs = sql.runCommand('user_data', f'SELECT expr FROM expressions WHERE uname="{loggedInAs}"')
    exprs = [i[0] for i in exprs]
    return exprs

def saveExpr(expr):
    sql.insertExpression('user_data', loggedInAs, expr)


def setLoading(func, *args, **kwargs):
    global loading
    loading = (func, args, kwargs)

def setTheme(theme):
    global curTheme, BACKGROUNDC, HIGHLIGHT1, HIGHLIGHT2, TEXTC, BORDERC
    curTheme = theme
    if theme == 'dark':
        BORDERC = (199, 81, 70)#testc[3]
        BACKGROUNDC = testc[1]
        HIGHLIGHT1 = testc[2]
        HIGHLIGHT2 = testc[3]
        TEXTC = testc[7]

    elif theme == 'light':
        BORDERC = (199, 81, 70)#testc[3]
        BACKGROUNDC = testc[8]
        HIGHLIGHT1 = testc[6]
        HIGHLIGHT2 = testc[7]
        TEXTC = testc[2]

    try:
        mainScreenSetup()
    except NameError:
        pass


pg.init()
pg.font.init()


smallFont = pg.font.SysFont('Calibri', 16)
smallMedFont = pg.font.SysFont('Calibri', 20)
medFont = pg.font.SysFont('Calibri', 24)
largeFont = pg.font.SysFont('Calibri', 36)
vLargeFont = pg.font.SysFont('Calibri', 48)
subtitleFont = pg.font.SysFont('Calibri', 86)
titleFont = pg.font.SysFont('Calibri', 121)

DIM = (1450, 725)

testc = [(0.05+0.1*i, 0.05+0.1*i, 0.1*(i+1)) for i in range(10)]
testc = [[round(k*255) for k in i] for i in testc]
blank = ['', 'Enter Username', 'Enter Password']

loggedInAs = None

loadingFrame = 0
loading = None

toRemove = []

curTheme = 'light'

setTheme(curTheme)

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
loginScreen = pgu.Screen(DIM)
loginScreenSetup()
logicHelpScreen = pgu.Screen(DIM)
logicHelpScreenSetup()
syntaxHelpScreen = pgu.Screen(DIM)
syntaxHelpScreenSetup()

loadingOverlay = pg.Surface(DIM, pg.SRCALPHA)
loadingOverlay.fill((255, 255, 255, 150))
loadingLabel = pgu.Label(loadingOverlay, 'Loading . . . ', (0,0,DIM[0],DIM[1]), subtitleFont, (255,255,255), TEXTC, align='center', addSelf=False)
loadingOverlay.blit(loadingLabel.label, loadingLabel.label_rect)

curScreen = mainScreen
run = True
while run:
    curScreen.fill(BACKGROUNDC)
    curScreen.redraw()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        curScreen.event_update(event)
    curScreen.update()



    clock.tick(1000)
    display.blit(curScreen, (0,0))

    if loading != None:
        if loadingFrame == 0:
            display.blit(loadingOverlay, (0,0))
            loadingFrame += 1
        elif loadingFrame == 1:
            loading[0](*loading[1], **loading[2])
            loading = None
            loadingFrame = 0
            loading = None

    pg.display.update()

pg.quit()
quit()

