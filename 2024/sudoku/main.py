import pygame as py
from pygame.locals import *
from classes import Game


game = Game()



while 1:
    for e in py.event.get():
        if e.type == QUIT:
            py.quit()
            exit()

    game.update()