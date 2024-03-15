import pygame as py
from pygame.locals import *
from classes import QuizHandler, WW, WH

py.init()


py.display.set_caption('Jasunks Historiequiz')
surf = py.display.set_mode((WW, WH))

qh = QuizHandler(surf)
qh.get_question()
while 1:
    surf.fill((0, 0, 0))
    for e in py.event.get():
        if e.type == QUIT:
            py.quit()
            exit()

    qh.update()
    py.display.update()

