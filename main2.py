import pygame
import sys
import time
from flappy_bird_env import FlappyBirdEnv
import constants

from deep_q_learning import q_learning_policy, save_weights, game_step
from log import log_score

# Initialize pygame
pygame.init()
FPS = 60
fpsClock = pygame.time.Clock()

# Create game display
DISPLAYSURF = pygame.display.set_mode(
    (constants.WINDOWWIDTH, constants.WINDOWHEIGHT))
pygame.display.set_caption('Flappy Bird Reinforcement Learning')

# Initialize environment
env = FlappyBirdEnv(constants.WINDOWWIDTH,
                    constants.WINDOWHEIGHT, constants.BACKGROUND, DISPLAYSURF)


def simple_policy(state):
    bird_y, bird_speed, pipe_x, pipe_y_top, pipe_y_bottom = state
    if bird_y < pipe_y_top:
        return 1
    else:
        return 0


def main():
    game_over = False
    counter = 0
    while not game_over:
        # Get current state
        state = env.get_state()

        # Choose action based on simple policy
        # action = simple_policy(state)

        # Choose action based on Q-learning policy
        action = q_learning_policy(state)

        # Perform action and update environment
        next_state, reward, game_over = env.step(action)

        # Update Q-network and replay buffer
        # game_step(state, action, reward, next_state, game_over)

        # Draw game state
        DISPLAYSURF.blit(constants.BACKGROUND, (0, 0))
        env.pipe.draw()
        env.bird.draw()
        env.score.draw()

        # Update display
        pygame.display.update()
        fpsClock.tick(FPS)

        # Check for exit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_weights(constants.Q_NETWORK_MODEL_PATH)
                pygame.quit()
                sys.exit()

        # Restart the game if game_over
        if game_over:
            counter += 1
            log_score("log/game_results.csv", env.score.score_, counter)
            time.sleep(0.5)
            env.reset()
            game_over = False


if __name__ == '__main__':
    main()
