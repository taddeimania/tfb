# 		Tecmo Fantasy Bowl
# 		by: Joel Taddei, 2011
# 		TSB Datafile input & SQL Statement Output functions
#		   this is the raw backend i wrote first

import menu
import random
from myproject.settings import PROJECT_ROOT
from players.models import Stats, Player, Pro_Team, Schedule

def scan_player (posid):
    """Reads each line of the player roster CSV file.
     Data stream input format:
         1000,'QB1','First Last',0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,'BUF','OPP','OK',0

     Returns a PlayerID when PosID is found by concatenating BUF & QB1.

     In this case the function would return: BUFQB1 & 1000.
     """

    infile = open(PROJECT_ROOT + '/players.csv', 'r')

    for line in infile:
        line = line.strip()
        line = line.replace(' ', '')
        line = line.split(',')
        team = line[3].strip()
        posid = posid.replace('.','')
        formatline = team + line[1]
        formatline = formatline.replace("'", "")
        if formatline == posid:
            return posid, line[0]

    infile.close()

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
        posid = line[0]
        pid1 = scan_player(posid)
        try:
            if pid1[0] == line[0]:
                healthINJ = str(line[-1])
                try:
                    # if a lock exists on a player prior to processing, lets delete it
                    # this will occur if we did a real time broadcast of a game
                    # and generated a lock
                    Stats.objects.get(player=pid1[1], week=week).delete()
                except Exception:
                    pass
                try:
                    healthINJ = Stats.objects.get(player=pid1[1], week=(int(week)-1)).health
                except Exception:
                    pass
                bonus = 0
                if int(line[6]) > 299:
                    bonus += 3
                elif int(line[8]) > 99:
                    bonus += 3
                elif int(line[17]) > 99:
                    bonus += 3
                tm2 = str(line[-2])
                health = str(line[-1])
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
                stat = Stats(player = Player.objects.get(pk=pid1[1]), week = week,
                 pa = line[3], pc=line[2], pastd=line[4], intcp=line[5], pasyds=line[6], rec=line[7], recyds=line[8],
                 rectd=line[9],krtd=line[12], prtd=line[15], rusat=line[16], rusyds=line[17], rustd=line[18], xpm=line[24],
                 fgm=line[25],tm2 = tm2, health = health, guid = guid)
                stat.fanpts = (int(line[4])*6) - (int(line[5])*2) + (int(line[6])/20) + (int(line[8])/10) + \
                              (int(line[9])*6) + (int(line[12])*6) + (int(line[15])*6) + (int(line[17])/10) + \
                              (int(line[18])*6) + int(line[24]) + (int(line[25])*3) + bonus
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