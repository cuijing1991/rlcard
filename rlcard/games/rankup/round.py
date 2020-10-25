class RankupRound(object):
    ''' Keep track of the cards played by all players in a single round.
    '''
    
    def __init__(self, player_num):
        self.player_num = player_num
        self.starter_id = None
        self.played_cards = []
        
    def start(self, starter_id):
        self.starter_id = starter_id
        
    def record(self, played_card):
        self.played_cards.append(played_card)
    
    def get_player_num(self):
        return self.player_num
    
    def get_starter_id(self):
        return self.starter_id
    
    def get_played_cards(self):
        return self.played_cards
        