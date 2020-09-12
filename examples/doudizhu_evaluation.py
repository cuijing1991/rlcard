''' An example of playing Doudizhu with random agents
'''

import rlcard
from rlcard import models
from rlcard.utils import set_global_seed
from rlcard.agents import RandomAgent
from datetime import datetime

# Make environment
env = rlcard.make('doudizhu', config={'seed': int(datetime.now().timestamp())})
episode_num = 100

# Set a global seed
set_global_seed(0)

# Set up agents
random_agent = RandomAgent(action_num=env.action_num)
dqn_agent = models.load('doudizhu-dqn').agents[0]

nfsp_agents = models.load('doudizhu-nfsp').agents

env.set_agents([dqn_agent, nfsp_agents[1], nfsp_agents[2]])

win_status = [0, 0, 0]

for episode in range(episode_num):

    # Generate data from the environment
    trajectories, player_wins = env.run(is_training=False)
    win_status = win_status + player_wins
    
print("DQN v.s. NFSP scores: ", win_status)

############################################################

env.set_agents([nfsp_agents[0], dqn_agent, dqn_agent])

win_status = [0, 0, 0]

for episode in range(episode_num):

    # Generate data from the environment
    trajectories, player_wins = env.run(is_training=False)
    win_status = win_status + player_wins
    
print("NFSP v.s. DQN scores: ", win_status)