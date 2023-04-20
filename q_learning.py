import numpy as np
import pickle
import constants
import os

#  -----------------------------------------------------

def save_q_table(file_path):
    with open(file_path, 'wb') as f:
        pickle.dump(q_table, f)


def load_q_table(file_path):
    global q_table
    with open(file_path, 'rb') as f:
        q_table = pickle.load(f)


#  -----------------------------------------------------

# Q-learning parameters
alpha = 0.1
gamma = 0.99
epsilon = 0.1

# Discretize state space
state_bins = [
    np.linspace(0, constants.WINDOWHEIGHT -
                constants.BIRDHEIGHT, 10),  # bird_y
    np.linspace(-20, 20, 10),  # bird_speed
    np.linspace(0, constants.WINDOWWIDTH, 10),  # pipe_x
    np.linspace(0, constants.WINDOWHEIGHT - constants.BLANK, 10),  # pipe_y_top
    np.linspace(constants.BLANK, constants.WINDOWHEIGHT, 10)  # pipe_y_bottom
]

# Initialize Q-table
num_actions = 2
q_table_shape = tuple(len(bins) + 1 for bins in state_bins) + (num_actions,)
q_table = np.zeros(q_table_shape)

# Load saved Q-table if exists
q_table_file = 'q_table.pickle'
if os.path.exists(q_table_file):
    load_q_table(q_table_file)

def discretize_state(state):
    return tuple(np.digitize(s, state_bins[i]) for i, s in enumerate(state))


def epsilon_greedy_policy(state, epsilon):
    if np.random.rand() < epsilon:
        return np.random.choice(num_actions)
    else:
        return np.argmax(q_table[state])


def update_q_table(state, action, reward, next_state):
    state = discretize_state(state)
    next_state = discretize_state(next_state)

    # Update Q-table using the Q-learning formula
    q_table[state][action] += alpha * \
        (reward + gamma * np.max(q_table[next_state]) - q_table[state][action])


def q_learning_policy(state):
    state = discretize_state(state)
    return epsilon_greedy_policy(state, epsilon)
