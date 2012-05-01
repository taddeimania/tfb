class MockPlayer:
    def __init__(self, player, stats=None):
        self.name = player.player
        self.id = player.id
        self.pos = player.pos
        if stats:
            self.pasyds = stats.pasyds
            self.pastd = stats.pastd
            self.intcp = stats.intcp
            self.recyds = stats.recyds
            self.rectd = stats.rectd
            self.rusyds = stats.rusyds
            self.rustd = stats.rustd
            self.xpm = stats.xpm
            self.fgm = stats.fgm
            self.fanpts = stats.fanpts
            self.health = stats.health
