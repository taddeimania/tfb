from django.db.models import Q
from tfb.players.models import Roster, Team, Player, Curweek, \
    Schedule, Pro_Team, Stats, UserProfile, Transaction
from tfb.draft.models import DraftPick

MAX_ROSTER = 7

def is_player_available_in_your_league(user, player_id):
    """ Is player available in your league. Returns True if you are allowed to add the requested
    	player to your roster, returns false if they are currently owned by another team.
    """
    return False if Roster.objects.filter(
        week=getweek(),
        team__league=getleague(user),
        player__id=player_id
    ).exists() else  True


def avail_list(user, posid):
    """ Returns a list of available players in your league.
    """
    team = Team.objects.get(owner = user.userprofile.id)
    plist = Player.objects.filter(pos__startswith=posid).exclude(roster__team__league = team.league,
        roster__week = getweek()).exclude(stats__week = getweek())
    plist = [player.SeasonTotal() for player in plist]
    pbyes = Player.objects.filter(pos__startswith=posid, stats__week = getweek(), stats__tm2 = 'BYE').exclude(roster__team__league = team.league,
        roster__week = getweek())

    plist.sort(key=lambda x: x.Allfanpts, reverse=True)

    for player in pbyes:
        plist.append(player)

    return plist


def player_on_my_roster(user, player_id):
    """ Returns true if player_id is not currently in your roster.
    """
    if player_id not in list(Roster.objects.get_roster_this_week(user.userprofile)):
        return True
    else:
        return False


def ispositionopen(user,posid):
    """ Returns true if you currently don't have a player in the corresponding slot on your roster.
    	Returns false if there is currently a player in that slot - making the position unfillable.
    """
    maxpos = 2
    if posid == 'QB' or posid == 'K' or posid == 'TE':
        maxpos = 1

    team = Team.objects.get(owner=user.userprofile.id)
    roster = Roster.objects.filter(week = getweek(), team = team,
        player__pos__startswith=posid).count()

    if roster < maxpos:
        return True
    else:
        return False

def setplayertoroster(user,player):
    """ Applies a pro player to your roster and apply all logic
    	constraints before player is added.
    """
    if not player.is_player_locked()\
       and is_player_available_in_your_league(user, player.id)\
       and player_on_my_roster(user, player.id)\
       and not user.userprofile.are_you_at_max_roster()\
       and getweek() != 0\
    and ispositionopen(user,player.pos):
        T = Team.objects.get(owner = user.userprofile.id)
        r = Roster(week = getweek(), team = T, player = player)
        r.save()
        add_record(user.userprofile.id, player.id, 'ADD')
        return "success"
    else:
        return "failure"


def getteam(user):
    """ Returns your team... duh.
    """
    return Team.objects.get(owner=user.userprofile.id)


def getleague(user):
    return Team.objects.get(owner = user.userprofile.id).league


def getweek():
    """ Returns current week from the curweek table
    """
    return Curweek.objects.get(pk=1).curweek


def getteamschedule(pro_team_id):
    """ Returns a pro_team's schedule
    """
    return Schedule.objects.filter(Q(away=pro_team_id) | Q(home=pro_team_id))


def getproteamopponent(pro_team_id, week):
    """ Returns the pro_team's opponent for a given week.
    	TODO: overload function to handle just pro_team_id to return current opponent.
    """
    for x in Schedule.objects.filter(Q(away=pro_team_id) | Q(home=pro_team_id), week=week):
        if x.home == pro_team_id:
            return Pro_Team.objects.get(short=x.away)
        else:
            return Pro_Team.objects.get(short=x.home)


def evennumberofteams(_league):
    """ Returns status of league depending on the number of teams
    """
    if Team.objects.filter(league = _league.id).count() % 2 == 0:
        return True
    return False


def draft_avail_players(league):
    """ Isn't it obvious what this returns?  Cmon it's a simple return statement.
        Gets a full list of players -> excludes players that currently have a draft pick entered for them
            in your league.
    """
    return Player.objects.all().exclude(
        id__in=[x.player.id for x in DraftPick.objects.filter(draft_team__draft__league = league)]
    )


def drop_player(player, team, user):
    """ If business rules pass, this will drop a player... kind of wish this was a private method.
    """
    player_drop = Player.objects.get(pk=player)
    if not player_drop.is_player_locked():
        Roster.objects.get(week=getweek(), team=team.id, player=player_drop).delete()
        add_record(user.userprofile.id, player_drop.id, 'DROP')
    else:
        return "Cannot drop " + player_drop.player_name + ", he's already played this week"

def stats_to_dict(curstats):
    """ Why is this a dictionary when it could be a beautiful object?
    """
    return {
        'name':curstats.player,
        'pasyds':curstats.pasyds,
        'pastd':curstats.pastd,
        'intcp':curstats.intcp,
        'recyds':curstats.recyds,
        'rectd':curstats.rectd,
        'rusyds':curstats.rusyds,
        'rustd':curstats.rustd,
        'xpm':curstats.xpm,
        'fgm':curstats.fgm,
        'fanpts':curstats.fanpts,
        'id':curstats.player.id,
        'health':curstats.health,
        'tm2':curstats.tm2,
        }

def roster_to_dict(roster, blank_stats=None):
    """ Wow this was painful to write
    """
    roster_dict = {}
    pos_list_copy = ['QB','RB','RB','WR','WR','TE','K']

    for player in roster:
        week = roster[0].week
        pos = player.player.pos
        posid = pos
        if (s for s in pos_list_copy if pos in s):
            if (Stats.objects.filter(player=player.player, week=week).exists() and (week <= getweek())) and not blank_stats:
                info = stats_to_dict(Stats.objects.get(player=player.player, week=week))
            else:
                info = {'name':player.player, 'id':player.player.id}
            info.update({'pic':player.player.picture})
            if pos != 'K': posid = pos[:-1]
            if posid in roster_dict:
                posid = str(posid) + '1'
            roster_dict.update({posid:info})

    return roster_dict

def add_record(_userprofile, _player, _action):
    """ Who let the trailing underscore monster in here?
        This adds a record to the transaction table used for reporting player moves.
        TODO: Need to evolve this to account of player trades someday.
    """
    import datetime
    _team = Team.objects.get(owner = _userprofile)
    profile = UserProfile.objects.get(pk = _userprofile)
    player = Player.objects.get(pk = _player)
    T = Transaction(timestamp = datetime.datetime.now(), action = _action, team= _team, league=_team.league,
        owner=profile, player=player)
    T.save()