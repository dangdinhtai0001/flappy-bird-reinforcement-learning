import pygame

WINDOWWIDTH = 400
WINDOWHEIGHT = 600

BIRDWIDTH = 60
BIRDHEIGHT = 45
G = 0.5
SPEEDFLY = -8
BIRDIMG = pygame.image.load('img/bird.png')

PIPEWIDTH = 60
PIPEHEIGHT = 500
BLANK = 160
DISTANCE = 200
PIPESPEED = 2
PIPEIMG = pygame.image.load('img/pipe.png')

BACKGROUND = pygame.image.load('img/background.png')

Q_NETWORK_MODEL_PATH = "q_network_weights.pth"
