import pygame as py
class Song():
    py.mixer.init()
    def __init__(self, searchWord, artist, file):
        self.file = file
        self.artist = artist
        self.searchWord = searchWord
        self.playing = False
    def __str__(self):
        return f"Now playing {self.searchWord} by {self.artist}"
songs = [
    Song("My own summer (shove it)","Deftones", "sanger/Deftones - My Own Summer (Official Music Video) [HD Remaster].mp3"),
    Song("Mr. Blue Sky","Electric Light Orchestra", "sanger/Mr. Blue Sky.mp3")
]