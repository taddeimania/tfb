import os
from myproject.settings import PROJECT_ROOT
from myproject.players.models import Stats, Pro_Team, Schedule
from myproject.utility import logic
from myproject.utility.stat_mapper import MapPlayerStats

def clean(line):
    """Cleans up input data from TSB data files to prepare data
    """
    line = line.strip()
    line = line.replace('.', '', 1)
    line = line.split(',')
    return line

def insert_file(file):
    """ Insert individual files into stats
    """
    filename = file.replace("/", "")
    full_file_path = "{}/files/{}".format(PROJECT_ROOT, filename)
    week = logic.getweek()
    if "player.txt" in file:
        update(full_file_path, week)
    else:
        teamupdate(full_file_path, week)

    os.remove(full_file_path)

def update(filename, week):
    """Updates player and week_X tables with data from individual game files.
    """
    infile = open(filename)
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
    infile.close()

def teamupdate(a, week):
    index = 1
    tmid1 = ""
    tmid2 = ""
    tm1score = 0
    tm2score = 0
    infile = open(a)
    week = str(week)
    for line in infile:
        newline = line.split(',')
        if index == 1:
            tmid1 = newline[0]
            tm1score = newline[-7]
        else:
            tmid2 = newline[0]
            tm2score = newline[-7]
        tmid1 = tmid1.replace('.','')
        tmid2 = tmid2.replace('.','')
        index += 1

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
    schedule = Schedule.objects.get(away=pt1.short, home=pt2.short, week=week)
    schedule.awayscore = tm1score
    schedule.homescore = tm2score

    pt1.save()
    pt2.save()
    schedule.save()
    infile.close()