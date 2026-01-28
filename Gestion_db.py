import sqlite3

connection = sqlite3.connect('db.sqlite')

cursor = connection.cursor()

#Creation table Chambres

command1 ="CREATE TABLE IF NOT EXISTS chambre (id INTEGER PRIMARY KEY, nbcouchage INTEGER, prix DOUBLE)"
cursor.execute(command1)

#Creation table Clients

command3 = "CREATE TABLE IF NOT EXISTS client(id INTEGER PRIMARY KEY, nom TEXT, prenom TEXT)"
cursor.execute(command3)

#Creation table Reservations

command2 = "CREATE TABLE IF NOT EXISTS reservation (id INTEGER PRIMARY KEY,idclient INTEGER, idchambre INTEGER , datedebut TEXT, datefin TEXT, dejeuner BOOLEAN, spa BOOLEAN, parking BOOLEAN, FOREIGN KEY(idclient) REFERENCES client(id),FOREIGN KEY(idchambre) REFERENCES chambre(id))"
cursor.execute(command2)

#Ajout Chambres 

cursor.execute("INSERT INTO chambre VALUES (1,2,60.99)")
cursor.execute("INSERT INTO chambre VALUES (2,2,60.99)")
cursor.execute("INSERT INTO chambre VALUES (3,2,60.99)")
cursor.execute("INSERT INTO chambre VALUES (4,2,60.99)")
cursor.execute("INSERT INTO chambre VALUES (5,3,80.99)")
cursor.execute("INSERT INTO chambre VALUES (6,3,80.99)")
cursor.execute("INSERT INTO chambre VALUES (7,3,80.99)")
cursor.execute("INSERT INTO chambre VALUES (8,3,80.99)")
cursor.execute("INSERT INTO chambre VALUES (9,3,80.99)")
cursor.execute("INSERT INTO chambre VALUES (10,4,99.99)")
cursor.execute("INSERT INTO chambre VALUES (11,4,99.99)")
cursor.execute("INSERT INTO chambre VALUES (12,4,99.99)")
cursor.execute("INSERT INTO chambre VALUES (13,4,99.99)")
cursor.execute("INSERT INTO chambre VALUES (14,4,99.99)")
cursor.execute("INSERT INTO chambre VALUES (15,4,99.99)")

cursor.execute("SELECT * FROM  chambre")

print(cursor.fetchall())