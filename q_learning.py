import numpy as np
import pickle
import constants
import os
import torch
import torch.optim as optim
from q_network import QNetwork

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


def discretize_state(state):
    return tuple(np.digitize(s, state_bins[i]) for i, s in enumerate(state))


def epsilon_greedy_policy(state, epsilon):
    # if np.random.rand() < epsilon:
    #     return np.random.choice(num_actions)
    # else:
    #     return np.argmax(q_table[state])

    if np.random.rand() < epsilon:
        return np.random.choice(num_actions)
    else:
        with torch.no_grad():
            state_tensor = torch.tensor(
                state, dtype=torch.float32).unsqueeze(0)
            action_values = q_network(state_tensor)
        return torch.argmax(action_values).item()


# def update_q_table(state, action, reward, next_state):
#     state = discretize_state(state)
#     next_state = discretize_state(next_state)

#     # Update Q-table using the Q-learning formula
#     q_table[state][action] += alpha * \
#         (reward + gamma * np.max(q_table[next_state]) - q_table[state][action])

def update_q_table(state, action, reward, next_state):
    state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
    next_state_tensor = torch.tensor(
        next_state, dtype=torch.float32).unsqueeze(0)
    action_tensor = torch.tensor(action, dtype=torch.int64).unsqueeze(0)
    reward_tensor = torch.tensor(reward, dtype=torch.float32).unsqueeze(0)

    # Calculate target value
    with torch.no_grad():
        target = reward_tensor + gamma * \
            torch.max(q_network(next_state_tensor), dim=1)[0].unsqueeze(1)

    # Calculate prediction
    prediction = q_network(state_tensor).gather(1, action_tensor.unsqueeze(1))

    # Update Q-network weights
    loss = torch.mean((prediction - target) ** 2)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


# def q_learning_policy(state):
#     state = discretize_state(state)
#     return epsilon_greedy_policy(state, epsilon)

input_size = 5  # Number of state variables
hidden_size = 32  # Size of hidden layers
output_size = num_actions  # Number of actions

q_network = QNetwork(input_size, hidden_size, output_size)
optimizer = optim.Adam(q_network.parameters(), lr=alpha)


def save_weights(file_path):
    torch.save(q_network.state_dict(), file_path)


def load_weights(file_path):
    if os.path.isfile(file_path):
        q_network.load_state_dict(torch.load(file_path))
    else:
        print(
            f"No weights file found at {file_path}. Using a randomly initialized model.")


load_weights(constants.Q_NETWORK_MODEL_PATH)


def q_learning_policy(state):
    with torch.no_grad():
        state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        action_values = q_network(state_tensor)
    return epsilon_greedy_policy(state, epsilon)
