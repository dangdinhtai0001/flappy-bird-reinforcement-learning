import pygame


class Score():
    def __init__(self, window_width, game_display, rect_collision):
        self.score_ = 0
        self.add_score = True
        self.game_display = game_display
        self.window_width = window_width
        self.rect_collision = rect_collision

    def draw(self):
        font = pygame.font.SysFont('consolas', 40)
        score_suface = font.render(str(self.score_), True, (0, 0, 0))
        text_size = score_suface.get_size()
        self.game_display.blit(
            score_suface, (int((self.window_width - text_size[0])/2), 100))

    def update(self, bird, pipes):
        collision = False
        for i in range(3):
            rect_column = [pipes.ls[i][0] + pipes.width, pipes.ls[i][1], 1, pipes.blank]
            rect_bird = [bird.x, bird.y, bird.width, bird.height]
            if self.rect_collision(rect_bird, rect_column) == True:
                collision = True
                break
        if collision == True:
            if self.add_score == True:
                self.score_ += 1
            self.add_score = False
        else:
            self.add_score = True
