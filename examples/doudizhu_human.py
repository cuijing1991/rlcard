''' A toy example of playing against pretrianed AI on Doudizhu
'''

import rlcard
from rlcard import models
from rlcard.agents import DoudizhuHumanAgent as HumanAgent
from rlcard.utils import print_card

# Make environment
# Set 'record_action' to True because we need it to print results
env = rlcard.make('doudizhu', config={'record_action': True})
human_agent = HumanAgent(env.action_num)
dqn_agent = models.load('doudizhu-dqn').agents[0]
env.set_agents([human_agent, dqn_agent, dqn_agent])

print(">> Doudizhu pre-trained model")

while (True):
    print(">> Start a new game")

    trajectories, payoffs = env.run(is_training=False)
    # If the human does not take the final action, we need to
    # print other players action
    if len(trajectories[0]) != 0:
        final_state = trajectories[0][-1][-2]
        action_record = final_state['action_record']
        state = final_state['raw_obs']
        _action_list = []
        for i in range(1, len(action_record)+1):
            """
            if action_record[-i][0] == state['current_player']:
                break
            """
            _action_list.insert(0, action_record[-i])
        for pair in _action_list:
            print('>> Player', pair[0], 'chooses', pair[1])


    print('===============     Result     ===============')
    if payoffs[0] > 0:
        print('You win!')
    elif payoffs[0] == 0:
        print('It is a tie.')
    else:
        print('You lose!')
    print('')

    input("Press any key to continue...")