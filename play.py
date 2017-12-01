import gym
import game2048.game2048_env
import random
from q_learning import *

env = gym.make('2048-v0')

q_learning(approximate, env, .01, .5)
'''
env.seed()
observation = env.reset()
end = False
while not end:
    print "BEFORE:"
    env.render()
    action = env.action_space.sample()
    print "ACTION" + str(action)
    next_observation, reward, end, info = env.step(action)
    print "AFTER"
    env.render()
    
'''