import random
import pygame as py
from pygame.locals import *
from classes import *
import cProfile
from settings import *


py.init()
surf = py.display.set_mode((WW, WH),flags, 16)

game = Game()
py.mouse.set_cursor((8,8),(0,0),(0,0,0,0,0,0,0,0),(0,0,0,0,0,0,0,0))

while 1:

    game.update(surf, py.mouse.get_pos(), py.event.get())
    py.display.update()
    py.time.Clock().tick(FPS)
