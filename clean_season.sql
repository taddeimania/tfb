use jtaddei_tecmo;
update players_curweek set curweek = 1;
truncate players_matchup;
truncate players_player;
update players_pro_team set bye = 0, wins = 0, loss = 0, tie = 0;
truncate players_roster;
truncate players_schedule;
truncate players_stats;
update players_team set win = 0, loss = 0, total_points = 0, total_points_against = 0;
truncate players_transaction;