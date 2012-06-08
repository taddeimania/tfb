TEAM_LIST = ['BUF', 'MIA', 'NE', 'NYJ', 'CIN', 'CLE', 'BAL', 'PIT', 'IND', 'HOU', 'JAX', 'TEN',
             'DEN', 'KC', 'OAK', 'SD', 'WAS', 'NYG', 'PHI', 'DAL', 'CHI', 'DET', 'GB', 'MIN',
             'TB', 'NO', 'ATL', 'CAR', 'SF', 'STL', 'SEA', 'ARZ']
TEAM_DICT = {
	'bills': ('BUF', 'Buffalo Bills'),
	'dolphins': ('MIA', 'Miami Dolphins'),
	'patriots': ('NE', 'New England Patriots'),
	'jets': ('NYJ', 'New York Jets'),
	'bengals': ('CIN', 'Cininatti Bengals'),
	'browns': ('CLE', 'Cleveland Browns'),
	'ravens': ('BAL', 'Baltimore Ravens'),
	'steelers': ('PIT', 'Pittsburgh Steelers'),
	'colts': ('IND', 'Indianapolis Colts'),
	'texans': ('HOU', 'Houston Texans'),
	'jaguars': ('JAX', 'Jacksonville Jaguars'),
	'titans': ('TEN', 'Tennessee Titans'),
	'broncos': ('DEN', 'Denver Broncos'),
	'chiefs': ('KC', 'Kansas City Chiefs'),
	'raiders': ('OAK', 'Oakland Raiders'),
	'chargers': ('SD', 'San Diego Chargers'),
	'redskins': ('WAS', 'Washington Redskins'),
	'giants': ('NYG', 'New York Giants'),
	'eagles': ('PHI', 'Philidelphia Eagles'),
	'cowboys': ('DAL', 'Dallas Cowboys'),
	'bears': ('CHI', 'Chicago Bears'),
	'lions': ('DET', 'Detroit Lions'),
	'packers': ('GB', 'Green Bay Packers'),
	'vikings': ('MIN', 'Minnesota Vikings'),
	'buccaneers': ('TB', 'Tampa Bay Buccaneers'),
	'saints': ('NO', 'New Orleans Saints'),
	'falcons': ('ATL', 'Atlanta Falcons'),
	'panthers': ('CAR', 'Carolina Panthers'),
	'49ers': ('SF', 'San Francisco 49ers'),
	'rams': ('STL', 'St. Louis Rams'),
	'seahawks': ('SEA', 'Seattle Seahawks'),
	'cardinals': ('ARZ', 'Arizona Cardinals'),
}

KEYWORDS = ['QB1', 'QB2', 'RB1', 'RB2', 'RB3', 'RB4', 'WR1', 'WR2', 'WR3', 'WR4', 'TE1', 'TE2', 'K']

schedule = [
    [1, []], [2, []], [3, []], [4, []], [5, []], [6, []], [7, []], [8, []], [9, []], [10, []], [11, []], [12, []],
    [13, []], [14, []], [15, []], [16, []], [17, []],
]

def to_sql(team, pos, name, face, counter):

    name = name.strip()
    name = name.title()
    face = face.split('Face=0x')[1]
    sql = "INSERT INTO players_player VALUES ({0}, '{1}', '{2}', '{3}', '{4}');\n".format(counter, pos, name, team, face)
    player_file = "{0}, {1}, {2}, {3}\n".format(counter, pos, name, team)
    return sql, player_file

def main():

    read_file = open('tsb_raw.txt', 'r')
    schedule_read_file = open('schedule.txt', 'r')
    write_file = open('tsb_in.sql', 'a')
    player_write_file = open('players.csv', 'a')
    schedule_write_file = open('schedule.sql', 'a')
    out_team = ''
    week = 1
    counter = 1000

    for line in read_file:
        pass
        if 'TEAM' in line:
            team_line = line.split('=')
            team = str(team_line[1])
            out_team = str(team.split('S')[0]).strip()
            continue
        out_line = line.split(',')
        if out_line[0] in KEYWORDS:
            player_out, player_file = to_sql(TEAM_DICT[out_team][0], out_line[0], out_line[1], out_line[2], counter)
            write_file.write(player_out)
            player_write_file.write(player_file)
            counter += 1

    for line in schedule_read_file:
        if "WEEK" in line:
            week = line.split()[1]
        elif line.strip():
            out_line = line.split(' at ')
            away = TEAM_DICT[out_line[0]][0]
            home = TEAM_DICT[out_line[1].strip()][0]
            schedule[int(week)-1][1].append(away)
            schedule[int(week)-1][1].append(home)

            sql = "INSERT INTO players_schedule VALUES ('{0}', 0, '{1}', 0, {2});\n".format(
                away,
                home,
                week
            )
            schedule_write_file.write(sql)
    for week in schedule:
        for team in TEAM_LIST:
            if team not in week[1]:
                sql = "UPDATE players_pro_team SET bye = {0} where short = '{1}';\n".format(week[0], team)
                schedule_write_file.write(sql)

if __name__ == "__main__":
    main()
