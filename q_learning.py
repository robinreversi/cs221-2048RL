import numpy as np
import matplotlib.pyplot as plt
from operator import itemgetter

LOSS_BATCH_SIZE = 20
EPSILON = .001
NUM_FEATURES = 3

def approximate(obs, action):
    '''
        Defines the handicrafted approximation function
        - Outputs a vector of size n where n is the 
            number of features
    '''
    return np.array([1, sum(obs), max(obs)])
    
def q_learning(f, env, step_size, discount):
    action_space = range(env.action_space.n)
    has_converged = False
    env.seed()
    init = env.reset()
    w = np.zeros(NUM_FEATURES)
    avg_losses = []

    while not has_converged:
        env.seed()
        cur = env.reset()

        game_over = False
        
        losses = []
        i = 0
        while not game_over and not has_converged:
            
            print "BEFORE:"
            env.render()
            # pick the action that maximizes Q_opt(cur, a) = w . f(a)
            # ROUGH PSEUDO-CODE, UNTESTED
            features = dict((a, f(cur, a)) for a in action_space)
            potentials = dict((a, w.dot(features[a])) for a in features)
            action = max(potentials.iteritems(), key=itemgetter(1))[0]
            Q_opt = potentials[action]
            phi = features[action]
            print "ACTION" + str(action)
            cur, reward, game_over, info = env.step(action)
            print "AFTER"
            env.render()
            
            loss = Q_opt - (reward + discount * max([w.dot(f(cur, a)) for a in action_space]))
            losses.append(loss)
            
            # learn
            w = w - step_size * loss * phi
            
            if(i % LOSS_BATCH_SIZE == 0):
                avg_loss = sum(losses) / float(LOSS_BATCH_SIZE)
                avg_losses.append(avg_loss)
                print avg_loss
                if(avg_loss < EPSILON):
                    has_converged = True
            
    print avg_losses
    plt.plot(avg_losses)
    
