import pygame as py
from pygame.locals import *

WW, WH = 1800, 1000
leftSidePadding = 400
flags = DOUBLEBUF| HWACCEL  | HWSURFACE | FULLSCREEN | SCALED
FPS = 30



def returnFont(size):
    return py.font.Font("sprites/PixCon.ttf", int(size))

SISTEORD = [
    "Faen eg e keen på nokken seigmen as",
    "PEW PEW PEW MADAFAKKA",
    "Eg elsker mamma",
    "Eg elsker pappa",
    "Plis ikke drep meg :(",
    "Eg angrer på alt",
    "Eg angrer på ingenting",
    "Eg angrer på at eg ikke angrer på alt",
    "Se pappa, trengte ikke lappen",
    "Eg har ikke lappen",
    "Eg har ikke bil",
    "Faen, skulle coppet livsforsikring",
    "Si wallah du dreper meg",
    "Main character moment da",
    "Faen",
    "Nokken bør skrive bok om meg",
    "Dette gikk ikke veien as",
    "Om noen hører meg, spill slowdive på begravelsen min",
    "Eg har ikke råd til begravelse",
    "Shit happends",
    "Fakkass",
    "Fortjener dette lowkey as",
    "Slipper studielån iallefall",
    "Søren saltklype",
    "Fis",
    "Fanken",
    "Gresk yoghurt med revet gulrot er ganske og",
    "Penispumpe"

]

TILFELDIGNAVN = ["Rolf", "Frank", "Karl", "Fjomp", "Karsten", "Kornelius", "Albert", "Kurt", "Jens", "Ola", "Skalleknuseren", "Glont", "Sivert", "Jo-Bjo", "Rekesamleren", "Darth Reidar", "Kvantitativ metode", "Gnom", "Rasmus", "Fredrik", "Frederik", "Theodor", "Arun", "Bebb", "Tor", "Eirk", "Erickman", "Gelemauren", "Olav", "Silfo", "Ola", "Geir", "Walter Schreifels", "Ariana Grande", "Walter White", "Obama", "Donald Trump", "Ye West", "Supermann", "Glontikus", "Skillingsbolle", "Captain Jack Sparrow", "Luke Skywalker", "Meitemarkspiser", "Paul"
                 "Ass Kill"]