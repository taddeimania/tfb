import os
from tfb.settings import PROJECT_ROOT
from tfb.players.models import Stats, Pro_Team, Schedule
from tfb.utility import logic
from tfb.utility.stat_mapper import MapPlayerStats
from tfb.stat_parse import parser

def clean(line):
    """Cleans up input data from TSB data files to prepare data
    """
    line = line.strip()
    line = line.replace('.', '', 1)
    line = line.split(',')
    return line

def insert_file(filename):
    """ Insert individual files into stats
    """
    filename = filename.replace("/", "")
    full_file_path = "{}/files/{}".format(PROJECT_ROOT, filename)
    week = logic.getweek()
    stat_obj = parser.parser(full_file_path)
    update(stat_obj['stats'], week)
    teamupdate(stat_obj['game_result'], week)

    os.remove(full_file_path)

def update(infile, week):
    """Updates player and week_X tables with data from individual game files.
    """
    week = str(week)

    for line in infile:
        line = clean(line)
        stats = MapPlayerStats(line)
        stats.get_player_by_stat_file_id()
        try:
            if stats.player_id:
                health_one_week_ago = "OK"
                health_two_weeks_ago = "OK"
                try:
                    Stats.objects.get(player=stats.player_id, week=week).delete()
                except Exception:
                    pass
                try:
                    health_one_week_ago = Stats.objects.get(player=stats.player_id, week=int(week)-1).health
                    if week != 2:
                        # this looks stupid but if a player gets injured and goes on a bye week and
                        # doesn't come back, he is then marked as OK...  he should still be injured.
                        health_two_weeks_ago = Stats.objects.get(player=stats.player_id, week=int(week)-2).health
                except Exception:
                    pass
                stats.forgive_negative()
                stat = stats.create_stat_object(week)
                if health_one_week_ago != 'OK' and stat.fanpts == 0 and health_two_weeks_ago != 'OK':
                    stat.health = 'INJURED'
                stat.save()
        except TypeError:
            continue

def teamupdate(result, week):
    week = str(week)
    tmid1 = result[0][0]
    tm1score = result[0][1]
    tmid2 = result[1][0]
    tm2score = result[1][1]
    tmid1 = tmid1.replace('.','')
    tmid2 = tmid2.replace('.','')

    pt1 = Pro_Team.objects.get(short=tmid1)
    pt2 = Pro_Team.objects.get(short=tmid2)
    if int(tm1score) > int(tm2score):		#tm1 wins
        pt1.wins += 1
        pt2.loss += 1

    elif int(tm1score) == int(tm2score):	#TIE
        pt1.tie += 1
        pt2.tie += 1
    else:
        pt1.loss += 1
        pt2.wins += 1

    print pt1.short, pt2.short, week
    schedule = Schedule.objects.get(home=pt1.short, away=pt2.short, week=week)
    schedule.homescore = tm1score
    schedule.awayscore = tm2score

    pt1.save()
    pt2.save()
    schedule.save()