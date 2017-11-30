import gym
import game2048.game2048_env
import random


env = gym.make('2048-v0')

env.seed()
observation = env.reset()
for t in range(5):
    print "BEFORE:"
    env.render()
    action = env.action_space[random.randInt(0,3)]
    print "ACTION" + str(action)
    next_observation, reward, done, info = env.step(action)
    print "AFTER"
    print next_observation
    
    
