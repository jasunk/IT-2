import json
import pygame as py
from pygame.locals import *
import random


WW, WH = 1000, 800
class QuizHandler:
    def __init__(self, surf):
        self.question = None
        self.options = []
        self.correct = None
        self.index = 0
        self.data = self.read_json("questions.json")
        self.data = random.sample(self.data, len(self.data))
        self.score = {"correct": 0, "wrong": 0}

        self.surf = surf
        self.next_button = NextButton("Next", 20, (WW/2, 650), (255, 255, 255), self.surf, 0, 0, "pink", self)

    def read_json(self, file: str) -> list:
        with open(file, "r") as f:
            return json.load(f)

    #get_question() updates the self.question, self.options and self.correct attributes, and shows expected type of Label
    def get_question(self) -> None:
        data = self.data[self.index]
        self.options = []
        self.question = Label(data["Question"], 30, (WW/2, 100), (255, 255, 255), self.surf)

        self.correct = data["Options"][data["Answer_index"]]
        shuffled_options = random.sample(data["Options"], len(data["Options"]))
        correct_index = shuffled_options.index(self.correct)


        for option in shuffled_options:
            index = shuffled_options.index(option)
            self.options.append(
                OptionsButton(
                    option,
                    20,
                    (WW/2, 250 + (shuffled_options.index(option) * 100)),
                    (255, 255, 255),
                    self.surf,
                    index,
                    correct_index,
                    "blue",
                    self
                )
            )
    def next_question(self) -> None:

        if len(self.data) == self.index + 1:
            self.index = 0
            self.get_question()
            return
        self.index += 1
        self.get_question()
    def update(self) -> None:

        #draw stats
        correct = Label(f"Correct: {self.score['correct']}", 20, (WW/2, WH-75), (255, 255, 255), self.surf)
        wrong = Label(f"Wrong: {self.score['wrong']}", 20, (WW/2, WH-50), (255, 255, 255), self.surf)
        correct.draw()
        wrong.draw()

        self.question.draw()
        self.next_button.update()
        for o in self.options:
            o.update()


class Label(py.font.Font):
    def __init__(self, text, size, pos, color, surf):
        self.text = text
        self.size = size

        self.color = color
        self.surf = surf
        self.font = py.font.Font("Protest_Strike/ProtestStrike-Regular.ttf", self.size)
        self.render = self.font.render(self.text, 1, self.color)
        self.rect = self.render.get_rect()
        self.rect.center = pos


    def draw(self) -> None:
        self.render = self.font.render(self.text, 1, self.color)
        self.surf.blit(self.render, self.rect)

class Button(Label):
    def __init__(self, text, size, pos, color, screen, index, correct_index, bg_color="red"):
        super().__init__(text, size, pos, color, screen)
        self.clicked = False
        self.hovered = False
        self.tg_txt_color = self.color
        self.tg_bg_color = bg_color
        self.bg_color = self.tg_bg_color
        self.index = index
        self.correct_index = correct_index
        self.mouseDown = False


    def draw(self) -> None:
        py.draw.rect(self.surf, self.bg_color, py.rect.Rect(self.rect.x-10, self.rect.y-10, self.rect.width+20, self.rect.height+20))
        super().draw()

    def update(self) -> None:

        self.hovered = self.rect.collidepoint(py.mouse.get_pos())
        if self.hovered:
            self.bg_color = self.tg_txt_color
            self.color = self.tg_bg_color


        else:
            self.bg_color = self.tg_bg_color
            self.color = self.tg_txt_color
        self.draw()


class OptionsButton(Button):
    def __init__(self, text, size, pos, color, screen, index, correct_index, bg_color, ref):
        super().__init__(text, size, pos, color, screen, index, correct_index, bg_color)
        self.ref = ref
    def update(self) -> None:
        self.hovered = self.rect.collidepoint(py.mouse.get_pos())
        if self.hovered:
            self.bg_color = self.tg_txt_color
            self.color = self.tg_bg_color
            if py.mouse.get_pressed()[0] and not self.mouseDown:
                self.mouseDown = True
                if self.index == self.correct_index:
                    print("Correct")
                    self.ref.score["correct"] += 1
                    self.tg_bg_color = "green"
                    self.tg_txt_color = "black"

                else:
                    self.ref.score["wrong"] += 1
                    print("Wrong")
                    self.tg_bg_color = "red"
        else:
            self.bg_color = self.tg_bg_color
            self.color = self.tg_txt_color
        self.draw()

class NextButton(Button):
    def __init__(self, text, size, pos, color, screen, index, correct_index, bg_color, gameRef):
        super().__init__(text, size, pos, color, screen, index, correct_index, bg_color)
        self.gameRef = gameRef

    def update(self) -> None:
        self.hovered = self.rect.collidepoint(py.mouse.get_pos())
        if self.hovered:
            self.bg_color = self.tg_txt_color
            self.color = self.tg_bg_color
            if py.mouse.get_pressed()[0]:
                if not self.mouseDown:
                    self.mouseDown = True
                    self.gameRef.next_question()
            else:
                self.mouseDown = False
        else:
            self.bg_color = self.tg_bg_color
            self.color = self.tg_txt_color
        self.draw()
