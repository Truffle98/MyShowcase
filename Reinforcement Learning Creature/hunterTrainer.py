from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
import time

print(tf.__version__)
start_time = time.time()

from tf_agents.agents.dqn import dqn_agent
from tf_agents.environments import tf_py_environment
from tf_agents.environments import utils
from tf_agents.networks import sequential
from tf_agents.policies import random_tf_policy
from tf_agents.policies import PolicySaver
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.specs import tensor_spec
from tf_agents.utils import common

from huntingEnvironment import HuntingEnvironment

# Hyperparameters
num_iterations = 40000

initial_collect_steps = 1000
collect_steps_per_iteration = 4
replay_buffer_capacity = 100000

batch_size = 32
learning_rate = 0.0001
epsilon = 0.7
log_interval = 20

num_eval_episodes = 20
final_evals = 5
eval_interval = 200
n_step_update = 1

fc_layer_params = (2048, 2048)

model_path = "Policies"

env = HuntingEnvironment()
utils.validate_py_environment(env, episodes = 3)

hyperparameters = [fc_layer_params, num_iterations, initial_collect_steps, collect_steps_per_iteration, 
                   replay_buffer_capacity, batch_size, learning_rate, epsilon, env.return_discount()]

# Environment and agent setup
train_env = tf_py_environment.TFPyEnvironment(HuntingEnvironment())
eval_env = tf_py_environment.TFPyEnvironment(HuntingEnvironment())

action_tensor_spec = tensor_spec.from_spec(env.action_spec())
num_actions = action_tensor_spec.maximum - action_tensor_spec.minimum + 1

def dense_layer(num_units):
    return tf.keras.layers.Dense(
        num_units,
        activation=tf.keras.activations.relu,
        kernel_initializer=tf.keras.initializers.VarianceScaling(
            scale=2.0, mode='fan_in', distribution='truncated_normal'))

dense_layers = [dense_layer(num_units) for num_units in fc_layer_params]
q_values_layer = tf.keras.layers.Dense(
    num_actions,
    activation=None,
    kernel_initializer=tf.keras.initializers.RandomUniform(
        minval=-0.03, maxval=0.03),
    bias_initializer=tf.keras.initializers.Constant(-0.2))
q_net = sequential.Sequential(dense_layers + [q_values_layer])

optimizer = tf.keras.optimizers.Adam(learning_rate=learning_rate)

train_step_counter = tf.Variable(0)

agent = dqn_agent.DqnAgent(
    train_env.time_step_spec(),
    train_env.action_spec(),
    q_network=q_net,
    epsilon_greedy = epsilon,
    optimizer=optimizer,
    td_errors_loss_fn=common.element_wise_squared_loss,
    train_step_counter=train_step_counter)

agent.initialize()
print("Summary: ")
agent._q_network.summary()

eval_policy = agent.policy
collect_policy = agent.collect_policy

def compute_avg_return(environment, policy, num_episodes=5):

    total_return = 0.0
    total_episode_length = 0.0
    for _ in range(num_episodes):

        time_step = environment.reset()
        episode_return = 0.0

        while not time_step.is_last():
            action_step = policy.action(time_step)
            time_step = environment.step(action_step.action)
            episode_return += time_step.reward
            total_episode_length += 1
        total_return += episode_return

    avg_return = total_return / num_episodes
    average_episode_length = total_episode_length / num_episodes
    return avg_return.numpy()[0], average_episode_length

random_policy = random_tf_policy.RandomTFPolicy(train_env.time_step_spec(), train_env.action_spec())
#print(compute_avg_return(eval_env, random_policy, num_eval_episodes))

replay_buffer = tf_uniform_replay_buffer.TFUniformReplayBuffer(
    data_spec=agent.collect_data_spec,
    batch_size=train_env.batch_size,
    max_length=replay_buffer_capacity)

def collect_step(environment, policy):
    time_step = environment.current_time_step()
    action_step = policy.action(time_step)
    next_time_step = environment.step(action_step.action)
    traj = trajectory.from_transition(time_step, action_step, next_time_step)

    # Add trajectory to the replay buffer
    replay_buffer.add_batch(traj)

for _ in range(initial_collect_steps):
    collect_step(train_env, random_policy)

dataset = replay_buffer.as_dataset(
    num_parallel_calls=3, sample_batch_size=batch_size,
    num_steps=n_step_update + 1).prefetch(3)

iterator = iter(dataset)

agent.train = common.function(agent.train)

# Reset the train step
agent.train_step_counter.assign(0)

