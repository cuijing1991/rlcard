from rlcard.utils.utils import print_card


class HumanAgent(object):
    ''' A human agent for Doudizhu. It can be used to play against trained models
    '''

    def __init__(self, action_num, id):
        ''' Initilize the human agent
        Args:
            action_num (int): the size of the ouput action space
        '''
        self.use_raw = True
        self.action_num = action_num
        self.id = id

    def step(self, state):
        ''' Human agent will display the state and make decisions through interfaces
        Args:
            state (dict): A dictionary that represents the current state
        Returns:
            action (int): The action decided by human
        '''
        _print_state(state['raw_obs'], state['action_record'], self.id)
        action = int(input('>> You choose action (integer): '))
        while action < 0 or action >= len(state['raw_obs']['legal_actions']):
            print('Action illegel...')
            action = int(input('>> Re-choose action (integer): '))
        return state['raw_obs']['legal_actions'][action]

    def eval_step(self, state):
        ''' Predict the action given the curent state for evaluation. The same to step here.
        Args:
            state (numpy.array): an numpy array that represents the current state
        Returns:
            action (int): the action predicted (randomly chosen) by the random agent
            probs (list): The list of action probabilities
        '''
        return self.step(state), []

def _print_state(state, action_record, agent_id):
    ''' Print out the state
    Args:
        state (dict): A dictionary of the raw state
        action_record (list): A list of the historical actions
    '''
    print('===============   Game Info    ===============')
    print('>> Lord Card', state['lord'])
    print('')
    
    print('>> Your ID', agent_id)
    
    print('===============   Raw State   ================')
    print(state)
    
    print('===============   Action Logs   ==============')
    action_list = []
    for i in range(1, len(action_record) + 1):
        action_list.insert(0, action_record[-i])
    for pair in action_list:
        print('>> Player', pair[0], 'chooses', pair[1])
    print('')
           
    print('===============   Your Hand    ===============')
    current_hand = state['current_hand']
    current_hand = sorted(current_hand, key=lambda x: x.value, reverse=False)
    print(current_hand)
    hand_size = len(current_hand)
    batch_size = 8
    i = 0
    while i < hand_size:
        print_card([str(current_hand[j]) for j in range(i, min(i + batch_size, hand_size))])
        i = i + batch_size          
    print('')
   
    print('=========== Actions You Can Choose ===========')
    print(', '.join([str(index) + ': ' + str(action) for index, action in enumerate(state['legal_actions'])]))
    print('')