# Sample Flask application for a Pro Football database, snapshot of Teams

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os


app = Flask(__name__)

# database connection
# Template:
# app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
# app.config["MYSQL_USER"] = "cs340_OSUusername"
# app.config["MYSQL_PASSWORD"] = "XXXX" | last 4 digits of OSU id
# app.config["MYSQL_DB"] = "cs340_OSUusername"
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# database connection info
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_fifieldb"
app.config["MYSQL_PASSWORD"] = "6876"
app.config["MYSQL_DB"] = "cs340_fifieldb"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Routes
# have homepage route to /people by default for convenience, generally this will be your home route with its own template
@app.route("/")
def home():
    return render_template("index.html")

# route for teams page
@app.route("/teams", methods=["POST", "GET"])
def teams():
    # Separate out the request methods, in this case this is for a POST
    # insert a team into the Teams entity
    if request.method == "POST":
        # fire off if user presses the Add Team button
        if request.form.get("Add_Team"):
            # grab user form inputs
            team_city = request.form["team_city"]
            team_name = request.form["team_name"]
            conference = request.form["conference"]

            query = "INSERT INTO Teams (team_city, team_name, conference) VALUES (%s, %s,%s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (team_city, team_name, conference))
            mysql.connection.commit()

            # redirect back to teams page
            return redirect("/teams")

    # Grab Teams data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in Teams
        query = "SELECT team_id, team_city, team_name, conference FROM Teams ORDER BY team_city ASC"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # render edit_teams page passing our query data and homeworld data to the edit_team template
        return render_template("teams.j2", data=data)


