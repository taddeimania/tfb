from django.db import models
from players import models as player_models

class Matchup(models.Model):
    week = models.IntegerField()
    league = models.ForeignKey(player_models.League, related_name='league')
    team_one = models.ForeignKey(player_models.Team, related_name='team_one')
    team_one_points = models.IntegerField()
    team_two = models.ForeignKey(player_models.Team, related_name='team_two')
    team_two_points = models.IntegerField()
    winner = models.ForeignKey(player_models.Team, related_name='winner', null=True)

    def __unicode__(self):
        return "{} vs. {}".format(self.team_one, self.team_two)