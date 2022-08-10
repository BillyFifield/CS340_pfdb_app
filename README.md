# CS340_pfdb_app

PDFB is a football database written in Flask and SQL. The database allows the user to manipulate data by adding and removing game data, player data,
team data, as well as team data. The database allows the user to use the CRUD operations on all 5 entities, including player game statistics as well.

The SQL is written to include foreign keys for each entity that will cascade to all entities that it is apart of.

To run this application, Python's Flask will need to be installed by running the following:

      pip install flask-mysqldb
