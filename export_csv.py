import csv
import psycopg2

username = 'Valentin'
password = 'qwerty123'
database = 'LW3'

OUTPUT_FILES = [
        'export_teams.csv',
        'export_players.csv',
        'export_statistic.csv'
]

TABLES = [
    'teams',
    'players',
    'statistic'
]

conn = psycopg2.connect(user=username, password=password, dbname=database)

with conn:
    cur = conn.cursor()

    for i in range(len(TABLES)):
        cur.execute('SELECT * FROM ' + TABLES[i])
        fields = [x[0] for x in cur.description]
        with open(OUTPUT_FILES[i].format(TABLES[i]), 'w') as outfile:
            writer = csv.writer(outfile)
            writer.writerow(fields)
            for row in cur:
                writer.writerow([str(x) for x in row])