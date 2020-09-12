from rlcard.utils.utils import print_card


class HumanAgent(object):
    ''' A human agent for Doudizhu. It can be used to play against trained models
    '''

    def __init__(self, action_num):
        ''' Initilize the human agent
        Args:
            action_num (int): the size of the ouput action space
        '''
        self.use_raw = True
        self.action_num = action_num

    @staticmethod
    def step(state):
        ''' Human agent will display the state and make decisions through interfaces
        Args:
            state (dict): A dictionary that represents the current state
        Returns:
            action (int): The action decided by human
        '''
        _print_state(state['raw_obs'], state['action_record'])
        action = int(input('>> You choose action (integer): '))
        while action < 0 or action >= len(state['raw_obs']['actions']):
            print('Action illegel...')
            action = int(input('>> Re-choose action (integer): '))
        return state['raw_legal_actions'][action]

    def eval_step(self, state):
        ''' Predict the action given the curent state for evaluation. The same to step here.
        Args:
            state (numpy.array): an numpy array that represents the current state
        Returns:
            action (int): the action predicted (randomly chosen) by the random agent
            probs (list): The list of action probabilities
        '''
        return self.step(state), []

def _print_state(state, action_record):
    ''' Print out the state
    Args:
        state (dict): A dictionary of the raw state
        action_record (list): A list of the historical actions
    '''
    print('===============   Game Info    ===============')
    print('>> Landlord is Player', state['landlord'])
    print('')
    
    print('===============   Action Logs   ==============')
    _action_list = []
    for i in range(1, len(action_record)+1):
        _action_list.insert(0, action_record[-i])
    for pair in _action_list:
        print('>> Player', pair[0], 'chooses', pair[1])
    print('')
    
    print('===============   Your Hand    ===============')
    print(state['current_hand'])
    print('')
   
    print('=========== Actions You Can Choose ===========')
    print(', '.join([str(index) + ': ' + action for index, action in enumerate(state['actions'])]))
    print('')