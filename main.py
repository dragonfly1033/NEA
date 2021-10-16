import colorsys
import pygame as pg
from math import sqrt, sin, cos, radians, degrees, pi
import pygameutil as pgu
from random import randint as rand


def test(display, p1, p2, p1d, p2d, res):
    p1 = (p1.x, p1.y)
    p2 = (p2.x, p2.y)
    l = bezier(p1 ,p2, p1d, p2d, res)
    pg.draw.lines(display, (255, 255, 255), False, l, 1)


def bezier(p0, p3, p0dir, p3dir, res):
    halfXdiff = 0.5*(p3[0] - p0[0])
    halfYdiff = 0.5*(p3[1] - p0[1])
    p1 = (p0[0] + p0dir[0]*halfXdiff, p0[1] + p0dir[1]*halfYdiff)
    p2 = (p3[0] + p3dir[0]*halfXdiff, p3[1] + p3dir[1]*halfYdiff)

    ps = []
    t = 0
    for i in range(res+1):
        q0 = list(map(lambda x: ((1-t)**3)*x, p0))
        q1 = list(map(lambda x: ((1-t)**2)*t*3*x, p1))
        q2 = list(map(lambda x: ((1-t)**1)*t*t*3*x, p2))
        q3 = list(map(lambda x: t*t*t*x, p3))
        nx = q0[0] + q1[0] + q2[0] + q3[0]
        ny = q0[1] + q1[1] + q2[1] + q3[1]
        ps.append((nx, ny))

        t += 1/res
    return ps

def mainScreenSetup():
    global alpha1, dp1, dp3, dp2, dp4
    mainScreen.fill((0, 0, 0))
    alpha1 = pgu.LayeredSurface(mainScreen, DIM, zlayer=6, flags=pg.SRCALPHA)
    e1 = pgu.Input(mainScreen, (100, 100, 300, 100), medFont, [DARKGREY, LIGHTGREY], VDARKGREY, RED, zlayer=0)
    l1 = pgu.Label(mainScreen, 'More poop', (100, 400, 300, 100), medFont, LIGHTGREY, VDARKGREY, align='center', justify='centre', zlayer=0)
    dp1 = pgu.DraggablePoint(alpha1, 500, 400, 10, RED, VDARKGREY)
    dp2 = pgu.DraggablePoint(alpha1, 600, 400, 10, RED, VDARKGREY)
    dp3 = pgu.DraggablePoint(alpha1, 700, 400, 10, RED, VDARKGREY)
    dp4 = pgu.DraggablePoint(alpha1, 800, 400, 10, RED, VDARKGREY)
    dr1 = pgu.DraggableRect(alpha1, 900, 400, 200, 100, RED, VDARKGREY)
    b1 = pgu.Button(mainScreen, 'poop pee', (100, 300, 300, 100), medFont, DARKGREY, LIGHTGREY, VDARKGREY, RED, lambda: test(alpha1, dp1, dp3, (0, 1), (0, -1), 15), zlayer=0)


pg.init()
pg.font.init()

medFont = pg.font.SysFont('Calibri', 36)
DIM = (1520, 600)
LIGHTGREY = (200, 200, 200)
DARKGREY = (100, 100, 100)
VDARKGREY = (50, 50, 50)
RED = (200, 0, 0)
NORTH = (0, 1)
SOUTH = (0, -1)
EAST = (1, 0)
WEST = (-1, 0)

display = pg.display.set_mode(DIM)
clock = pg.time.Clock()
mainScreen = pgu.Screen(DIM)
mainScreenSetup()


curScreen = mainScreen
run = True
while run:
    curScreen.fill(0)
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

