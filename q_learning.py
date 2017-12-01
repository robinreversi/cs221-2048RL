import numpy as np
import matplotlib.pyplot as plt
import random
from operator import itemgetter

LOSS_BATCH_SIZE = 20
EPSILON = .000001
NUM_FEATURES = 3
TEST_NUM = 10

def approximate(obs, action):
    '''
        Defines the handicrafted approximation function
        - Outputs a vector of size n where n is the 
            number of features
    '''
    return np.array([1, sum(obs), max(obs)])
    
def run_game(w, env, train, num_games, f, discount, step_size):
    game_over = False
    action_space = range(env.action_space.n)
    cur = env.reset()
    total_loss = 0
    while not game_over:
        print "===================================="
        print "-----------------BEFORE---------------\n"
        env.render()
        # pick the action that maximizes Q_opt(cur, a) = w . f(a)
        # ROUGH PSEUDO-CODE, UNTESTED
        action = None
        features = dict((a, f(cur, a)) for a in action_space)
        potentials = dict((a, w.dot(features[a])) for a in features)
        if(random.random() < 1.0 / (num_games + .1) and train):
            print "\nRANDOM ACTION TAKEN\n"
            action = env.action_space.sample()
        else:
            action = max(potentials.iteritems(), key=itemgetter(1))[0] 
        Q_opt = potentials[action]
        phi = features[action]
        cur, reward, game_over, info = env.step(action)

        print "\n-----------AFTER ACTION: " + str(action) + "------------\n"
        env.render()
        print "====================================="

        V_opt = max([w.dot(f(cur, a)) for a in action_space])

        loss = Q_opt - (reward + discount * V_opt)
        total_loss += loss
        # learn
        if(train):
            w = w - step_size * loss * phi
        print "\n WEIGHTS: " + str(w) + "\n"

    return total_loss, env.score

def q_learning(f, env, step_size, discount):
    print "START"
    has_converged = False
    
    env.seed()
    init = env.reset()

    w = np.zeros(NUM_FEATURES)
    avg_losses = np.array([])
    scores = []
    game_count = 0
    while not has_converged:
        env.seed()
        cur = env.reset()

        run_game(w, env, True, game_count, f, discount, step_size)

        game_count += 1

        if(game_count % 15 == 0):
            avg_loss = 0 
            avg_score = 0
            for i in range(TEST_NUM):
                env.seed()
                init = env.reset()
                loss, score = run_game(w, env, False, 1, f, discount, step_size)
                avg_loss += loss
                avg_score += score

            if(avg_loss / float(TEST_NUM) < EPSILON):
                has_converged = True
                print avg_loss
                print avg_score
    
    return w
    #plt.show()
    
