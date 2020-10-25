''' An example of learning a Deep-Q Agent on Rankup - toy version
'''

import tensorflow as tf
import os

import rlcard
from rlcard.agents import DQNAgent
from rlcard.agents import RandomAgent
from rlcard.utils import set_global_seed, tournament
from rlcard.utils import Logger

# Make environment
env = rlcard.make('rankup', config={'seed': 0})
eval_env = rlcard.make('rankup', config={'seed': 0})

# Set the iterations numbers and how frequently we evaluate the performance

episode_num = 10000
evaluate_every = 1000

# Number of games to play in each evaluation
tournament_play_num = 500

# The intial memory size (default=100)
replay_memory_init_size = 1000
# The total memory size (default=20000)
replay_memory_size = 20000

# Train the agent every X games (default=1)
train_every = 10
# Each train batch samples X games from memory (default=32)
batch_size = 32
# Update target model every X training (default=1000)
update_target_estimator_every = 1000


# The paths for saving the logs and learning curves
log_dir = './experiments/rankup_dqn_result/'

# Set a global seed
set_global_seed(0)

with tf.Session() as sess:

    # Initialize a global step
    global_step = tf.Variable(0, name='global_step', trainable=False)

    # Set up the agents
    agent = DQNAgent(sess,
                     scope='dqn',
                     action_num=env.action_num,
                     replay_memory_init_size=replay_memory_init_size,
                     train_every=train_every,
                     batch_size=batch_size,
                     update_target_estimator_every=update_target_estimator_every,
                     state_shape=env.state_shape,
                     mlp_layers=[520, 260])

    random_agent = RandomAgent(action_num=eval_env.action_num)
    env.set_agents([agent, agent, agent, agent])
    eval_env.set_agents([agent, random_agent, agent, random_agent])

    # Initialize global variables
    sess.run(tf.global_variables_initializer())

    # Init a Logger to plot the learning curve
    logger = Logger(log_dir)

    for episode in range(episode_num):

        # Generate data from the environment
        trajectories, _ = env.run(is_training=True)

        # Feed transitions into agent memory, and train the agent
        for ts in trajectories[0]:
            agent.feed(ts)

        # Evaluate the performance. Play with random agents.
        if episode % evaluate_every == 0:
            logger.log_performance(env.timestep, tournament(eval_env, tournament_play_num)[0])
            logger.log_performance(env.timestep, tournament(eval_env, tournament_play_num)[0])
            logger.log_performance(env.timestep, tournament(eval_env, tournament_play_num)[0])

    # Close files in the logger
    logger.close_files()

    # Plot the learning curve
    logger.plot('DQN')
    
    # Save model
    save_dir = 'models/rankup_dqn'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    saver = tf.train.Saver()
    saver.save(sess, os.path.join(save_dir, 'model'))
    
