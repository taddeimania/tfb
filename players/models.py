from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from tfb.tecmo_player.models import Stats, Player

MAX_ROSTER = 7

def getweek():
    """ Returns current week from the curweek table
    """
    return Curweek.objects.get(pk=1).curweek

class LeagueManager(models.Manager):

    def get_public(self):
        return self.filter(invite_code=None)

    def get_team_count(self, id):
        return Team.objects.filter(league=id).count()

class League(models.Model):
    lname = models.CharField(max_length=30)
    lslogan = models.CharField(max_length=200, null=True)
    maxteam = models.IntegerField()
    active = models.CharField(max_length=1)
    invite_code = models.CharField(max_length=30, null=True)

    objects = LeagueManager()

    def __unicode__(self):
        return self.lname

    def generate_hash(self):
        league = League.objects.get(pk=self.id)
        league.invite_code = abs(hash(league.lname))
        league.save()

    def is_valid_league(self):
        teams = Team.objects.filter(league = self.id)
        if teams.count() == self.maxteam and teams.count() % 2 == 0:
            return True
        else:
            return False

    def is_league_available(self):
        """ Returns true if the league requested is available to publicly join.
            TODO: Apply a check for private leagues
        """
        if (Team.objects.filter(league = self).count() < self.maxteam) and \
           self.active != 'N' and not self.invite_code:
            return True
        else:
            return False

    def team_count(self):
        return Team.objects.filter(league=self).count()

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    username = models.CharField(max_length=30)
    userpic = models.CharField(max_length=2)

    def __unicode__(self):
        return self.username

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)

    def are_you_at_max_roster(self):
        if Roster.objects.get_roster_this_week(self).count() >= MAX_ROSTER:
            return True
        return False

    @property
    def team(self):
        try:
            return Team.objects.get(owner=self)
        except DoesNotExist:
            return None

    post_save.connect(create_user_profile, sender=User)

class TeamManager(models.Manager):

    def get_owner_for_player_this_week(self, userleague, player):
        return self.get(
            league=userleague, roster__player=player, roster__week=getweek()
        ).owner

    def get_my_team(self, user):
        return self.get(owner=user.userprofile)

class Team(models.Model):
    owner = models.ForeignKey(UserProfile)
    league = models.ForeignKey(League)
    name = models.CharField(max_length=45)
    win = models.IntegerField()
    loss = models.IntegerField()
    slogan = models.CharField(max_length=200)
    total_points = models.IntegerField()
    total_points_against = models.IntegerField()
    iscommish = models.CharField(max_length=1, null=True, choices=(('Y', 'Yes'), ('N', 'No')))
    objects = TeamManager()

    def __unicode__(self):
        return self.name

    def calc_week_points(self, _week=None):
        total_points = 0
        if not _week:
            _week = Curweek.objects.get(pk=1).curweek
        roster = Roster.objects.filter(week = _week, team=self.id)
        for _player in roster:
            try:
                total_points += Stats.objects.get(week = _week,player = _player.player).fanpts
            except:
                total_points = total_points

        return total_points

class RosterManager(models.Manager):

    def get_roster_this_week(self, user):
        return Roster.objects.filter(week = getweek(), team__owner = user)

class Roster(models.Model):
    week = models.IntegerField()
    team = models.ForeignKey(Team)
    player = models.ForeignKey(Player)
    objects = RosterManager()

class Curweek(models.Model):
    curweek = models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.curweek)

class Transaction(models.Model):
    timestamp = models.DateTimeField()
    action = models.CharField(max_length=10)
    team = models.ForeignKey(Team)
    league = models.ForeignKey(League)
    owner = models.ForeignKey(UserProfile)
    player = models.ForeignKey(Player)

#start rebuilding data to use this table
class Season(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=50)

    def __unicode__(self):
        return self.name

class Trophy(models.Model):
    name = models.CharField(max_length=25)
    description = models.CharField(max_length=50)
    image = models.CharField(max_length=25)

    def __unicode__(self):
        return self.name

class TrophyAssignment(models.Model):
    profile = models.ForeignKey(UserProfile)
    season = models.ForeignKey(Season)
    trophy = models.ForeignKey(Trophy)

    def __unicode__(self):
        return str(self.trophy)

class SeasonRankingManager(models.Manager):

    def get_position(self, pos):
        if pos[-1] in [1, 2, 3, 4]:
            pos = pos[:-1]
        return self.filter(player__pos__startswith=pos.upper())

class SeasonRanking(models.Model):
    ranking = models.IntegerField()
    player = models.ForeignKey(Player)

    objects = SeasonRankingManager()

    class Meta:
        ordering = ['ranking']

    def __unicode__(self):
        return "{} - {}".format(self.ranking, self.player)