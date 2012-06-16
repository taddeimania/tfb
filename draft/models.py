from django.db import models
from tfb.players import models as player_models

class Draft(models.Model):
    league = models.ForeignKey(player_models.League)
    cur_round = models.IntegerField()

class DraftTeam(models.Model):
    draft = models.ForeignKey(Draft)
    team = models.ForeignKey(player_models.Team)

class DraftOrder(models.Model):
    draft_team = models.ForeignKey(DraftTeam)
    position = models.IntegerField()

class DraftPick(models.Model):
    round = models.IntegerField()
    draft_team = models.ForeignKey(DraftTeam)
    player = models.ForeignKey(player_models.Player)
