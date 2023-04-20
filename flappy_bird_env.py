from bird import Bird
from pipe import Pipe
from score import Score
import constants


def rect_collision(rect1, rect2):
    if rect1[0] <= rect2[0]+rect2[2] and rect2[0] <= rect1[0]+rect1[2] and rect1[1] <= rect2[1]+rect2[3] and rect2[1] <= rect1[1]+rect1[3]:
        return True
    return False


def is_game_over(bird, pipes):
    for i in range(3):
        rect_bird = [bird.x, bird.y, bird.width, bird.height]
        rect_pipe1 = [pipes.ls[i][0], pipes.ls[i][1] -
                      pipes.height, pipes.width, pipes.height]
        rect_pipe2 = [pipes.ls[i][0], pipes.ls[i][1] +
                      pipes.blank, pipes.width, pipes.height]
        if rect_collision(rect_bird, rect_pipe1) == True or rect_collision(rect_bird, rect_pipe2) == True:
            return True
    if bird.y + bird.height < 0 or bird.y + bird.height > constants.WINDOWHEIGHT:
        return True
    return False


class FlappyBirdEnv:
    def __init__(self, window_width, window_height, background_img, game_display):
        self.window_width = window_width
        self.window_height = window_height
        self.bird = Bird(bird_width=constants.BIRDWIDTH, bird_height=constants.BIRDHEIGHT, window_height=constants.WINDOWHEIGHT,
                         window_width=constants.WINDOWWIDTH, bird_img=constants.BIRDIMG, game_display=game_display)
        self.pipe = Pipe(width=constants.PIPEWIDTH, height=constants.PIPEHEIGHT, blank=constants.BLANK, distance=constants.DISTANCE, speed=constants.PIPESPEED,
                         img=constants.PIPEIMG, window_width=constants.WINDOWWIDTH, window_height=constants.WINDOWHEIGHT, game_display=game_display)
        self.score = Score(window_width=constants.WINDOWWIDTH,
                           game_display=game_display, rect_collision=rect_collision)
        self.background_img = background_img
        self.game_display = game_display

    def step(self, action):
        # Apply action
        if action == 0:
            mouse_click = False
        else:
            mouse_click = True

        # Update game state
        self.pipe.update()
        self.bird.update(mouse_click)
        self.score.update(self.bird, self.pipe)

        # Check for game over
        game_over = is_game_over(self.bird, self.pipe)

        # Calculate reward
        reward = 0
        if game_over:
            reward = -100
        elif self.score.add_score:
            reward = 10

        # Return next state, reward, and game over flag
        return self.get_state(), reward, game_over

    def get_state(self):
        # Find the closest pipe
        closest_pipe = None
        min_distance = float('inf')
        for pipe in self.pipe.ls:
            distance = pipe[0] - self.bird.x
            if 0 <= distance < min_distance:
                min_distance = distance
                closest_pipe = pipe

        # Return the state representation
        return [
            self.bird.y,
            self.bird.speed,
            closest_pipe[0] - self.bird.x,
            closest_pipe[1] - self.bird.y,
            (closest_pipe[1] + self.pipe.blank) - self.bird.y
        ]

    def reset(self):
        self.bird = Bird(bird_width=constants.BIRDWIDTH, bird_height=constants.BIRDHEIGHT, window_height=constants.WINDOWHEIGHT,
                         window_width=constants.WINDOWWIDTH, bird_img=constants.BIRDIMG, game_display=self.game_display)
        self.pipe = Pipe(width=constants.PIPEWIDTH, height=constants.PIPEHEIGHT, blank=constants.BLANK, distance=constants.DISTANCE, speed=constants.PIPESPEED,
                         img=constants.PIPEIMG, window_width=constants.WINDOWWIDTH, window_height=constants.WINDOWHEIGHT, game_display=self.game_display)
        self.score.score_ = 0
        self.score.add_score = True
