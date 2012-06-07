from players import models

class DisplayLeague():

    def __init__(self, league):
        self.id = league.id
        self.name = league.lname
        self.teamcount = models.League.objects.get_team_count(league.id)
        self.maxteam = league.maxteam