from rlcard.games.rankup.card import RankupCard as Card
from rlcard.games.rankup.card import DECK_SIZE
from rlcard.games.rankup.card import FULL_DECK_ENCODING_MAP
    
def encode_cards(cards):
    ''' Encodes the cards to 0-1 based vector representation.
    Args:
        cards: a list of Card objects
    Returns:
        the 0-1 based vector representation of the cards
    '''
    encoded_cards = [0] * DECK_SIZE
    for card in cards:
        encoded_cards[FULL_DECK_ENCODING_MAP[str(card)]] = 1
    return encoded_cards

def decode_cards(encoded_cards):
    ''' Decodes the 0-1 based vector representation to a list of Card objects.
    Args:
        encoded_cards: a 0-1 based vector representation of the cards 
    Returns:
        a list of Card objects
    '''
    return [Card(FULL_DECK[i][0], FULL_DECK[i][1]) for i, value in enumerate(encoded_cards) if value == 1]