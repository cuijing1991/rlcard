import numpy as np
from rlcard.envs import Env
from rlcard.games.rankup.card import FULL_DECK
from rlcard.games.rankup.card import FULL_DECK_ENCODING_MAP
from rlcard.games.rankup.utils import encode_cards
from rlcard.games.rankup import Game

class RankupEnv(Env):
    ''' Rankup Environment
    '''
    
    def __init__(self, config):
        self.name = 'rankup'
        self.game = Game()
        super().__init__(config)
        
        # FULL_DECK size is 52
        self.state_shape = [9, 52]   
    
    def compute_transition_trajectories(self, trajectories, payoffs):
        '''
            Reorganize trajectories in the format of (state, action, reward, next_state, is_done)
        Args:
            trajectories (list of list): A list of trajectories. Each inner list corresponds to one player's trajectory.
            payoffs (list of list): A list of payoffs for the players. Each inner list corresponds to one round's payoff.

        Returns:
            (list): A new trajectories that can be fed into RL algorithms.
        '''
        player_num = len(trajectories)
        new_trajectories = [[] for _ in range(player_num)]
        accumulated_reward = [0 for _ in range(player_num)]

        for player in range(player_num):
            for i in range(0, len(trajectories[player])-2, 2):
                reward = payoffs[int(i/2)][player]
                accumulated_reward[player] += reward
                if i == len(trajectories[player])-3:
                    done = True
                else:
                    done = False
                transition = trajectories[player][i:i+3].copy()
                transition.insert(2, reward/20)
                transition.append(done)

                new_trajectories[player].append(transition)
        return new_trajectories
    
    def get_payoffs(self):
        ''' Get the payoffs of players.

        Returns:
            payoffs (list of list): A list of payoffs for the players. Each inner list corresponds to one round's payoff.
        '''
        return self.game.get_payoffs()
           
    def _extract_state(self, state):
        ''' Extract useful information from state for RL.
        Args:
            state (dict): The raw state
        Returns:
            numpy.array: The extracted state that contains 'obs' in state_shape
        '''
        obs = np.zeros((9, 52), dtype=int)
        # Game lord
        obs[0] = encode_cards(state['lord'])
        # Current hand
        obs[1] = encode_cards(state['current_hand'])
        # The cards that have been played by each player
        for i, played in enumerate(state['played_cards']):
            obs[2+i] = encode_cards(played)
        # The previous actions of the current round, at most 3 actions. All-zero array means placeholder.
        for j, action in enumerate(state['round']):
            obs[6+j] = encode_cards(action)
        
        extracted_state = {'obs': obs, 'legal_actions': self._get_legal_action()}
        if self.allow_raw_data:
            extracted_state['raw_obs'] = state
            extracted_state['raw_legal_actions'] = state['legal_actions']
        if self.record_action:
            extracted_state['action_record'] = self.action_recorder   
        return extracted_state
       
    def _decode_action(self, action_id):
        ''' Action id -> the action in the game. Must be implemented in the child class.
        Args:
            action_id (int): the id of the action
        Returns:
            action (string): the action that will be passed to the game engine.
        '''
        return self.game.decode_action(action_id)
    
    def _get_legal_action(self):
        ''' Get all legal actions for current state
        
        Returns:
            legal_action_id (list of int): a list of legal actions' id
        '''             
        legal_action_ids = []
        legal_actions = self.game.state['legal_actions']
        for action in legal_actions:
            legal_action_ids.append(FULL_DECK_ENCODING_MAP[str(action)])
        return legal_action_ids
        
        
        
        
        
        
        
        
        
        
        
    
    