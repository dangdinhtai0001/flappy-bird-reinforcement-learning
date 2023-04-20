import pygame
import sys
import pygame

from bird import Bird
from pipe import Pipe
from score import Score

import constants

pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()

DISPLAYSURF = pygame.display.set_mode(
    (constants.WINDOWWIDTH, constants.WINDOWHEIGHT))
pygame.display.set_caption('Flappy Bird')


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


def main():
    bird = Bird(bird_width=constants.BIRDWIDTH, bird_height=constants.BIRDHEIGHT, window_height=constants.WINDOWHEIGHT,
                window_width=constants.WINDOWWIDTH, bird_img=constants.BIRDIMG, game_display=DISPLAYSURF)
    pipe = Pipe(width=constants.PIPEWIDTH, height=constants.PIPEHEIGHT, blank=constants.BLANK, distance=constants.DISTANCE, speed=constants.PIPESPEED,
                img=constants.PIPEIMG, window_width=constants.WINDOWWIDTH, window_height=constants.WINDOWHEIGHT, game_display=DISPLAYSURF)
    score = Score(window_width=constants.WINDOWWIDTH,
                  game_display=DISPLAYSURF, rect_collision=rect_collision)
    while True:
        mouse_click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_click = True

        DISPLAYSURF.blit(constants.BACKGROUND, (0, 0))

        pipe.draw()
        pipe.update()

        bird.draw()
        bird.update(mouse_click)

        score.draw()
        score.update(bird, pipe)

        if is_game_over(bird, pipe) == True:
            return

        pygame.display.update()
        fpsClock.tick(FPS)


if __name__ == '__main__':
    main()
