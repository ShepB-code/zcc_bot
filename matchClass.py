#Match Class


class Match:
    def __init__(self, opponent_one, score_one, opponent_two, score_two):
        self.opponent_one = opponent_one
        self.score_one = score_one
        self.opponent_two = opponent_two
        self.score_two = score_two
    
    def get_winner(self):
        if self.score_one > self.score_two:
            return self.opponent_one
        elif self.score_one < self.score_two:
            return self.opponent_two
        else:
            return None