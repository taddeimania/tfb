from positions import QuarterBack, RunningBack, WideReceiver, TightEnd, Kicker, BasePosition

def get_home_and_away(hexfile):
    away = ""
    home = ""
    for x in range(3087, 3090):
        home += hexfile[x]

    for x in range(3119, 3122):
        away += hexfile[x]

    return [home, away]

def get_results(hexfile):
    home = hexfile[977]
    away = hexfile[982]
    return (BasePosition.team_list[0], str(hex(ord(home)))[2:]), (BasePosition.team_list[1], str(hex(ord(away)))[2:])

def set_stats(hexfile):
    game = get_home_and_away(hexfile)
    stat_list = []
    home_side = True
    for side in game:
        for i in range(1, 3):
            qb1 = QuarterBack(hexfile, i, team=side, home=home_side)
            stat_list.append(qb1.get_stats())
        for i in range(1, 5):
            rb = RunningBack(hexfile, i, team=side, home=home_side)
            stat_list.append(rb.get_stats())
        for i in range(1, 5):
            wr = WideReceiver(hexfile, i, team=side, home=home_side)
            stat_list.append(wr.get_stats())
        for i in range(1, 3):
            te = TightEnd(hexfile, i, team=side, home=home_side)
            stat_list.append(te.get_stats())

        k = Kicker(hexfile, team=side, home=home_side)
        stat_list.append(k.get_stats())


        home_side = False

    return stat_list

def parser(infile):
    file = open(infile, "rb")
    hexfile = file.read()
    BasePosition.team_list = get_home_and_away(hexfile)
    BasePosition.get_injuries(hexfile)
    BasePosition.get_conditions(hexfile)
    stat_list = set_stats(hexfile)
    game_result = get_results(hexfile)
    return {'stats': stat_list, 'game_result': game_result}

if __name__ == "__main__":
    main()