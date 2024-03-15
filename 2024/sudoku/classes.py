import pygame as py
from pygame.locals import *
import json
py.init()
def load_settings():
    with open('settings.json') as f:
        return json.load(f)


class Game:
    def __init__(self):
        self.update_settings()


    def update_settings(self):
        self.settings = load_settings()
        self.WindowSize = self.settings["WindowSize"]
        self.FPS = self.settings["FPS"]
        self.flags = DOUBLEBUF | HWSURFACE | HWACCEL | FULLSCREEN if self.settings["Fullscreen"] else 0
        self.surf = py.display.set_mode(self.WindowSize ,self.flags)
        self.clock = py.time.Clock()
        self.running = True
        self.font = py.font.Font(None, 36)

        self.SudokuGrid = SudokuGrid(self)

    def update(self):
        self.surf.blit(self.SudokuGrid.localSurface, (0,0))
        py.display.update()
        self.clock.tick(self.FPS)

class Square(py.sprite.Sprite):
    def __init__(self, position_index, group, game, sudokuSurface):
        super().__init__(group)
        self.image = py.Surface([sudokuSurface.get_width()//9, sudokuSurface.get_height()//9])
        self.size = [sudokuSurface.get_width()//9, sudokuSurface.get_height()//9]

        self.rect = py.rect.Rect([position_index[0]*self.size[0], position_index[1]*self.size[1]], self.size)
        self.sudokuSurface = sudokuSurface
        self.color = "white"

    def draw(self):
        py.draw.rect(self.sudokuSurface, self.color, self.rect)

class SudokuGrid:
    def __init__(self, game):
        self.game = game
        self.localSurface = py.Surface((game.WindowSize[1], game.WindowSize[1]))
        self.squareGroup = py.sprite.Group()
        self.grid = [[0 for i in range(9)] for j in range(9)]
        self.empty_initialization()

        self.update_local_surf()
        #self.selected = None
        #self.load()
        #self.update()
    def empty_initialization(self):
        self.grid = [[Square([i,j], self.squareGroup, self.game, self.localSurface) for i in range(9)] for j in range(9)]
    def load(self):
        with open('grid.json') as f:
            self.grid = json.load(f)

    def update_local_surf(self):
        for i in range(9):
            for j in range(9):
                self.grid[i][j].draw()

    def update_ll(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.draw_number(i, j, self.grid[i][j])

    def draw_number(self, x, y, number):
        text = game.font.render(str(number), True, (0, 0, 0))
        game.surf.blit(text, (x*50, y*50))