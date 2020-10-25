from rlcard.games.rankup import Card
from rlcard.games.rankup.utils import encode_cards

class RankupPlayer(object):
    ''' Player stores cards in the player's hand.
    '''

    def __init__(self, player_id, np_random):
        ''' Every player should have a unique player id
        '''
        self.player_id = player_id
        self.np_random = np_random
        self.hand = None
        self.hand_by_suit = None
        self.played_cards = []
        
    def current_hand(self):
        return list(self.hand)
    
    def current_hand_by_suit(self, suit):
        return list(self.hand_by_suit[suit])

    def set_hand(self, cards):
        ''' Set the initial hand.
        Arguments:
            cards: a list of Card objects
        ''' 
        self.hand = set(cards)
    
    def sort_hand(self):
        self.hand_by_suit = {'S': set(), 'H': set(), 'D': set(), 'C': set(), 'L': set()}
        for card in self.hand:
            self.hand_by_suit[card.get_rankup_suit()].add(card)
             
    # TODO: This can be moved out of RankupPlayer class.
    def get_state(self, game_lord, action_history, round, legal_actions):
        '''Construct a state based on the current hand, the action history, and the round information
        Arguments:
            lord: a Card object
            action_history: [[]], action history associated with each palyer
            round: a Round object
            legal_actions: [], legal actions (not id). In this prototype, each action is just a RankupCard object.
        '''
        current_hand = list(self.hand)
        
        lord = [game_lord]
        
        players_num = len(action_history)
        # Put this player's action history at the front, and then the following players in the play order.
        played_cards = [action_history[(self.player_id + i) % players_num] for i in range(players_num)]
        
        round_starter_id = round.get_starter_id()
        round_played_cards = round.get_played_cards()
        round_actions_num = len(round_played_cards)
        assert round_actions_num < players_num
        round = [[(round_played_cards[round_actions_num - i - 1])] for i in range(round_actions_num)]

        state = {'lord': lord,
                 'current_hand': current_hand,
                 'played_cards': played_cards,
                 'round': round,
                 'legal_actions': legal_actions}
        return state

    def play(self, action):
        ''' Apply the given action. 
        Arguments:
            action: a single Card object
        '''
        self.hand.remove(action)
        self.hand_by_suit[action.get_rankup_suit()].remove(action)
        self.played_cards.append(action)
    
    def play_back(self):
        ''' Restore recorded cards back to self.hand
        '''
        raise NotImplementedError

