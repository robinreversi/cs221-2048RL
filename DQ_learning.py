import gym
import numpy as np
import random
import tensorflow as tf
tf.reset_default_graph()
import Multi_Game_2048.Multi_Game_2048_env
<<<<<<< HEAD
import expectimax.player as pl
import collections, random, operator
import copy
=======
import player as pl
import collections, random, operator
import copy
from Multi_Game_2048 import gameutil
util = gameutil.gameutil()
>>>>>>> ba95830c36bdf0d3e00608f70e093de393c4deed


DISCOUNT = .9
NUM_GAMES = 100
epsilon = 0.1

env = gym.make('Multi2048-v0')

num_boards = env.n
board_vals = tf.placeholder(shape=[1, 16 * num_boards],dtype=tf.float32)
b1 = tf.Variable(tf.random_uniform([1, 16 * num_boards],0,1))
b2 = tf.Variable(tf.random_uniform([1, 16 * num_boards],0,1))
b3 = tf.Variable(tf.random_uniform([1, 4],0,1))
W1 = tf.Variable(tf.random_uniform([16 * num_boards, 16*num_boards], 0, 1))
W2 = tf.Variable(tf.random_uniform([16 * num_boards, 16*num_boards], 0, 1))
A2 = tf.nn.relu(tf.add(tf.matmul(board_vals, W1),b1))
W3 = tf.Variable(tf.random_uniform([16 * num_boards, 4], 0, 1))
A3 = tf.nn.relu(tf.add(tf.matmul(A2, W2),b2))
q_values = tf.add(tf.matmul(A3, W3),b3)
action = tf.argmax(q_values,1)
nextQ = tf.placeholder(shape=[1,4],dtype=tf.float32)


loss = tf.reduce_sum(tf.square(nextQ - q_values))
trainer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
updateModel = trainer.minimize(loss)
init = tf.initialize_all_variables()
weights1 = [7,6,5,4,6,5,4,3,5,4,3,2,4,3,2,1]
weights2 = [4,5,6,7,3,4,5,6,2,3,4,5,1,2,3,4]
weights3 = [1,2,3,4,2,3,4,5,3,4,5,6,4,5,6,7]
weights4 = [4,3,2,1,5,4,3,2,6,5,4,3,7,6,5,4]

def evalFn(currentGameState, isEnd, score):
        if isEnd:
            return float('-inf')

        def countZeros(board):
            count = 0
            for x in range(16):
                i = 0xF << (4 * x)
                if i & board == 0:
                    count += 1
            return count

        def weightedGrid(board):
            sum1 = 0.0
            sum2 = 0.0
            sum3 = 0.0
            sum4 = 0.0
            for i in range(16):
                val = 1 << ((board >> (4 * i)) & 0xF)
                if val > 1:
                    sum1 += weights1[i] * val
                    sum2 += weights2[i] * val
                    sum3 += weights3[i] * val
                    sum4 += weights4[i] * val
            return max(sum1, sum2, sum3, sum4)

        ''' def monotonicity(cGS, k=10.0):

            def monoEval(a, b, e=1.0):
                # if a == b: b += 1  # make [ v ][ v ] the same as [ v ][ v+1 ]
                if a == b: return 2 * k
                return k / (np.log2(b / a) ** e)
            sum = 0.0

            for r in range(4):
                forw = 0.0
                back = 0.0
                for k in range(3):
                    forw += monoEval(cGS.board[r, k], cGS.board[r, k+1])
                    back += monoEval(cGS.board[r, k+1], cGS.board[r, k])
                sum += max(forw, back)

            for c in range(4):
                forw = 0.0
                back = 0.0
                for k in range(3):
                    forw += monoEval(cGS.board[k, c], cGS.board[k+1, c])
                    back += monoEval(cGS.board[k+1, c], cGS.board[k, c])
                sum += max(forw, back)

<<<<<<< HEAD
weights1 = [range(i,i+4) for i in range(1,5)]
weights2 = [range(i+3, i-1,-1) for i in range(1, 5)]
weights3 = [range(i+3, i-1,-1) for i in range(4, 0,-1)]
weights4 = [range(i, i + 4) for i in range(4, 0,-1)]

def evalFn(currentGameState):
    if currentGameState.isEnd():
        return float('-inf')

    def weightedGrid(currentGameState):
        sum1 = 0.0
        sum2 = 0.0
        sum3 = 0.0
        sum4 = 0.0
        for i in range(4):
            for j in range(4):
                sum1 += weights1[i][j] * currentGameState.board[i, j]
                sum2 += weights2[i][j] * currentGameState.board[i, j]
                sum3 += weights3[i][j] * currentGameState.board[i, j]
                sum4 += weights4[i][j] * currentGameState.board[i, j]
        return max(sum1, sum2, sum3, sum4)

    def monotonicity(cGS, k=10.0):

        def monoEval(a, b, e=1.0):
            # if a == b: b += 1  # make [ v ][ v ] the same as [ v ][ v+1 ]
            if a == b: return 2 * k
            return k / (np.log2(b / a) ** e)
        sum = 0.0

        for r in range(4):
            forw = 0.0
            back = 0.0
            for k in range(3):
                forw += monoEval(cGS.board[r, k], cGS.board[r, k+1])
                back += monoEval(cGS.board[r, k+1], cGS.board[r, k])
            sum += max(forw, back)

        for c in range(4):
            forw = 0.0
            back = 0.0
            for k in range(3):
                forw += monoEval(cGS.board[k, c], cGS.board[k+1, c])
                back += monoEval(cGS.board[k+1, c], cGS.board[k, c])
            sum += max(forw, back)

        return sum

    def openTilePenalty(cGS, n=5):
        return cGS.countZeros() - n
            # return -((cGS.countZeros() - n) ** 2)

    eval = 0.0
    eval += currentGameState.score
    eval += weightedGrid(currentGameState)
    # eval += monotonicity(currentGameState, k=10.0)
    eval += 50 * openTilePenalty(currentGameState)

    return eval
=======
            return sum '''

        def openTilePenalty(board, n=5):
            #return util.countZeros(board) - n
            return -((util.countZeros(board) - n) ** 2)

        def smoothness(board):
            sm = 0.0
            for r in range(4):
                for k in range(3):
                    sm += abs(util.getTile(board, 4 * r + k) - util.getTile(board, 4 * r + k + 1))

            for c in range(4):
                for k in range(3):
                    sm += abs(util.getTile(board, 4 * k + c) - util.getTile(board, 4 * (k+1) + c))

            return -sm  # penalize high disparity

        eval = 0.0
        eval += score
        eval += weightedGrid(currentGameState)
        #eval += monotonicity(currentGameState, k=10.0)
        #eval += 10 * openTilePenalty(currentGameState)
        eval += smoothness(currentGameState)

        return eval
