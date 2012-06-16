import menu
import random
from players.models import Stats, Player, Pro_Team, Schedule

def scan_player (posid):

    if posid[-1] != 'K':
        if len(posid) == 6:
            pos = posid[3:]
        else:
            pos = posid[2:]
    elif posid[:-1] == 'P':
        return [None, None]
    else:
        pos = 'K'

    team = posid.replace(pos, '')

    try:
        player = Player.objects.get(pro_team=team, pos=pos)
        return player.id
    except Exception:
        return [None, None]


def calculate_bonuses(bonus, line):
    if int(line[6]) > 299:
        bonus += 3
    if int(line[8]) > 99:
        bonus += 3
    if int(line[17]) > 99:
        bonus += 3
    return bonus


def calc_fan_pts(bonus, line):
    return (int(line[4]) * 6) - (int(line[5]) * 2) + (int(line[6]) / 20) + (int(line[8]) / 10) +\
                  (int(line[9]) * 6) + (int(line[12]) * 6) + (int(line[15]) * 6) + (int(line[17]) / 10) +\
                  (int(line[18]) * 6) + int(line[24]) + (int(line[25]) * 3) + bonus


def map_line_to_stats(line):
    stats = {
        'posid': line[0],
        'healthINJ': str(line[-1]),
        'tm2': str(line[-2]),
    }
    return stats

def update(filename, week):
    """Updates player and week_X tables with data from individual game files.
     Input stream format:
         DENQB1,0,21,6,0,2,154,0,0,0,0,0,0,0,0,0,5,30,0,0,0,0,0,0,0,0,0,0,0,0,DEN,JAX,OK

     Function calls the scan2(posid) method in order to obtain the players PlayerID number.
     Django api is called to add the weekly stat information as well as
     the week_X stat information.

     Fantasy points are then calculated and updated into the players and week_X tables.
     """
    infile = open(filename)
    week = str(week)

    for line in infile:
        line = menu.clean(line)
        stats = map_line_to_stats(line)
        pid1 = scan_player(stats['posid'])
        try:
            if pid1:
                healthINJ = stats['healthINJ']
                try:
                    Stats.objects.get(player=pid1, week=week).delete()
                except Exception:
                    pass
                try:
                    healthINJ = Stats.objects.get(player=pid1, week=(int(week)-1)).health
                except Exception:
                    pass
                bonus = 0
                bonus = calculate_bonuses(bonus, line)
                tm2 = stats['tm2']
                health = stats['healthINJ']
                guid = random.randint(1, 2147486)
                guid = week + '0' + str(guid)
                guid = int(guid)
                tm2 = str(tm2).replace('.','')
                if int(line[8]) < 0:
                    line[8] = 0
                if int(line[17]) < 0:
                    line[17] = 0
                if int(line[6]) < 0:
                    line[6] = 0
                stat = Stats(
                    player=Player.objects.get(pk=pid1),
                    week = week,
                    pa = line[3],
                    pc=line[2],
                    pastd=line[4],
                    intcp=line[5],
                    pasyds=line[6],
                    rec=line[7],
                    recyds=line[8],
                    rectd=line[9],
                    krtd=line[12],
                    prtd=line[15], 
                    rusat=line[16],
                    rusyds=line[17],
                    rustd=line[18],
                    xpm=line[24],
                    fgm=line[25],
                    tm2=tm2,
                    health=health,
                    guid=guid)

                stat.fanpts = calc_fan_pts(bonus, line)
                if healthINJ != 'OK' and stat.fanpts == 0:
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