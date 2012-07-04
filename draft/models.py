from django.db import models
from tfb.players import models as player_models

class Draft(models.Model):
    league = models.ForeignKey(player_models.League)
    cur_round = models.IntegerField()

    def __unicode__(self):
        return str(self.league)

class DraftTeam(models.Model):
    draft = models.ForeignKey(Draft)
    team = models.ForeignKey(player_models.Team)

    def __unicode__(self):
        return str(self.team)

class DraftOrder(models.Model):
    draft_team = models.ForeignKey(DraftTeam)
    position = models.IntegerField()

    def __unicode__(self):
        return str(self.draft_team)

class DraftPick(models.Model):
    round = models.IntegerField()
    draft_team = models.ForeignKey(DraftTeam)
    player = models.ForeignKey(player_models.Player)

    def __unicode__(self):
        return str(self.draft_team)
