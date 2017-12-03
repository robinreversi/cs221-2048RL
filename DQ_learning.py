import gym
import numpy as np
import random
import tensorflow as tf
import Multi_Game_2048.Multi_Game_2048_env


DISCOUNT = .9
NUM_GAMES = 100000
epsilon = .2

env = gym.make('Multi2048-v0')

num_boards = env.n

board_vals = tf.placeholder(shape=[1, 16 * num_boards],dtype=tf.float32)
W1 = tf.Variable(tf.random_uniform([16 * num_boards, 16*num_boards], 0, 0.01))
W2 = tf.Variable(tf.random_uniform([16 * num_boards, 16*num_boards], 0, 0.01))
A2 = tf.nn.relu(tf.matmul(board_vals, W1))
W3 = tf.Variable(tf.random_uniform([16 * num_boards, 4], 0, 0.01))
A3 = tf.nn.relu(tf.matmul(A2, W2))
q_values = tf.sigmoid(tf.matmul(A3, W3))
action = tf.argmax(q_values,1)

nextQ = tf.placeholder(shape=[1,4],dtype=tf.float32)
loss = tf.reduce_sum(tf.square(nextQ - q_values))
trainer = tf.train.GradientDescentOptimizer(learning_rate=0.01)
updateModel = trainer.minimize(loss)
init = tf.initialize_all_variables()


with tf.Session() as sess:
    sess.run(init)
    tf.reset_default_graph()

    for i in range(NUM_GAMES):
        obs = env.reset()
        done = False
        while not done:
            a, init_q_values = sess.run([action, q_values], feed_dict={board_vals:obs})
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
            #print("AFTER ACTION")
            #env.render()
        print("BOARD END")
        env.render()

        epsilon = 1./((i/50) + 10)
