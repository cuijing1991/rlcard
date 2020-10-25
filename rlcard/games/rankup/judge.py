from rlcard.games.rankup.card import FULL_DECK

class RankupJudge(object):
    ''' Judge decides whether the round/game ends and return the winner of the round/game
    '''
    
    @staticmethod
    def get_legal_actions(round, player):
        ''' Returns all the legal actions of the player given the current round.
        '''
        played_cards = round.get_played_cards()
        if len(played_cards) == 0:
            return player.current_hand()
        else:
            pattern = played_cards[0]
            suit = None
            if pattern.is_lord():
                suit = 'L'
            else:
                suit = pattern.get_suit()
            matched_cards = player.current_hand_by_suit(suit)
            if len(matched_cards) == 0:
                return player.current_hand()
            else:
                return matched_cards
                
    @staticmethod
    def judge_round(round):
        ''' Return the winner of the round and the scores winner gets.
        Returns:
            (int, int, rewards (a list of int)): return the player's id who wins the round, the scores winner gets,
            and the rewards for constructing the trajectories.
        '''
        starter_id = round.get_starter_id()
        player_num = round.get_player_num()
        
        scores = [0, 0, 0, 0]
        rewards = [0, 0, 0, 0]
        winner_id = starter_id
        winner_card = pattern = round.get_played_cards()[0]
        for idx, card in enumerate(round.get_played_cards()):
            player_id = (starter_id + idx) % player_num
            if not RankupJudge.compare(pattern, winner_card, card):
                winner_card = card
                winner_id = player_id
            if card.get_rank() == '5':
                scores[player_id] += 5
            elif card.get_rank() == 'T' or card.get_rank() == 'K':
                scores[player_id] += 10
        total_scores = sum(scores)
        
        for id in range(player_num):
            if id == winner_id:
                # Winner gets the total scores of this round as the reward.
                rewards[id] = total_scores
            if (id - winner_id) % 2 == 0:
                # Teammate of the winner gets the scores they contributed.
                rewards[id] = scores[id]
            else:
                # Losers get pentalized for the scores they contributed.
                rewards[id] = -scores[id]
        return (winner_id, total_scores, rewards)
    
    @staticmethod
    def compare(pattern, card1, card2):
        ''' Returns whether card1 wins over card2. (card1 is the current winner.)
            Be cautious that #compare should only be called in a certain way. See the 'assert' statement below.
        Arguments:
            pattern: a RankupCard object, the pattern of this round, which may or may not be the same as card1. 
            card1: a RankupCard object
            card2: a RankupCard object
        '''
        if pattern.is_lord():
            assert card1.is_lord()
            return card1 >= card2
        else:
            assert card1.is_lord() or card1.get_rankup_suit() == pattern.get_rankup_suit()
            return card1 >= card2
        
    @staticmethod
    def evaluate_cards(lord, cards):
        for card in cards:
            card.initialize_value(lord)
        
    