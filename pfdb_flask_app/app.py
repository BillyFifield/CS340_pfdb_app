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
app.config["MYSQL_USER"] = "cs340_username"
app.config["MYSQL_PASSWORD"] = "XXXX"
app.config["MYSQL_DB"] = "cs340_username"
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
        query = "SELECT team_id, team_city, team_name, conference FROM Teams"
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
        query = "SELECT * FROM Teams WHERE team_id = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()


        # render edit_team page passing our query data to the edit_people template
        return render_template("edit_team.j2", data=data)

    # meat and potatoes of our update functionality
    if request.method == "POST":
        # fire off if user clicks the 'Edit Team' button

        query = "UPDATE Teams SET Teams.team_city = %s, Teams.team_name = %s, Teams.conference = %s WHERE Teams.team_id = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (team_city, team_name, conference, id))
        mysql.connection.commit()

        # redirect back to teams page after we execute the update query
        return redirect("/teams")


# Listener
# change the port number if deploying on the flip servers
if __name__ == "__main__":
    app.run(port=62112, debug=True)