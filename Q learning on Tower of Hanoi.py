import random
import sys
import numpy as np
import gym
from domains import *
from domains import tower_of_hanoi
import matplotlib.pyplot as plt

if __name__ == "__main__":
    environment = gym.make("toh_d3_r3-v2")  # change the environment name to experiment on different versions (two options: "toh_d3_r3-v1" and "toh_d3_r3-v2")

    step_limit = 100  # you can provide a step limit for each episode. change the step limit to see different learning curves 1000
    number_of_episodes = 100 # change the number of episodes to see how much episodes it takes to converge 100
    epsilon = 0.8  # change the epsilon value to see the effect of exploration 0.1
    learning_rate = 0.7 # change the learning rate to see its effect on the learning 0.1
    discount_rate = 0.3  # change the discount rate to see its effect on the learning 0.9

    action_size = environment.action_space.n
    state_size = 3 ** 3 #
    print(environment.get_observation_space_size())#print(action_size, state_size)

    q_table = np.zeros([state_size, action_size])#np.array([])#


    # Initialize variables to track rewards for plotting
    reward_list = []
    ave_reward_list = []


    for i in range(number_of_episodes):
        state = environment.reset()  # reset to get the initial state from the environment
        total_reward = 0  # keep the reward get from the environment through an episode to report

        for _ in range(step_limit):
            '''
                IMPLEMENT EPSILON GREEDY ACTION SELECTION BASED ON THE CURRENT STATE
            '''


            # decide if explore or exploit
            tradeoff = random.uniform(0, 1)
            #print(tradeoff)

            if tradeoff > epsilon:
                action = np.argmax(q_table[state])
            else:
                action = environment.action_space.sample()



            next_state, reward, done = environment.step(action)
            #print(reward)
            total_reward = total_reward + reward
            #print(total_reward)

            '''
                IMPLEMENT Q LEARNING UPDATE RULE
            '''

            old_value = q_table[state, action]
            next_max = np.max(q_table[next_state])

            new_value = (1 - learning_rate) * old_value + learning_rate * (reward + discount_rate * next_max)
            np.append(q_table[state,action], new_value)

            #q_table[state, action] = q_table[state, action] + learning_rate * (reward + discount_rate * next_max - q_table[state, action])

            #if reward == -10:
            #    penalties += 1

            state = next_state

            print(state, action, next_state, reward, done)  # printing each step for debugging purposes
            print(i,_)
            if done:  # episode ends when the agent reaches to a goal state
                break


        # Track rewards
        reward_list.append(total_reward)

        if (i + 1) % 100 == 0:
            ave_reward = np.mean(reward_list)
            ave_reward_list.append(ave_reward)
            reward_list = []
        print(total_reward)  # total reward get from the environment should increase with new episodes if the agent is learning

    # Plot Rewards
    plt.plot(100 * (np.arange(len(ave_reward_list)) + 1), ave_reward_list)
    plt.xlabel('Episodes')
    plt.ylabel('Average Reward')
    plt.title('Average Reward vs Episodes')
    plt.savefig('rewards.png')
    plt.show()
    plt.close()

    environment.close()