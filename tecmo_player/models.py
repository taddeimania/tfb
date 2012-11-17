from django.db import models


class Pro_Team(models.Model):
    short = models.CharField(max_length=3, primary_key="true")
    long = models.CharField(max_length=45)
    bye = models.IntegerField()
    wins = models.IntegerField()
    loss = models.IntegerField()
    tie = models.IntegerField()

    def __str__(self):
        return self.long

class Player(models.Model):
    pos = models.CharField(max_length=3)
    player_name = models.CharField(max_length=45)
    pro_team = models.ForeignKey(Pro_Team)
    picture = models.CharField(max_length=2)

    def __str__(self):
        return self.player_name

    def is_player_locked(self):
        """ Checks if a player has played yet this week.  A live lock is INP while a sim'd lock is whatever
            Team the player played.
        """
        try:
            if Stats.objects.get_current_opponent_by_player(self) != 'BYE':
                return True
            return False
        except:
            return False

    def SeasonTotal(self):
        stats = Stats.objects.filter(player=self.id)
        try:
            self.Bye = self.pro_team.bye
        except:
            self.Bye = "?"
        try:
            stats = Stats.objects.filter(players=self.id)
            self.Health = Stats.objects.filter(players=self.id, week=max([stat.week for stat in stats]))
        except:
            self.Health = "OK"
        self.Allpa = sum([x.pa for x in stats])
        self.Allpc = sum([x.pc for x in stats])
        self.Allpastd = sum([x.pastd for x in stats])
        self.Allintcp = sum([x.intcp for x in stats])
        self.Allpasyds = sum([x.pasyds for x in stats])
        self.Allrec = sum([x.rec for x in stats])
        self.Allrecyds = sum([x.recyds for x in stats])
        self.Allrectd = sum([x.rectd for x in stats])
        self.Allkrtd = sum([x.krtd for x in stats])
        self.Allprtd = sum([x.prtd for x in stats])
        self.Allrusat = sum([x.rusat for x in stats])
        self.Allrusyds = sum([x.rusyds for x in stats])
        self.Allrustd = sum([x.rustd for x in stats])
        self.Allxpm = sum([x.xpm for x in stats])
        self.Allfgm = sum([x.fgm for x in stats])
        self.Allfanpts = sum([x.fanpts for x in stats])

        return self

class Schedule(models.Model):
    away = models.CharField(max_length=3)
    awayscore = models.IntegerField()
    home = models.CharField(max_length=3)
    homescore = models.IntegerField()
    week = models.IntegerField()

    def __unicode__(self):
        return "{} at {} - week {}".format(self.home, self.away, self.week)

class StatsManager(models.Manager):

    def get_current_opponent_by_player(self, player):
        return self.get(player = player, week = getweek()).tm2

class Stats(models.Model):
    player = models.ForeignKey(Player)
    week = models.IntegerField(default=1)				# week
    pa = models.IntegerField(default=0)				# line[3]
    pc = models.IntegerField(default=0)					# line[2]
    pastd = models.IntegerField(default=0)				# line[4]
    intcp = models.IntegerField(default=0)				# line[5]
    pasyds = models.IntegerField(default=0)			# line[6]
    rec = models.IntegerField(default=0)					# line[7]
    recyds = models.IntegerField(default=0)				# line[8]
    rectd = models.IntegerField(default=0)				# line[9]
    krtd = models.IntegerField(default=0)					# line[12]
    prtd = models.IntegerField(default=0)				# line[15]
    rusat = models.IntegerField(default=0)					# line[16]
    rusyds =  models.IntegerField(default=0)				# line[17]
    rustd = models.IntegerField(default=0)				# line[18]
    xpm = models.IntegerField(default=0)					# line[24]
    fgm = models.IntegerField(default=0)					# line[-7]
    tm2 = models.CharField(max_length=3)					# tm2
    health = models.CharField(max_length=10)
    condition = models.CharField(max_length=10)
    fanpts = models.IntegerField(default=0)
    guid = models.IntegerField(primary_key=True)

    objects = StatsManager()

    def __unicode__(self):
        return self.player.player_name