import random


class Pipe():
    def __init__(self, width, height, blank, distance, speed, img, window_width, window_height, game_display):
        self.width = width
        self.height = height
        self.blank = blank
        self.distance = distance
        self.speed = speed
        self.surface = img
        self.game_display = game_display
        self.window_height = window_height
        self.ls = []
        for i in range(3):
            x = window_width + i*self.distance
            y = random.randrange(60, self.window_height - self.blank - 60, 20)
            self.ls.append([x, y])

    def draw(self):
        for i in range(3):
            self.game_display.blit(
                self.surface, (self.ls[i][0], self.ls[i][1] - self.height))
            self.game_display.blit(
                self.surface, (self.ls[i][0], self.ls[i][1] + self.blank))

    def update(self):
        for i in range(3):
            self.ls[i][0] -= self.speed

        if self.ls[0][0] < -self.width:
            self.ls.pop(0)
            x = self.ls[1][0] + self.distance
            y = random.randrange(60, self.window_height - self.blank - 60, 10)
            self.ls.append([x, y])
