import random
from django.db.models import Q
from players.models import League, Team, Roster, Curweek, Stats, Schedule, Player, Matchup
from myproject.settings import PROJECT_ROOT

def create_matchup_schedule(list_of_teams, _league):
    # matchup logic sorted by spreadsheet.  Thanks @sarahtaddei for being a spreadsheet wizard
    infile = open(PROJECT_ROOT + '/matchupschedule.csv', 'r')

    for line in infile:
        line = line.split(',')
        MU = Matchup(
            week=line[0],
            league=_league,
            team_one=list_of_teams[int(line[1])-1],
            team_one_points=0,
            team_two=list_of_teams[int(line[2])-1],
            team_two_points=0,
            winner = None
        )
        MU.save()

def create_matchup_data():  #no args lol
    all_leagues = []
    league_qs = League.objects.all()
    for league in league_qs:
        if league.is_valid_league():
            all_leagues.append(league)
        else:
            #disable league
            pass

    for league in all_leagues:
        team_list = Team.objects.filter(league=league)
        count = team_list.count()
        shuffled_team_list = [0] * count
        seed = random.sample(range(1, count+1),count)
        for idx, team in enumerate(team_list):
            shuffled_team_list.remove(0)
            shuffled_team_list.insert(seed[idx],team)

        create_matchup_schedule(shuffled_team_list, league)

    import menu
    menu.create_bye_weeks()


def calc_matchup_results(matchup, t1, t2):

    t1pts = t1.calc_week_points()
    t2pts = t2.calc_week_points()

    matchup.team_one_points = t1pts
    matchup.team_two_points = t2pts

    if t1pts > t2pts:
        matchup.winner = t1
        t1.win += 1
        t1.total_points += t1pts
        t1.total_points_against += t2pts
        t2.loss += 1
        t2.total_points += t2pts
        t2.total_points_against += t1pts
    elif t2pts > t1pts:
        matchup.winner = t2
        t2.win += 1
        t2.total_points += t2pts
        t2.total_points_against += t1pts
        t1.loss += 1
        t1.total_points += t1pts
        t1.total_points_against += t2pts
    else:
        week=Curweek.objects.get(pk=1).curweek
        try:
            t1qb = Roster.objects.get(week=week, team=t1, player__pos='QB1')
            t1qb = Stats.objects.get(player=t1qb.player, week=week).pasyds
        except Exception:
            t1qb = 0
        try:
            t2qb = Roster.objects.get(week=week, team=t2, player__pos='QB1')
            t2qb = Stats.objects.get(player=t2qb.player, week=week).pasyds
        except Exception:
            t2qb = 1

        if int(t1qb) > int(t2qb):
            matchup.winner = t1
            t1.win += 1
            t1.total_points += t1pts
            t1.total_points_against += t2pts
            t2.loss += 1
            t2.total_points += t2pts
            t2.total_points_against += t1pts
        else:
            matchup.winner = t2
            t2.win += 1
            t2.total_points += t2pts
            t2.total_points_against += t1pts
            t1.loss += 1
            t1.total_points += t1pts
            t1.total_points_against += t2pts

def process_weekly_matchups():
    week = Curweek.objects.get(pk=1)
    MU = Matchup.objects.filter(week=week.curweek)
    for matchup in MU:
        t1 = Team.objects.get(pk = matchup.team_one.id)
        t2 = Team.objects.get(pk = matchup.team_two.id)
        calc_matchup_results(matchup, t1, t2)
        copy_roster(t1)
        copy_roster(t2)
        t1.save()
        t2.save()
        matchup.save()

    increment_curweek()

def copy_roster(team):
    """ Copies roster from previous week
    """
    next_week = int(Curweek.objects.get(pk=1).curweek) + 1
    roster_to_copy = Roster.objects.filter(week = Curweek.objects.get(pk=1).curweek, team = team)
    for player in roster_to_copy:
        R = Roster(week = next_week, team = team, player = player.player)
        R.save()

def create_locks(pro_team_matchup):
    """ Creates 0'd out stat records once a player has started playing.
    """
    pro_team_matchup = Schedule.objects.get(pk = pro_team_matchup)
    players = Player.objects.filter(Q(pro_team = pro_team_matchup.home)|Q(pro_team = pro_team_matchup.away))
    for player in players:
        guid = int(str(pro_team_matchup.week) + '0' + str(random.randint(1, 9147483)))
        lock = Stats(player = player, week = pro_team_matchup.week, tm2 = 'INP', health = 'OK', guid = guid)
        lock.save()

def recalculate_weekly_matchups():
    week = Curweek.objects.get(pk=1)
    MU = Matchup.objects.filter(week = week.curweek)
    for matchup in MU:
        t1 = Team.objects.get(pk = matchup.team_one.id)
        t2 = Team.objects.get(pk = matchup.team_two.id)
        t1pts = t1.calc_week_points()
        t2pts = t2.calc_week_points()

        matchup.team_one_points = t1pts
        matchup.team_two_points = t2pts
        matchup.save()

def increment_curweek():
    week = Curweek.objects.get(pk=1)
    week.curweek += 1
    week.save()