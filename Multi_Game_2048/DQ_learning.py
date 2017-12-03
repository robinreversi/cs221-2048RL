import gym
import numpy as np
import random
import tensorflow as tf
import matplotlib.pyplot as plt

DISCOUNT = .9
NUM_GAMES = 100000
EPSILON = .2

env = gym.make('Multi2048-v0')

num_boards = env.n

board_vals = tf.placeholder(shape=[1, 16 * num_boards],dtype=tf.float32)
print inputs1
W = tf.Variable(tf.random_uniform([16 * num_boards, 4], 0, 0.01))
print W
q_values = tf.matmul(inputs1, W)
print Qout
action = tf.argmax(Qout,1)

nextQ = tf.placeholder(shape=[1,4],dtype=tf.float32)
loss = tf.reduce_sum(tf.square(nextQ - Qout))
trainer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
updateModel = trainer.minimize(loss)

return env



with tf.Session() as sess:
    sess.run(init)
    tf.reset_default_graph()

    for _ in range(NUM_GAMES):
        obs = env.reset()
        done = False
        env.render()
        while not done:
            a, q_values = sess.run([action, Qout], feed_dict={board_vals:obs})
            print a
            if(random.random() < EPSILON):
                a[0] = env.action_space.sample()

            obs, reward, done, info = env.step(a[0])

            new_q_values = sess.run(Qout, feed_dict={board_vals:obs})

            # V of the new state = max of the q values
            maxQ1 = np.max(Q1)

            _, W1 = sess.run([updateModel, W], feed_dict={board_vals: , nextQ: new_q_values})

        env.render()