>>>>>>> ba95830c36bdf0d3e00608f70e093de393c4deed

saver = tf.train.Saver()
<<<<<<< HEAD
with tf.Session() as sess:
    sess.run(init)
    tf.reset_default_graph()
<<<<<<< HEAD
    agent = pl.Player(2, evalFn)
=======
    agent = pl.Player(2, evalFn, util, True)
>>>>>>> ba95830c36bdf0d3e00608f70e093de393c4deed
    for i in range(NUM_GAMES):
        obs = env.reset()
        done = False
        while not done:
            a, init_q_values = sess.run([action, q_values], feed_dict={board_vals:obs})
            games = env.boards
            values = collections.defaultdict(float)
            count = collections.defaultdict(float)
            for game in games:
                f, vals = agent.getAction(copy.deepcopy(game))
                for move, score in vals:
                    values[move] += score
                    count[move] += 1
            for key in values:
                values[move] /= count[move]
            a[0] = max(values.items(), key=operator.itemgetter(1))[0]
            if(random.random() < epsilon):
                a[0] = env.action_space.sample()

            new_obs, reward, done, info = env.step(a[0])

            new_q_values = sess.run(q_values, feed_dict={board_vals:new_obs})

            # V of the new state = max of the q values
            max_new_q = np.max(new_q_values)
            targetQ = init_q_values
            targetQ[0, a[0]] = reward + DISCOUNT * max_new_q
            _ = sess.run([updateModel], feed_dict={board_vals: obs, nextQ: targetQ})

            obs = new_obs
            print("AFTER ACTION")
            env.render()
        print("BOARD END")
=======
sess = tf.Session()

saver.restore(sess, "./model/model.ckpt")
#sess.run(init)
agent = pl.Player(2, evalFn, util, True)
scores = []
for i in range(NUM_GAMES):
    obs = env.reset()
    done = False
    while not done:
        a, init_q_values = sess.run([action, q_values], feed_dict={board_vals:obs})
        print(a)
        print(init_q_values)
        games = env.boards


        legalMoves = list(env.getLegalMoves())
        maxmov = 0
        maxval = 0
        for mov in legalMoves:
            if init_q_values[0][mov] > maxval:
                maxval = init_q_values[0][mov]
                maxmov = mov
        '''
        values = collections.defaultdict(float)
        count = collections.defaultdict(float)
        for game in games:
            f, vals = agent.getAction(copy.deepcopy(game))
            for move, score in vals:
                values[move] += score
                count[move] += 1
        for key in values:
            values[move] /= count[move]
        maxmov = max(values.items(), key=operator.itemgetter(1))[0]
        '''
        if(random.random() < epsilon):
            maxmov = env.action_space.sample()

        new_obs, reward, done, info = env.step(maxmov)
        new_q_values = sess.run(q_values, feed_dict={board_vals:new_obs})

        # V of the new state = max of the q values
        max_new_q = np.max(new_q_values)
        print(max_new_q)
        targetQ = init_q_values
        targetQ[0, a[0]] = reward + DISCOUNT * max_new_q
        _ = sess.run([updateModel], feed_dict={board_vals: obs, nextQ: targetQ})

        obs = new_obs
        print("AFTER ACTION")
        print('Iter: ', i)
>>>>>>> 2d8ce898d62c69f2463a691364feb7c741578fe5
        env.render()
    print("BOARD END")
    env.render()
    scores.append(env.getScore())
    epsilon = 1./((i/50) + 10)
print("Average Score: ", sum(scores)/float(len(scores)))

save_path = saver.save(sess, "./model/model.ckpt")
print("Model saved in file: %s" % save_path)
sess.close()
