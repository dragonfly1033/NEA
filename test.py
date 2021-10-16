import pygame as pg
from math import sin, cos, pi


pg.init()
pg.font.init()

smallFont = pg.font.SysFont('Calibri', 12)
medFont = pg.font.SysFont('Calibri', 24)
largeFont = pg.font.SysFont('Calibri', 36)
DIM = (1520, 600)

display = pg.display.set_mode(DIM)
redS = pg.Surface(DIM)
redS.fill((255, 0, 0))
alphaS = pg.Surface(DIM, flags=pg.SRCALPHA)
alphaS.fill((0, 255, 0, 0))

clock = pg.time.Clock()

run = True
while run:
    display.fill(0)
    alphaS.fill(0)
    pg.draw.circle(display, (255, 255, 0), (400, 400), 50)
    pg.draw.circle(redS, (255, 255, 0), (400, 600), 50)
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

    x = 100*cos(pg.time.get_ticks()*0.01 - 0) + 100
    y = 100*sin(pg.time.get_ticks()*0.01 + 00) + 100
    pg.draw.circle(alphaS, (0, 0, 255, 150), (x, y), 10)

    clock.tick(300)
    display.blit(alphaS, (0,0))
    #display.blit(redS, (0,0))
    pg.display.update()

pg.quit()
quit()