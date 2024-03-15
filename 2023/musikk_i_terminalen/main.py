import pygame as py
from pygame.locals import *
import objects



def songPrint():
    for song in objects.songs:
        print(f"{objects.songs.index(song)+1}. {song.searchWord}  ")

def velgSang():
    validChoice = False
    print("Skriv index eller låtnavn for å spille av")
    songPrint()
    while not validChoice:
        valg = input("Skriv valg:   ")
        try:
            valg = int(valg)
            validChoice=True
            print(valg)
            if valg <= len(objects.songs):
                return objects.songs[valg-1]
        except ValueError:
            print("hei")
            valg = str(valg)
            validChoice=True
            for song in objects.songs:
                if valg == song.searchWord:
                    return song

mixer = py.mixer
mixer.init()
valgtLåt = False

while True:
    if not valgtLåt:
        valgtSang = velgSang()
        valgtLåt = True
        print(valgtSang)
        mixer.music.load(valgtSang.file)
        mixer.music.play()


    pause = input("Pause(p), Unpause(o), Quit(q):   ")
    match pause.lower():
        case "o":
            mixer.music.unpause()
        case "p":
            mixer.music.pause()
        case "q":
            py.quit()
            quit()
        case _:
            print("Ugyldig input")







