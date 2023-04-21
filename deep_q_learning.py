import numpy as np
import constants
import os
import torch
import torch.optim as optim
from deep_q_network import DeepQNetwork
from relay_buffer import ReplayBuffer

# Q-learning parameters
alpha = 0.1
gamma = 0.99
epsilon = 0.1

# Experience Replay parameters
replay_buffer = ReplayBuffer(max_size=100000)
batch_size = 64

# Initialize Q-table
num_actions = 2


def epsilon_greedy_policy(state, epsilon):
    if np.random.rand() < epsilon:
        return np.random.choice(num_actions)
    else:
        with torch.no_grad():
            state_tensor = torch.tensor(
                state, dtype=torch.float32).unsqueeze(0)
            action_values = q_network(state_tensor)
        return torch.argmax(action_values).item()


def update_q_table(state, action, reward, next_state):
    state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
    next_state_tensor = torch.tensor(
        next_state, dtype=torch.float32).unsqueeze(0)
    action_tensor = torch.tensor(action, dtype=torch.int64).unsqueeze(0)
    reward_tensor = torch.tensor(reward, dtype=torch.float32).unsqueeze(0)

    # Calculate target value
    with torch.no_grad():
        target = reward_tensor + gamma * \
            torch.max(target_network(next_state_tensor), dim=1)[0].unsqueeze(1)

    # Calculate prediction
    prediction = q_network(state_tensor).gather(1, action_tensor.unsqueeze(1))

    # Update Q-network weights
    loss = torch.mean((prediction - target) ** 2)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()


def update_target_network():
    target_network.load_state_dict(q_network.state_dict())


input_size = 5  # Number of state variables
hidden_size = 32  # Size of hidden layers
output_size = num_actions  # Number of actions

# Initialize Q-network and target network
q_network = DeepQNetwork(input_size, hidden_size, output_size)
target_network = DeepQNetwork(input_size, hidden_size, output_size)
optimizer = optim.Adam(q_network.parameters(), lr=alpha)


def save_weights(file_path):
    torch.save(q_network.state_dict(), file_path)


def load_weights(file_path):
    if os.path.isfile(file_path):
        q_network.load_state_dict(torch.load(file_path))
    else:
        print(
            f"No weights file found at {file_path}. Using a randomly initialized model.")

# Load weights if they exist
load_weights(constants.Q_NETWORK_MODEL_PATH)

# Function to update the Q-network with Experience Replay
def update_q_network(batch_size):
    if len(replay_buffer) < batch_size:
        return

    samples = replay_buffer.sample(batch_size)

    for state, action, reward, next_state, done in samples:
        update_q_table(state, action, reward, next_state)

# Function to add experience to the replay buffer
def add_experience(state, action, reward, next_state, done):
    replay_buffer.add(state, action, reward, next_state, done)

# Function to get the action using the epsilon-greedy policy
def q_learning_policy(state):
    with torch.no_grad():
        state_tensor = torch.tensor(state, dtype=torch.float32).unsqueeze(0)
        action_values = q_network(state_tensor)
    return epsilon_greedy_policy(state, epsilon)

# Update this function in your game loop to add experience and update the Q-network
def game_step(state, action, reward, next_state, done):
    add_experience(state, action, reward, next_state, done)
    update_q_network(batch_size)