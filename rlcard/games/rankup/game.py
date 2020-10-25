## Rankup Toy Version - only uses one deck of cards without Jokers.

import numpy as np
from rlcard.games.rankup import Player
from rlcard.games.rankup import Round
from rlcard.games.rankup import Judge
from rlcard.games.rankup import Dealer
from rlcard.games.rankup import Card

from rlcard.games.rankup.card import SUITS
from rlcard.games.rankup.card import RANKS
from rlcard.games.rankup.card import FULL_DECK
from rlcard.games.rankup.card import DECK_SIZE

class RankupGame(object):
    ''' Provide game APIs for env to run rankup and get corresponding state information.
    '''
    
    def __init__(self):
        self.np_random = np.random.RandomState()
        self.player_num = 4
    
    def init_game(self):
        ''' Starts the game
        
        Returns:
            dict: first state in one game
            int: current player's id
        '''
        
        # Initialize game state
        self.scores = []
        self.rewards = []
        self.action_history = [[], [], [], []]
        self.steps = 0      
        self.winner_id = None
        self.current_player_id = None
        self.lord = None
        self.full_deck_of_cards = None
        
        # Initialize players
        self.players = [Player(num, self.np_random) for num in range(self.player_num)]
        
        # Initialize Dealer.
        self.dealer = Dealer(self.np_random)
        
        # Initialize Judge.
        self.judge = Judge()
        
        # Deal cards.
        self.dealer.deal_cards(self.players)
        
        # Pick a random suit, a random rank as lord.
        # This can be set to a fixed value in order to simply the training process.
        suit_idx = self.np_random.random_integers(low=0, high=3)
        rank_idx = self.np_random.random_integers(low=0, high=12)
        self.lord = Card(SUITS[suit_idx], RANKS[rank_idx])
        
        for player in self.players:
            self.judge.evaluate_cards(self.lord, player.current_hand())
            player.sort_hand()
            
        # full_deck_of_cards is used to look up 'Action' by action id. 
        # 'Action' in this prototype is just a single Card (RankupCard) object. 
        # Each card must be initialized by calling #initialize_value. This is done by judge after lord card is determined.
        self.full_deck_of_cards = [Card(c[0], c[1]) for c in FULL_DECK]
        self.judge.evaluate_cards(self.lord, self.full_deck_of_cards)
        
        # Pick a random player as the starting player.
        self.current_player_id = self.np_random.random_integers(low=0, high=self.player_num-1)
        
        # Initialize round.
        self.round = Round(self.player_num)
        self.round.start(self.current_player_id)
        
        # Get the state of the starting player.
        self.state = self.get_state(self.current_player_id)

        return self.state, self.current_player_id
        
    def step(self, action):
        ''' Perform one draw of the game
        Args:
            action (str): a specific action
            
        Returns:
            dict: next player's state
            int: next player's id
        '''
        player = self.players[self.current_player_id]
        player.play(action)
        self.round.record(action)
        self.action_history[self.current_player_id].append(action)
        self.steps = self.steps + 1
        
        next_player_id = None
              
        if self.steps % self.player_num == 0:
            (round_winner_id, round_scores, rewards) = self.judge.judge_round(self.round)
            next_player_id = round_winner_id
            if round_winner_id % 2 == 0:
                self.add_scores_to_team_1(round_scores)
            else:
                self.add_scores_to_team_2(round_scores)
            self.record_rewards(rewards)
            self.round = Round(self.player_num)
            self.round.start(next_player_id)
        else:
            next_player_id = (self.current_player_id + 1) % 4
        
        next_state = self.get_state(next_player_id)
        
        # Update state and current_player_id at the end of each step.
        self.current_player_id = next_player_id
        self.state = next_state
        
        return self.state, self.current_player_id
    
    def decode_action(self, action_id):
        ''' Decodes the given action id
        Args:
            action_id (int): action id
        Returns:
            RankupCard: a card object that represents the action. 
            (Again, this prototype uses one deck of cards, so each action is just one card.)
        '''
        return self.full_deck_of_cards[action_id]
        
         
    def get_state(self, player_id):
        ''' Return player's state
        Args:
            player_id (int): player id
            
        Returns:
            dict: the state of the player
        '''
        player = self.players[player_id]
        legal_actions = self.judge.get_legal_actions(self.round, player)
        
        state = player.get_state(self.lord, self.action_history, self.round, legal_actions)
        return state
   
    def get_player_num(self):
        return self.player_num
    
    def get_action_num(self):
        return DECK_SIZE
    
    def get_player_id(self):
        ''' Return current player's id

        Returns:
            int: current player's id
        '''
        return self.current_player_id
    
    def is_over(self):
        ''' Judge whether a game is over

        Returns:
            Bool: True(over) / False(not over)
        '''
        if self.steps < DECK_SIZE:
            return False
        else:
            return True
    
    def get_payoffs(self):
        return self.scores 
    
    def add_scores_to_team_1(self, round_score):
        self.scores.append([round_score, -round_score, round_score, -round_score])
        
    def add_scores_to_team_2(self, round_score):
        self.scores.append([-round_score, round_score, -round_score, round_score])
        
    def record_rewards(self, rewards):
        self.rewards.append(rewards)
    