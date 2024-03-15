from pysunk import *
import pygame as py
from pygame.locals import *

py.init()
surf = py.display.set_mode((800,600), HWSURFACE|DOUBLEBUF, 16)

game = GameLogic(30)

bgColor = (255,255,255)
p = KinematicBody([100,100], 0.9, rescale_factored(py.image.load("player.png"),[0.05,0.05]), 1, game)
r1 = py.rect.Rect(100,100, 100,100)
r2 = py.rect.Rect(200,200, 100,100)
l = 0
x = 0
while 1:

    surf.fill(bgColor)

    for e in py.event.get():
        if e.type == QUIT:
            quit()
            exit()
    ks = py.key.get_pressed()
    if ks[K_UP]: p.add_velocity([0,-10])
    if ks[K_DOWN]: p.add_velocity([0,10])
    if ks[K_LEFT]: p.add_velocity([-10,0])
    if ks[K_RIGHT]: p.add_velocity([10,0])




    game.update(surf, py.event.get())

    p.update(surf)
    py.display.update()
    py.time.Clock().tick(30)