#This function saves the data. It takes the hyperparams, an average score and episode length, and a name.
#The hyperparams are a list that go in this order. A list of the neurons in each layer, the number of training iterations, the number of initial collect steps,
#   the number of collection steps per iteration, the replay buffer capacity, the batch size, the learning rate, and the environment's discount
def save_data(hyperparams, score, length, name = "n/a"):
    path = model_path
    if name != "n/a":
        path += "/.Old Policies/" + name
        os.mkdir(path)

    f = open(path + "/policy_stats.txt", 'w')
    f.write("Name: {}".format(name))

    f.write("\nNeurons: ")
    for n in hyperparams[0]:
        f.write(str(n) + " ")
    f.write("\nNumber of Training Iterations: {}".format(hyperparams[1]))
    f.write("\nNumber of Initial Collection Steps: {}".format(hyperparams[2]))
    f.write("\nNumber of Collection Steps per Iteration: {}".format(hyperparams[3]))
    f.write("\nReplay Buffer Capacity: {}".format(hyperparams[4]))
    f.write("\nBatch Size: {}".format(hyperparams[5]))
    f.write("\nLearning Rate: {}".format(hyperparams[6]))
    f.write("\nEpsilon: {}".format(hyperparams[7]))
    f.write("\nEnvironment's Discount: {}".format(hyperparams[8]))

    f.write("\nAverage Score: {0:.2f}".format(score))
    f.write("\nAverage Episode Length: {0:.2f}".format(length))

total_returns = 0
total_evals = 0
highest_return = -200
total_episode_lengths = 0
lowest_episode_length = 100000

# Evaluate the agent's policy once before training.
avg_return, average_episode_length = compute_avg_return(eval_env, agent.policy, num_eval_episodes)
returns = [avg_return]

total_returns += avg_return
total_episode_lengths += average_episode_length
total_evals += 1
print('step = {0}: Average Return = {1:.2f}, Average episode length = {2}'.format(0, avg_return, average_episode_length))

# Training the agent
for _ in range(num_iterations):

    # Collect a few steps using collect_policy and save to the replay buffer.
    for _ in range(collect_steps_per_iteration):
        collect_step(train_env, collect_policy)

    # Sample a batch of data from the buffer and update the agent's network.
    experience, unused_info = next(iterator)
    train_loss = agent.train(experience)

    step = agent.train_step_counter.numpy()

    if step % log_interval == 0:
        print('step = {0}: loss = {1}'.format(step, train_loss.loss))

    if step % eval_interval == 0:
        avg_return, average_episode_length = compute_avg_return(eval_env, agent.policy, num_eval_episodes)
        total_returns += avg_return
        total_episode_lengths += average_episode_length
        total_evals += 1
        if avg_return > highest_return:
            highest_return = avg_return
            saver = PolicySaver(agent.policy, batch_size = None)
            saver.save(model_path)
            save_data(hyperparameters, avg_return, average_episode_length)
        if average_episode_length < lowest_episode_length:
            lowest_episode_length = average_episode_length
        print('step = {0}: Average Return = {1:.2f}, Average episode length = {2}'.format(step, avg_return, average_episode_length))
        returns.append(avg_return)

best_policy = tf.compat.v2.saved_model.load(model_path)

# Prints stats at the end along with a graph
print('Average across all returns = {0:.2f}'.format(total_returns / total_evals))
print('Highest single run = {0:.2f}'.format(highest_return))
print('Average episode length = {0:.2f}'.format(total_episode_lengths / total_evals))
print('Lowest episode length = {0:.2f}'.format(lowest_episode_length))
second_test_return, second_average_length = compute_avg_return(eval_env, best_policy, num_eval_episodes)
print('Best policy second test: R - {0:.2f}, EL - {1:.2f}'.format(second_test_return, second_average_length))

steps = range(0, num_iterations + 1, eval_interval)
plt.plot(steps, returns)
plt.ylabel('Average Return')
plt.xlabel('Step')
plt.ylim(-150, 150)

seconds = int(np.round(time.time() - start_time))
minutes = int(np.floor(seconds / 60))
seconds %= 60
hours = int(np.floor(minutes / 60))
minutes %= 60

print("Runtime: {0} hour(s), {1} minute(s), and {2} second(s)".format(hours, minutes, seconds))

plt.show()

# Watch your trained policy and save if you wish
print("Ready to watch?")
answer = input()
if answer != "no":
    final_env = tf_py_environment.TFPyEnvironment(HuntingEnvironment(True))
    for i in range(final_evals):

        time_step = final_env.reset()

        while not time_step.is_last():
            
            action_step = best_policy.action(time_step)
            time_step = final_env.step(action_step.action)

    cv2.destroyAllWindows()
    given_name = input("What would you like to name this policy?")
    if (given_name != "no"):
        save_data(hyperparameters, second_test_return, second_average_length, given_name)
        tf.saved_model.save(best_policy, model_path + "/.Old Policies/" + given_name)

print ("No errors !")