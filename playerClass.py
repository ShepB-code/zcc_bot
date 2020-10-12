#Player class


class PlayerClass:
    
    def __init__(self, player_name, clan, player_image, cs_wins=0, cs_matches=0):
        self.player_name = player_name
        self.clan = clan
        self.player_image = player_image
        self.cs_wins = cs_wins
        self.cs_matches = cs_matches
        self.win_rate = self.update_win_rate()
    
    def update_win_rate(self):
            if self.cs_matches != 0:
                self.win_rate = float(self.cs_wins) / float(self.cs_matches)
            else:
                self.win_rate = 0
    def get_player_data(self):
        data = dict()
        data["player_name"] = self.player_name
        data["clan"] = self.clan
        data["player_image"] = self.player_image
        data["cs_wins"] = self.cs_wins
        data["cs_matches"] = self.cs_matches
        data["win_rate"] = self.win_rate
        return data