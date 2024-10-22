import sqlite3
import csv

conn = sqlite3.connect("db.db")
cursor = conn.cursor()

query = "CREATE TABLE IF NOT EXISTS sys_command(id integer primary key, name VARCHAR(100), path VARCHAR(1000))"
cursor.execute(query)

# query = "INSERT INTO sys_command VALUES (null, 'one note', 'C:\\Program Files\\Microsoft Office\root\\Office16\\ONENOTE.exe')"
# cursor.execute(query)
# conn.commit()

# query = "CREATE TABLE IF NOT EXISTS web_command(id integer primary key, name VARCHAR(100), url VARCHAR(1000))"
# cursor.execute(query)

# query = "INSERT INTO web_command VALUES (null, 'youtube', 'https://www.youtube.com')"
# cursor.execute(query)
# conn.commit()

# query = "UPDATE sys_command SET name = 'note', path = 'C:\\Program Files\\Microsoft Officeoot\\Office16\\ONENOTE.exe' WHERE name = 'one note';"
# cursor.execute(query)
# conn.commit()

# Create a table with the desired columns
cursor.execute('''CREATE TABLE IF NOT EXISTS contacte (id integer primary key, name VARCHAR(200), mobile_no VARCHAR(255))''')

# Specify the column indices you want to import (0-based index)
# Example: Importing the 1st and 3rd columns
desired_columns_indices = [0, 30]

# Read data from CSV and insert into SQLite table for the desired columns
with open('contacts.csv', 'r', encoding='utf-8') as csvfile:
    csvreader = csv.reader(csvfile)
    
    # Sauter l'en-tête si nécessaire
    next(csvreader)
    
    # Parcourir chaque ligne du fichier CSV
    for row in csvreader:
        # Sélectionner les colonnes désirées (par exemple, la colonne 1 pour le nom et la colonne 2 pour le numéro)
        selected_data = (row[0], row[1], row[2])  # row[1] pour 'name', row[2] pour 'mobile_no'
        
        # Exécuter la requête d'insertion
        cursor.execute(''' 
        INSERT INTO contacte (id, name, mobile_no) 
        VALUES (?, ?, ?);
        ''', selected_data)

# Confirmer les changements
conn.commit()

# Fermer la connexion à la base de données
conn.close()