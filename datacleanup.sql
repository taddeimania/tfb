TRUNCATE players_matchup;
UPDATE players_pro_team SET wins = 0, loss = 0, tie = 0;
TRUNCATE players_roster
UPDATE players_schedule SET awayscore = 0, homescore = 0;
TRUNCATE players_stats;
UPDATE players_team SET win = 0, loss = 0, total_points = 0, total_points_against = 0;
TRUNCATE players_transaction;
