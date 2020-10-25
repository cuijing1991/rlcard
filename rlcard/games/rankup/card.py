from enum import Enum

# Constants
SUITS = ['S', 'H', 'D', 'C']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
JOKERS = ['BJ', 'RJ']
FULL_DECK = [suit + rank for suit in SUITS for rank in RANKS]
FULL_DECK_ENCODING_MAP = {value: index for index, value in enumerate(FULL_DECK)}
DECK_SIZE = 52

class RankupCard(object):
    ''' RankupCard stores suit and rank, and additonally a boolean of whether this card is lord.
    Note:
        The suit variable in a standard card game should be one of [S, H, D, C, BJ, RJ],
        meaning [Spades, Hearts, Diamonds, Clubs, Black Joker, Red Joker]
        Similarly the rank variable should be one of [2, 3, 4, 5, 6, 7, 8, 9, T, J, Q, K, A]
    '''
    rank = None
    suit = None
    
    # Value for comparison
    value = None
    
    valid_suit = ['S', 'H', 'D', 'C', 'BJ', 'RJ']
    valid_rank = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
    
    def __init__(self, suit, rank):
        ''' Initialize the suit and rank of a card
        Args:
            suit: RankupSuit, suit of the card
            rank: RankupRank, rank of the card
        '''
        self.suit = suit
        self.rank = rank
    
    def initialize_value(self, lord):
        ''' Set a magic value for the card.
        Args:
            lord: RankupCard, the lord card
        '''
        suit_match = (self.suit == lord.suit)
        rank_match = (self.rank == lord.rank)
        
        if self.suit == 'RJ':
            self.value = 500
        elif self.suit == 'BJ':
            self.value = 400
        elif suit_match and rank_match:
            self.value = 300
        elif rank_match:
            self.value = 200
        elif suit_match:
            self.value = 100 + FULL_DECK_ENCODING_MAP[self.__str__()]
        else:
            self.value = FULL_DECK_ENCODING_MAP[self.__str__()]
    
    def get_suit(self):
        return self.suit
    
    def get_rank(self):
        return self.rank
    
    def is_lord(self):
        return self.value > FULL_DECK_ENCODING_MAP[self.__str__()]
    
    def get_rankup_suit(self):
        if self.is_lord():
            return RankupSuit.LORDS.value
        else:
            return self.suit
        
    def __ge__(self, other):
        if self.is_lord():
            return self.value >= other.value
        elif other.is_lord():
            return False
        elif self.suit == other.suit:
            return self.value >= other.value
        else:
            return True
    
    def __eq__(self, other):
        return self.rank == other.rank and self.suit == other.suit

    def __hash__(self):
        suit_index = RankupCard.valid_suit.index(self.suit)
        rank_index = RankupCard.valid_rank.index(self.rank)
        return rank_index + 100 * suit_index

    def __str__(self):
        ''' Get string representation of a card.
        Returns:
            string: the combination of suit and rank of a card. Eg: AS, 5H, JD, 3C, ...
        '''
        return self.suit + self.rank
    
    def __repr__(self):
        return self.suit + self.rank

class RankupSuit(Enum):
    ''' RankupSuit defines the suits of the game. 
        A card's RankupSuit can be different from its face suit.
    '''
    SPADES = 'S'
    HEARTS = 'H'
    DIAMONDS = 'D'
    CLUBS = 'C'
    LORDS = 'L'
    
class RankupRank(Enum):
    R_2 = '2'
    R_3 = '3'
    R_4 = '4'
    R_5 = '5'
    R_6 = '6'
    R_7 = '7'
    R_8 = '8'
    R_9 = '9'
    R_T = 'T'
    R_J = 'J'
    R_Q = 'Q'
    R_K = 'K'
    R_A = 'A'

   
    