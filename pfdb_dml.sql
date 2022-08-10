-- get all Team IDs, city names, team names, and conferences
SELECT team_id, team_city, team_name, conference FROM Teams;

-- get all player IDs, player first names, player last names, team names, and positions
SELECT Players.player_id, Players.fname, Players.lname, Teams.team_name, Players.primary_position
FROM Players
INNER JOIN Teams ON Players.team_id = Teams.team_id;

-- get all game IDs, home team names, away team names, home team scores, away team scores, dates, and season years
SELECT Games.game_id, Teams.team_name, Teams.team_name, Games.home_score, Games.away_score, Games.date, Games.season_year
FROM Games
INNER JOIN Teams ON Games.home_team_id = Teams.team_id
INNER JOIN Teams ON Games.away_team_id = Teams.team_id;

-- get all player stats IDs, player first names, player last names, game IDs, passing yards, passing TDs, rushing yards, rushing TDs, receiving yards, and receiving TDs
SELECT Players_Games_Stats.player_stats_id, CONCAT(Players.fname, ' ', Players.lname) AS name, Players_Games_Stats.game_id, Players_Games_Stats.passing_yard_total, Players_Games_Stats.passing_td_total,
Players_Games_Stats.rushing_yard_total, Players_Games_Stats.rushing_td_total, Players_Games_Stats.receiving_yard_total, Players_Games_Stats.receiving_td_total
FROM Players_Games_Stats
INNER JOIN Players ON Players_Games_Stats.player_id = Players.player_id;

-- get all season years, super bowl champ team names, and super bowl runner-up team names
SELECT Seasons.season_year, Teams.team_id, t1.team_id
FROM Seasons
INNER JOIN Teams ON Seasons.super_bowl_champ = Teams.team_id
INNER JOIN Teams t1 ON Seasons.super_bowl_runner_up = t1.team_id;

-- get a single player's data for update player form
SELECT Players.player_id, Players.fname, Players.lname, Teams.team_name
FROM Players
INNER JOIN Teams on Players.team_id = Teams.team_id
WHERE Players.player_id = :player_id_selected_from_players_page;

-- get a single team's data for update team form
SELECT team_id, team_city, team_name, conference
FROM Teams
WHERE team_id = :team_id_selected_from_teams_page;

-- get a single game's data for update game form
SELECT Games.game_id, Teams.team_id, Teams.team_id, Games.home_score, Games.away_score, Games.date, Games.season_year
FROM Games
INNER JOIN Teams ON Games.home_team_id = Teams.team_id
INNER JOIN Teams t1 ON Games.away_team_id = t1.team_id
WHERE Games.game_id = :game_id_selected_from_games_page;

-- get a single player game stats entry for update player_game page
SELECT Players_Games_Stats.player_stats_id, CONCAT(Players.fname, ' ', Players.lname) AS name, Players_Games_Stats.game_id, Players_Games_Stats.passing_yard_total, Players_Games_Stats.passing_td_total,
Players_Games_Stats.rushing_yard_total, Players_Games_Stats.rushing_td_total, Players_Games_Stats.receiving_yard_total, Players_Games_Stats.receiving_td_total
FROM Players_Games_Stats
INNER JOIN Players ON Players_Games_Stats.player_id = Players.player_id
WHERE Players_Games_Stats.player_stats_id = :player_stats_id_selected_from_player_game_page;

-- get a single season year for update seasons page
SELECT Seasons.season_year, Teams.team_id, t1.team_id
FROM Seasons
INNER JOIN Teams ON Seasons.super_bowl_champ = Teams.team_id
INNER JOIN Teams t1 ON Seasons.super_bowl_runner_up = t1.team_id
WHERE Seasons.season_year = :season_year_selected_from_seasons_page;

-- get team IDs and team names to populate drop down list for associating a team with a player
SELECT team_id, team_name
FROM Teams;

-- get team IDs and team names to populate drop down lists for associating a team with a game
SELECT team_id, team_name
FROM Teams;

