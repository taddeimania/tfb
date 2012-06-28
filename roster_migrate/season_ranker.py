import MySQLdb

def calc_points(line):
	for idx, stat in enumerate(line):
		if not stat:
			line[idx] = 0

	return (int(line[5]) * 6) - (int(line[6]) * 2) + (int(line[7]) / 20) + (int(line[13]) / 10) +\
		       (int(line[12]) * 6) + (int(line[16]) * 6) + (int(line[19]) * 6) + (int(line[9]) / 10) +\
		       (int(line[10]) * 6) + int(line[26]) + (int(line[28]) * 3)

def main():
	read_file = open('reformatted.csv', 'r')
	write_file = open('player_ranking.sql', 'a')
	player_list = []
	i = 1000

	for line in read_file:
		line = line.split(',')
		if line[0] in ["QB1", "QB2", "RB1", "RB2", "RB3", "RB4", "WR1", "WR2", "WR3", "WR4", "TE1", "TE2", "K"]:			
			name = i
			points = calc_points(line)
			player_list.append((points, name))
			i += 1

	player_list.sort(reverse=True)
	write_file.write("use jtaddei_tecmo;\n")
	for idx, player in enumerate(player_list):
		write_file.write("INSERT INTO players_seasonranking values (null, {}, {});\n".format(idx+1, player[1]))


if __name__ == "__main__":
    main()
