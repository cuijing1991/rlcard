from rlcard.games.rankup.card import RankupCard as Card

class RankupDealer(object):
    ''' Dealer deals a deck of cards at the begining of the game. 
        This toy version of Rankup doesn't hold any table cards.
    ''' 
    def __init__(self, np_random):
        ''' Initializes two decks of cards, each deck contains 54 card including black joker and red joker
        '''
        self.np_random = np_random
        # No Joker card in this prototype)
        suit_list = ['S', 'H', 'D', 'C']
        rank_list = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        self.deck = [Card(suit, rank) for suit in suit_list for rank in rank_list]
        
    def shuffle(self):
        ''' Randomly shuffle the deck
        '''
        self.np_random.shuffle(self.deck)

    def deal_cards(self, players):
        ''' Deal cards to players
        Args:
            players (list): list of RankupPlayer objects
        '''
        assert len(self.deck) % len(players) == 0
        self.shuffle()
        hand_num = int(len(self.deck) / len(players))
        for index, player in enumerate(players):
            hand = self.deck[index*hand_num:(index+1)*hand_num]
            player.set_hand(hand)