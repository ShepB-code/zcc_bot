#Clan class

class ClanClass:

    def __init__(self, clan_name, creation_date, leaders, clan_image, cs_wins=0, cs_matches=0):
        self.clan_name = clan_name
        self.creation_date = creation_date
        self.leaders = leaders
        self.clan_image = clan_image
        self.cs_wins = cs_wins
        self.cs_matches = cs_matches
        self.win_rate = 0
        self.update_win_rate()

        self.matches = []

    def update_win_rate(self):
        if self.cs_matches != 0:
            self.win_rate = float(self.cs_wins) / float(self.cs_matches)
        else:
            self.win_rate = 0
            
    def update(self, creation_date=None, leaders=None, clan_image=None, cs_wins=None, cs_matches=None):
        if creation_date:
            self.creation_date = creation_date
        if leaders:
            self.leaders = leaders
        if clan_image:
            self.clan_image = clan_image
        if cs_wins:
            self.cs_wins = cs_wins
            self.update_win_rate()
        if cs_matches:
            self.cs_matches = cs_matches
            self.update_win_rate()
        
    def add_win(self):
        self.update(cs_wins=self.cs_wins + 1)
        self.add_match()
        
    def add_match(self): #Match was a parameter, add later
        #match.append(match)
        self.update(cs_matches=self.cs_matches + 1)

    def get_clan_data(self):
        #Potential Runtime Issue
        data = dict()
        data["clan_name"] = self.clan_name
        data["creation_date"] = self.creation_date
        data["leaders"] = self.leaders
        data["clan_image"] = self.clan_image
        data["cs_wins"] = self.cs_wins
        data["cs_matches"] = self.cs_matches
        data["win_rate"] = self.win_rate
        return data
    def get_name(self):
        return self.clan_name