-- get player IDs and player names to populate drop down list for associating player game stats with player
SELECT player_id, CONCAT(fname, ' ', lname) AS name
FROM Players;

-- get game IDs to populate drop down list for associating player game stats with games
SELECT game_id
FROM Games;

-- get team names and team IDs to populate drop down lists for associating teams with seasons as super bowl champs and super bowl runners-up
SELECT team_id, team_name
FROM Teams;

-- add a new team
INSERT INTO Teams 
(
    team_city,
    team_name,
    conference
)
VALUES
(
    :team_cityInput,
    :team_nameInput,
    :conferenceInput
);

-- add new game
INSERT INTO Games
(
    home_team_id,
    away_team_id,
    home_score,
    away_score,
    date,
    season_year
)
VALUES
(
    :home_team_id_from_dropdown_Input,
    :away_team_id_from_dropdown_Input,
    :home_scoreInput,
    :away_scoreInput,
    :dateInput,
    :season_yearInput
);

-- add a new player
INSERT INTO Players
(
    fname,
    lname,
    team_id,
    primary_position
)
VALUES
(
    :fnameInput,
    :lnameInput,
    :team_id_from_dropdown_Input,
    :primary_positionInput
);

-- add new game player stats
INSERT INTO Players_Games_Stats
(
    player_id,
    game_id,
    passing_yard_total,
    passing_td_total,
    rushing_yard_total,
    rushing_td_total,
    receiving_yard_total,
    receiving_td_total
)
VALUES
(
    :player_id_from_dropdown_Input,
    :game_id_from_dropdown_Input,
    :passing_yard_totalInput,
    :passing_td_totalInput,
    :rushing_yard_totalInput,
    :rushing_td_totalInput,
    :receiving_yard_totalInput,
    :receiving_td_totalInput
);

-- Update team info from team edit page
UPDATE Teams SET team_city = :team_city_input, team_name= :team_name_input, conference = :conference_input 
    WHERE team_id = :team_id_selected_from_teams_page

-- Update game info from game edit page
UPDATE Games SET home_team_id = :home_team_id_input, away_team_id = :away_team_id_input, home_score = :home_score_input, away_score = :away_score_input, 
    date = :date_input, season_year = :season_year_input
    WHERE game_id = :game_id_selected_from_games_page;

-- Update player info from player edit page
UPDATE Players SET fname = :fname_input, lname = :lname_input, team_id = :team_id_from_input, primary_position = :primary_position_input
    WHERE player_id = :player_id_selected_from_players_page;

--Update player game stats info from player game stats edit page
UPDATE Players_Games_Stats SET player_id = :player_id_input, game_id = :game_id_input, passing_yard_total = :passing_yard_total_input, passing_td_total = :passing_td_total_input,
    rushing_yard_total = :rushing_yard_total_input, rushing_td_total = :rushing_td_total_input, receiving_yard_total = :receiving_yard_total_input, receiving_td_total, :receiving_td_total_input
    WHERE player_stats_id = :player_stats_id_selected_from_player_game_page;

--Update season info from seasons edit page
UPDATE Seasons SET super_bowl_champ = :super_bowl_champ_input, super_bowl_runner_up = :super_bowl_runner_up_input
    WHERE season_year = :season_year_selected_from_seasons_page;

-- Delete team from Teams page
DELETE FROM Teams WHERE team_id = :team_id_selected_from_teams_page;

-- Delete game from Games page
DELETE FROM Games WHERE game_id = :game_id_selected_from_games_page;

-- Delete player from Players page
DELETE FROM Players WHERE player_id = :player_id_selected_from_players_page;

-- Delete player game stats from Players Games Stats page
DELETE FROM Players_Games_Stats WHERE player_stats_id = :player_stats_id_selected_from_player_game_page;

-- Delete season from Seasons page
DELETE FROM Seasons WHERE season_year = :season_year_selected_from_seasons_page;
