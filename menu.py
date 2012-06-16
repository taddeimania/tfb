# 		Tecmo Fantasy Bowl
# 		by: Joel Taddei, 2011
# 		Menu & Misc Utility Functions
#
import load_stats
import os
import random
import logic
from myproject.settings import PROJECT_ROOT
from players.models import Player, Curweek, Stats, Pro_Team

path = PROJECT_ROOT + "/files/"

def clean(line):
    """Cleans up input data from TSB data files to prepare data
    """

    line = line.strip()
    line = line.replace(' ', '', 1)
    line = line.replace('.', '', 1)
    line = line.replace('"', '\'')
    line = line.replace('[', '')
    line = line.replace(']', '')
    line = line.split(',')
    return line

def insert_file(file):
    """ Insert individual files into stats
    """
    file = file.replace("/", "")
    file1 = (path + file)
    week = logic.getweek()
    if "player.txt" in file:
        load_stats.update(file1, week)
    elif "team.txt" in file:
        load_stats.teamupdate(file1, week)

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
