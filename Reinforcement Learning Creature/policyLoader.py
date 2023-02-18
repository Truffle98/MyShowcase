from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import tensorflow as tf
import cv2

print(tf.__version__)

from tf_agents.environments import tf_py_environment

from huntingEnvironment import HuntingEnvironment

num_eval_episodes = 10
final_evals = 5

# Load the policy
policy_name = input("What is the name of the policy you would like to load?")
model_path = "Policies/.Old Policies/" + policy_name
saved_policy = tf.compat.v2.saved_model.load(model_path)

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

# Test the policy
eval_env = tf_py_environment.TFPyEnvironment(HuntingEnvironment())
avg_return, average_episode_length = compute_avg_return(eval_env, saved_policy, num_eval_episodes)
print('Average Return = {0:.2f}, Average episode length = {1}'.format(avg_return, average_episode_length))

# Watch the policy
print("Ready to watch?")
answer = input()
if answer != "no":
    show_env = tf_py_environment.TFPyEnvironment(HuntingEnvironment(True))
    for i in range(final_evals):

        time_step = show_env.reset()

        while not time_step.is_last():
            
            action_step = saved_policy.action(time_step)
            time_step = show_env.step(action_step.action)

    cv2.destroyAllWindows()