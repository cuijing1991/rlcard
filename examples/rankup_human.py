''' An example of human players playing toy Rankup agaist two pretained DQN agents.
'''

import rlcard
from rlcard import models
from rlcard.agents import RankupHumanAgent as HumanAgent
from rlcard.utils import print_card
import numpy as np

# # Make environment
# # Set 'record_action' to True because we need it to print results
env = rlcard.make('rankup', config={'record_action': True})
human_agent1 = HumanAgent(env.action_num, 1)
human_agent3 = HumanAgent(env.action_num, 3)
dqn_agent = models.load('rankup-dqn').agents[0]
env.set_agents([dqn_agent, human_agent1, dqn_agent, human_agent3])

print(">> Rankup pre-trained model")
print(">> Start a new game")

trajectories, payoffs = env.run(is_training=False)
# If the human does not take the final action, we need to
# print other players action
if len(trajectories[0]) != 0:
    final_state = trajectories[0][-1][-2]
    action_record = final_state['action_record']
    state = final_state['raw_obs']
    action_list = []
    for i in range(1, len(action_record)+1):
        action_list.insert(0, action_record[-i])
    for pair in action_list:
        print('>> Player', pair[0], 'chooses', pair[1])


print('===============     Result     ===============')
print('Raw payoffs:', payoffs)
accumulated_payoffs = np.sum(payoffs, axis=0)
print('DQN player 0:', accumulated_payoffs[0])
print('Human player 1:', accumulated_payoffs[1])
print('DQN player 2:', accumulated_payoffs[2])
print('Huamn player 3:', accumulated_payoffs[3])