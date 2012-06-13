# 		Tecmo Fantasy Bowl
# 		by: Joel Taddei, 2011
# 		Menu & Misc Utility Functions
#
import format
import os
import random
from myproject.settings import PROJECT_ROOT
from players.models import Player, Curweek, Stats, Pro_Team

path = PROJECT_ROOT + "/files/"

def clean(line):
    """Cleans up input data from TSB data files to prepare data
         to be inserted via SQL."""

    line = line.strip()
    line = line.replace(' ', '', 1)
    line = line.replace('.', '', 1)
    line = line.replace('"', '\'')
    line = line.replace('[', '')
    line = line.replace(']', '')
    line = line.split(',')
    return line

# I SEE DEAD CODE
#def refresh_player_schedule():
#    """Creates the player table with empty values"""
#    #TODO:
#
#    #cursor.execute("DROP TABLE IF EXISTS players_schedule")
#    #cursor.execute("""CREATE TABLE `players_schedule` (`id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY, `away` varchar(3) NOT NULL,`home` varchar(3) NOT NULL,`week` integer NOT NULL)""")
#    infile = open('c:/schedule.txt', 'r')
#    counter = 1
#    for line in infile:
#        line = line.replace('\n', '')
#        line = line.split(',')
#
#        sql = "INSERT INTO players_schedule (id, away, awayscore, home, homescore, week) VALUES (" + str(counter) + ",'" + line[0] + "', 0, '" + line[1] + "', 0, " + line[2] + ")"
#        counter += 1
#    #sqlcurweek = "INSERT INTO players_curweek (id, curweek) VALUES (1, 0)"
#
#
#def refreshteams():
#    # """Drop individual table manually.  Primarily for admin tasks."""
#    #TODO:
#    infile = open('c:/nes/teampos.csv', 'r')
#    for line in infile:
#        line = line.replace('\n', '')
#        line = line.split(',')
#        sql = "INSERT INTO players_pro_team VALUES (" + line[0] + "," + line[1] + "," + line[2] + ",0,0,0)"
#
#def populate_player_table():
#
#    infile = open(PROJECT_ROOT + '/roster.csv', 'r')
#    counter = 1000
#    for line in infile:
#        # Insert each player into players table with default values from roster.csv
#        counter = str(counter)
#        line = line.strip()
#        line = line.split(',')
#        player = Player(id = counter, pos = line[0], name = line[1], pro_team = line[-5], picture = line[-1])
#        #player.save()
#        counter = int(counter)
#        counter += 1
#    infile.close()

def insert_file(file):
    """ Insert individual files into stats
    """
    file = file.replace("/", "")
    file1 = (path + file)
    week = Curweek.objects.get(pk=1).curweek
    if "player.txt" in file:
        format.update(file1, week)
    elif "team.txt" in file:
        format.teamupdate(file1, week)

    os.remove(file1)

#only needed for new pro league creation, after players objects are created
# THIS IS SUPER IMPORTANT FOR PLAYER CARDS TO DISPLAY CORRECTLY!!!!
def create_bye_weeks():
    teams = Pro_Team.objects.filter(bye__gt=0)
    for team in teams:
        players = Player.objects.filter(pro_team=team)
        for player in players:
            guid = int(str(team.bye) + '0' + str(random.randint(1, 9147483)))
            byeweek = Stats(player=player, week=player.pro_team.bye, tm2='BYE', health='BYE', guid=guid)
            byeweek.save()
