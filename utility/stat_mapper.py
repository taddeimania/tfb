import random
from players.models import Player, Stats

class MapPlayerStats(object):

    def __init__(self, line):
        self.posid = line[0]
        self.healthINJ = str(line[-1])
        self.condition = str(line[-3])
        self.tm2 = str(line[-2]).replace('.','')
        self.pa = line[1]
        self.pc = line[2]
        self.pastd = line[3]
        self.intcp = line[4]
        self.pasyds = line[5]
        self.rec = line[6]
        self.recyds = line[7]
        self.rectd = line[8]
        self.rusat = line[9]
        self.rusyds = line[10]
        self.rustd = line[11]
        self.krtd = line[14]
        self.prtd = line[17]
        self.xpa = line[18]
        self.xpm = line[19]
        self.fga = line[20]
        self.fgm = line[21]

    def calc_fan_pts(self, bonus):
        return (int(self.pastd) * 6) - (int(self.intcp) * 2) + (int(self.pasyds) / 20) + (int(self.recyds) / 10) +\
               (int(self.rectd) * 6) + (int(self.krtd) * 6) + (int(self.prtd) * 6) + (int(self.rusyds) / 10) +\
               (int(self.rustd) * 6) + int(self.xpm) + (int(self.fgm) * 3) + bonus

    def forgive_negative(self):
        if int(self.recyds) < 0:
            self.recyds = 0
        if int(self.rusyds) < 0:
            self.rusyds = 0
        if int(self.pasyds) < 0:
            self.pasyds = 0

    def calculate_bonuses(self):
        bonus = 0
        if int(self.pasyds) > 299:
            bonus += 3
        if int(self.recyds) > 99:
            bonus += 3
        if int(self.rusyds) > 99:
            bonus += 3
        return bonus

    def get_player_by_stat_file_id(self):

        posid_ = self.posid[-1]
        if posid_ != 'K':
            if len(self.posid) == 6:
                pos = self.posid[3:]
            else:
                pos = self.posid[2:]
        elif posid_ == 'P':
            return [None, None]
        else:
            pos = 'K'

        team = self.posid.replace(pos, '')

        try:
            player = Player.objects.get(pro_team=team, pos=pos)
            self.player_id = player.id
        except Exception:
            self.player_id = None

    @staticmethod
    def construct_guid(week):
        return int(week + '0' + str(random.randint(1, 2147486)))

    def create_stat_object(self, week):
        return Stats(
            player=Player.objects.get(pk=self.player_id),
            week=week,
            pa=self.pa,
            pc=self.pc,
            pastd=self.pastd,
            intcp=self.intcp,
            pasyds=self.pasyds,
            rec=self.rec,
            recyds=self.recyds,
            rectd=self.rectd,
            rusat=self.rusat,
            rusyds=self.rusyds,
            rustd=self.rustd,
            krtd=self.krtd,
            prtd=self.prtd,
            xpm=self.xpm,
            fgm=self.fgm,
            tm2=self.tm2,
            health=self.healthINJ,
            guid=self.construct_guid(week),
            fanpts=self.calc_fan_pts(self.calculate_bonuses()),
            condition=self.condition,
        )