# route for delete functionality, deleting a person from Teams,
# we want to pass the 'team_id' value of that person on button click (see HTML) via the route
@app.route("/delete_team/<int:id>")
def delete_team(id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Teams WHERE team_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to people page
    return redirect("/teams")


# route for edit functionality, updating the attributes of a person in Teams
# similar to our delete route, we want to the pass the 'team_id' value of that taem on button click (see HTML) via the route
@app.route("/edit_team/<int:id>", methods=["POST", "GET"])
def edit_team(id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT team_id, team_city, team_name, conference FROM Teams WHERE team_id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()


        # render edit_team page passing our query data to the edit_people template
        return render_template("edit_team.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Team' button
        id = request.form["team_id"]
        team_city = request.form["team_city"]
        team_name = request.form["team_name"]
        conference = request.form["conference"]

        query = "UPDATE Teams SET Teams.team_city = %s, Teams.team_name = %s, Teams.conference = %s WHERE Teams.team_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (team_city, team_name, conference, id))
        mysql.connection.commit()

        # redirect back to teams page after we execute the update query
        return redirect("/teams")

@app.route("/games", methods=["POST", "GET"])
def games():
    # Separate out the request methods, in this case this is for a POST
    # insert a season into the Games entity
    if request.method == "POST":
        # fire off if user presses the Add Game button
        if request.form.get("Add_Game"):
            # grab user form inputs
            home_team_id = request.form["home_team_id"]
            away_team_id = request.form["away_team_id"]
            home_score = request.form["home_score"]
            away_score = request.form["away_score"]
            date = request.form["date"]
            season_year = request.form["season_year"]


            query = "INSERT INTO Games (home_team_id, away_team_id, home_score, away_score, date, season_year) VALUES (%s, %s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (home_team_id, away_team_id, home_score, away_score, date, season_year))
            mysql.connection.commit()

            # redirect back to teams page
            return redirect("/games")

    # Grab Seaons data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in Teams
        query = "SELECT Games.game_id, Teams.team_name AS home_team_id, t1.team_name AS away_team_id, Games.home_score, Games.away_score, Games.date, Games.season_year FROM Games INNER JOIN Teams ON home_team_id = Teams.team_id INNER JOIN Teams t1 ON away_team_id = t1.team_id INNER JOIN Seasons ON Games.season_year = Seasons.season_year ORDER BY date DESC"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT team_id, team_name FROM Teams ORDER BY team_name ASC"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        team_data = cur.fetchall()

        query3 = "SELECT season_year FROM Seasons ORDER BY season_year DESC"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        season_data = cur.fetchall()      

        # render edit_teams page passing our query data and homeworld data to the edit_team template
        return render_template("games.j2", data=data, teams=team_data, seasons=season_data)

@app.route("/delete_game/<int:id>")
def delete_game(id):
    # mySQL query to delete the game with our passed id
    query = "DELETE FROM Games WHERE game_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to games page
    return redirect("/games")

@app.route("/search_season_games/<int:id>", methods=["POST", "GET"])
def search_season_games(id):
    query = "SELECT Games.game_id, Teams.team_name AS home_team_id, t1.team_name AS away_team_id, Games.home_score, Games.away_score, Games.date, Games.season_year FROM Games INNER JOIN Teams ON home_team_id = Teams.team_id INNER JOIN Teams t1 ON away_team_id = t1.team_id INNER JOIN Seasons ON Games.season_year = Seasons.season_year WHERE Games.season_year = %s" % (id)
    cur = mysql.connection.cursor()
    cur.execute(query)
    data = cur.fetchall()

    return render_template("search_season_games.j2", data=data)

@app.route("/edit_game/<int:id>", methods=["POST", "GET"])
def edit_game(id):
    if request.method == "GET":
        # mySQL query to grab the info of the game with our passed id
        query = "SELECT Games.game_id, Teams.team_name AS home_team_id, t1.team_name AS away_team_id, Games.home_score, Games.away_score, Games.date, Games.season_year FROM Games INNER JOIN Teams ON home_team_id = Teams.team_id INNER JOIN Teams t1 ON away_team_id = t1.team_id INNER JOIN Seasons ON Games.season_year = Seasons.season_year WHERE Games.game_id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT team_id, team_name FROM Teams ORDER BY team_name ASC"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        team_data = cur.fetchall()

        query3 = "SELECT season_year FROM Seasons ORDER BY season_year DESC"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        season_data = cur.fetchall()   

        # render edit_team page passing our query data to the edit_game template
        return render_template("edit_game.j2", data=data, teams=team_data, seasons=season_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Game' button
        id = request.form["game_id"]         
        home_team_id = request.form["home_team_id"]
        away_team_id = request.form["away_team_id"]
        home_score = request.form["home_score"]
        away_score = request.form["away_score"]
        date = request.form["date"]
        season_year = request.form["season_year"]

        query = "UPDATE Games SET Games.home_team_id = %s, Games.away_team_id = %s, Games.home_score = %s, Games.away_score = %s, Games.date = %s, Games.season_year = %s WHERE Games.game_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (home_team_id, away_team_id, home_score, away_score, date, season_year, id))
        mysql.connection.commit()

    # redirect back to teams page after we execute the update query
        return redirect("/games")

# route for players page
@app.route("/players", methods=["POST", "GET"])
def players():
    # Separate out the request methods, in this case this is for a POST
    # insert a player into the Players entity
    if request.method == "POST":
        # fire off if user presses the Add Player button
        if request.form.get("Add_Player"):
            # grab user form inputs
            fname = request.form["fname"]
            lname = request.form["lname"]
            primary_position = request.form["primary_position"]
            team_id = request.form["team_id"]

            # account for null team
            if team_id == "0":
                query = "INSERT INTO Players (fname, lname, primary_position) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, primary_position))
                mysql.connection.commit()

            # no null inputs
            else:
                query = "INSERT INTO Players (fname, lname, team_id, primary_position) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (fname, lname, team_id, primary_position))
                mysql.connection.commit()

            # redirect back to players page
            return redirect("/players")

    # Grab Players data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the players in Players
        query = '''SELECT Players.player_id, Players.fname, Players.lname, Players.primary_position, Teams.team_name
        FROM Players LEFT JOIN Teams ON Players.team_id = Teams.team_id ORDER BY lname, fname ASC'''
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT team_id, team_name FROM Teams ORDER BY team_name ASC"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        team_data = cur.fetchall()

        # render edit_player page passing our query data and homeworld data to the edit_player template
        return render_template("players.j2", data=data, team_data=team_data)

# route for delete functionality, deleting a person from Players,
# we want to pass the 'player_id' value of that person on button click (see HTML) via the route
@app.route("/delete_player/<int:id>")
def delete_player(id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Players WHERE player_id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to players page
    return redirect("/players")


@app.route("/edit_player/<int:id>", methods=["POST", "GET"])
def edit_player(id):
    if request.method == "GET":
        # mySQL query to grab the info of the player with our passed id
        query = '''SELECT Players.player_id, Players.fname, Players.lname, Players.primary_position, Teams.team_name 
        FROM Players LEFT JOIN Teams ON Players.team_id = Teams.team_id WHERE player_id = %s''' % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # mySQL query to grab team id/name data for dropdown
        query2 = "SELECT team_id, team_name FROM Teams ORDER BY team_name ASC"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        team_data = cur.fetchall()


        # render edit_player page passing our query data to the edit_player template
        return render_template("edit_player.j2", data=data, team_data=team_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Player' button
        id = request.form["player_id"]
        fname = request.form["fname"]
        lname = request.form["lname"]
        primary_position = request.form["primary_position"]
        team_id = request.form["team_id"]

        if team_id == "0":
            query = "UPDATE Players SET Players.fname = %s, Players.lname = %s, Players.primary_position = %s, Players.team_id = NULL WHERE Players.player_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (fname, lname, primary_position, team_id, id))
            mysql.connection.commit()
        else:
            query = "UPDATE Players SET Players.fname = %s, Players.lname = %s, Players.primary_position = %s, Players.team_id = %s WHERE Players.player_id = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (fname, lname, primary_position, team_id, id))
            mysql.connection.commit()

        # redirect back to teams page after we execute the update query
        return redirect("/players")

    # route for player game stats page
@app.route("/player_game", methods=["POST", "GET"])
def players_games_stats():
    # Separate out the request methods, in this case this is for a POST
    # insert stats into the Players_Games_Stats entity
    if request.method == "POST":
        # fire off if user presses the Add Player Game button
        if request.form.get("Add_Player_Game"):
            # grab user form inputs
            player_id = request.form["player_id"]
            game_id = request.form["game_id"]
            passing_yard_total = request.form["passing_yard_total"]
            passing_td_total = request.form["passing_td_total"]
            rushing_yard_total = request.form["rushing_yard_total"]
            rushing_td_total = request.form["rushing_td_total"]
            receiving_yard_total = request.form["receiving_yard_total"]
            receiving_td_total = request.form["receiving_td_total"]

           
            query = '''INSERT INTO Players_Games_Stats (player_id, game_id, passing_yard_total, passing_td_total,
            rushing_yard_total, rushing_td_total, receiving_yard_total, receiving_td_total) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'''
            cur = mysql.connection.cursor()
            cur.execute(query, (player_id, game_id, passing_yard_total, passing_td_total,
            rushing_yard_total, rushing_td_total, receiving_yard_total, receiving_td_total))
            mysql.connection.commit()

            # redirect back to teams page
            return redirect("/player_game")

        # Grab Players_Games_Stats data so we send it to our template to display
    elif request.method == "GET":
        # mySQL query to grab all the data in Players_Games_Stats
        query = '''SELECT Players_Games_Stats.player_stats_id, CONCAT(Players.fname, ' ', Players.lname) AS name, Players_Games_Stats.game_id, Players_Games_Stats.passing_yard_total, Players_Games_Stats.passing_td_total, 
        Players_Games_Stats.rushing_yard_total, Players_Games_Stats.rushing_td_total, Players_Games_Stats.receiving_yard_total, Players_Games_Stats.receiving_td_total
        FROM Players_Games_Stats INNER JOIN Players ON Players_Games_Stats.player_id = Players.player_id ORDER BY Players_Games_Stats.player_stats_id ASC'''
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT player_id, CONCAT(fname, ' ', lname) AS name FROM Players ORDER BY lname, fname ASC"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        player_data = cur.fetchall()

        query3 = "SELECT game_id FROM Games"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        game_data = cur.fetchall()

        # render edit_player_games_stats page passing our query data and dropdown list data to the edit_player template
        return render_template("player_game.j2", data=data, player_data=player_data, game_data=game_data)

@app.route("/delete_player_game/<int:id>")
def delete_player_game(id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Players_Games_Stats WHERE player_stats_id = '%s'"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to seasons page
    return redirect("/player_game")

@app.route("/edit_player_game/<int:id>", methods=["POST", "GET"])
def edit_player_game(id):
    if request.method == "GET":
        # mySQL query to grab the info of the player game with our passed id
        query = '''SELECT Players_Games_Stats.player_stats_id, Players.player_id, Players_Games_Stats.game_id, Players_Games_Stats.passing_yard_total, Players_Games_Stats.passing_td_total, 
        Players_Games_Stats.rushing_yard_total, Players_Games_Stats.rushing_td_total, Players_Games_Stats.receiving_yard_total, Players_Games_Stats.receiving_td_total
        FROM Players_Games_Stats INNER JOIN Players ON Players_Games_Stats.player_id = Players.player_id WHERE Players_Games_Stats.player_stats_id = %s''' % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT player_id, CONCAT(fname, ' ', lname) AS name FROM Players ORDER BY lname ASC"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        player_data = cur.fetchall()

        query3 = "SELECT game_id FROM Games"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        game_data = cur.fetchall()


        # render edit_player_game page passing our query data to the edit_player_game template
        return render_template("edit_player_game.j2", data=data, player_data=player_data, game_data=game_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Player Game' button
        if request.form.get("Edit_Player_Game"):
            id = request.form["player_stats_id"]
            player_id = request.form["player_id"]
            game_id = request.form["game_id"]
            passing_yard_total = request.form["passing_yard_total"]
            passing_td_total = request.form["passing_td_total"]
            rushing_yard_total = request.form["rushing_yard_total"]
            rushing_td_total = request.form["rushing_td_total"]
            receiving_yard_total = request.form["receiving_yard_total"]
            receiving_td_total = request.form["receiving_td_total"]

            query = '''UPDATE Players_Games_Stats SET Players_Games_Stats.player_id = %s, Players_Games_Stats.game_id = %s, Players_Games_Stats.passing_yard_total = %s, Players_Games_Stats.passing_td_total = %s, 
            Players_Games_Stats.rushing_yard_total = %s, Players_Games_Stats.rushing_td_total = %s, Players_Games_Stats.receiving_yard_total = %s, Players_Games_Stats.receiving_td_total = %s 
            WHERE Players_Games_Stats.player_stats_id = %s'''
            cur = mysql.connection.cursor()
            cur.execute(query, (player_id, game_id, passing_yard_total, passing_td_total, rushing_yard_total, rushing_td_total, receiving_yard_total, receiving_td_total, id))
            mysql.connection.commit()

    # redirect back to teams page after we execute the update query
            return redirect("/player_game")


# route for seasons page
@app.route("/seasons", methods=["POST", "GET"])
def seasons():
    # Separate out the request methods, in this case this is for a POST
    # insert a season into the Seasons entity
    if request.method == "POST":
        # fire off if user presses the Add Team button
        if request.form.get("Add_Season"):
            # grab user form inputs
            season_year = request.form["season_year"]
            super_bowl_champ = request.form["super_bowl_champ"]
            super_bowl_runner_up = request.form["super_bowl_runner_up"]

            # Account for if the Super Bowl champ and runner up are not entered
            if super_bowl_champ == "none" and super_bowl_runner_up == "none":
                query = "INSERT INTO Seasons (season_year) VALUES (%s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (season_year))
                mysql.connection.commit()
            
            # Account for if the Super Bowl champ is not entered but runner up is
            elif super_bowl_champ == "none":
                query = "INSERT INTO Seasons (season_year, super_bowl_runner_up) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (season_year, super_bowl_runner_up))
                mysql.connection.commit()
            
            # Account for if the Super Bowl runner up is not enter but the champ is
            elif super_bowl_runner_up == "none":
                query = "INSERT INTO Seasons (season_year, super_bowl_champ) VALUES (%s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (season_year, super_bowl_champ))
                mysql.connection.commit()

            # Account for all Seasons attributes
            else:
                query = "INSERT INTO Seasons (season_year, super_bowl_champ, super_bowl_runner_up) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(query, (season_year, super_bowl_champ, super_bowl_runner_up))
                mysql.connection.commit()

            # redirect back to teams page
            return redirect("/seasons")

    # Grab Seaons data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in Teams
        query = "SELECT Seasons.season_year, Teams.team_name AS super_bowl_champ, t1.team_name AS super_bowl_runner_up FROM Seasons INNER JOIN Teams ON super_bowl_champ = Teams.team_id INNER JOIN Teams t1 ON super_bowl_runner_up = t1.team_id ORDER BY season_year DESC"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT team_id, team_name FROM Teams ORDER BY team_name ASC"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        team_data = cur.fetchall()

        # render edit_teams page passing our query data and homeworld data to the edit_team template
        return render_template("seasons.j2", data=data, teams=team_data)

    # Grab Seaons data so we send it to our template to display
    if request.method == "GET":
        # mySQL query to grab all the people in Teams
        query = "SELECT Seasons.season_year, Teams.team_name AS super_bowl_champ, t1.team_name AS super_bowl_runner_up FROM Seasons INNER JOIN Teams ON super_bowl_champ = Teams.team_id INNER JOIN Teams t1 ON super_bowl_runner_up = t1.team_id ORDER BY season_year DESC"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT team_id, team_name FROM Teams ORDER BY team_name ASC"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        team_data = cur.fetchall()

        # render edit_teams page passing our query data and homeworld data to the edit_team template
        return render_template("seasons.j2", data=data, teams=team_data)

@app.route("/delete_season/<int:id>")
def delete_season(id):
    # mySQL query to delete the person with our passed id
    query = "DELETE FROM Seasons WHERE season_year = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    # redirect back to seasons page
    return redirect("/seasons")

@app.route("/edit_season/<int:id>", methods=["POST", "GET"])
def edit_season(id):
    if request.method == "GET":
        # mySQL query to grab the info of the person with our passed id
        query = "SELECT Seasons.season_year, Teams.team_name AS super_bowl_champ, t1.team_name AS super_bowl_runner_up FROM Seasons INNER JOIN Teams ON super_bowl_champ = Teams.team_id INNER JOIN Teams t1 ON super_bowl_runner_up = t1.team_id WHERE Seasons.season_year = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query2 = "SELECT team_id, team_name FROM Teams ORDER BY team_name ASC"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        team_data = cur.fetchall()


        # render edit_team page passing our query data to the edit_people template
        return render_template("edit_season.j2", data=data, teams=team_data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Team' button
        if request.form.get("Edit_Season"):
            id = request.form["season_year"]
            super_bowl_champ = request.form["super_bowl_champ"]
            super_bowl_runner_up = request.form["super_bowl_runner_up"]

            if super_bowl_champ == "none" and super_bowl_runner_up == "none":
                query = "UPDATE Seasons SET Seasons.super_bowl_champ = NULL, Seasons.super_bowl_runner_up = NULL WHERE Seasons.season_year = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (id))
                mysql.connection.commit()
            
            elif super_bowl_champ == "none":
                query = "UPDATE Seasons SET Seasons.super_bowl_champ = NULL, Seasons.super_bowl_runner_up = %s WHERE Seasons.season_year = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (super_bowl_runner_up, id))
                mysql.connection.commit()

            elif super_bowl_runner_up == "none":
                query = "UPDATE Seasons SET Seasons.super_bowl_champ = %s, Seasons.super_bowl_runner_up = NULL WHERE Seasons.season_year = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (super_bowl_champ, id))
                mysql.connection.commit()

            else:
                query = "UPDATE Seasons SET Seasons.super_bowl_champ = %s, Seasons.super_bowl_runner_up = %s WHERE Seasons.season_year = %s"
                cur = mysql.connection.cursor()
                cur.execute(query, (super_bowl_champ, super_bowl_runner_up, id))
                mysql.connection.commit()

    # redirect back to teams page after we execute the update query
            return redirect("/seasons")



# Listener
# change the port number if deploying on the flip servers
if __name__ == "__main__":
    app.run(port=62112, debug=True)