import csv
import psycopg2

username = 'Valentin'
password = 'qwerty123'
database = 'LW3'

INPUT_CSV_FILE1 = 'team_stats.csv'
INPUT_CSV_FILE2 = 'player_stats.csv'

query_0 = '''
DELETE FROM statistic;
DELETE FROM players;
DELETE FROM teams
'''

query_1 = '''
INSERT INTO teams (team_id, team_name, team_country) VALUES (%s, %s, %s)
'''

query_2 = '''
INSERT INTO players (player_id, team_id, player_name, player_country) VALUES (%s, %s, %s, %s)
'''

query_3 = '''
INSERT INTO statistic (stat_id, player_id, score, date) VALUES (%s, %s, %s, %s)
'''

conn = psycopg2.connect(user=username, password=password, dbname=database)

def func(line):
    temp_line = line[2:]
    res = list()
    for i in range(len(line)-2):
        if temp_line[i] != "'":
            res.append(temp_line[i])
        else:
            break
    return ''.join(res)


def curr_team_id(team):
    with open(INPUT_CSV_FILE1, 'r') as inf1:
        reader1 = csv.DictReader(inf1)
        for idx1, row1 in enumerate(reader1):
            if row1['name'] == func(team):
                return idx1+1
    return 0

with conn:
    cur = conn.cursor()
    cur.execute(query_0)
    v = (0, "no team", "no team")
    cur.execute(query_1, v)
    with open(INPUT_CSV_FILE1, 'r') as inf:
        reader = csv.DictReader(inf)
        for idx, row in enumerate(reader):
            values = (idx+1, row['name'], row['country'])
            cur.execute(query_1, values)
    with open(INPUT_CSV_FILE2, 'r') as inf:
        reader = csv.DictReader(inf)
        for idx, row in enumerate(reader):
            values1 = (idx+1, curr_team_id(row['teams']), row['name'], row['country'])
            cur.execute(query_2, values1)
            date = "21.12.2021"
            values2 = (idx+10000001, idx+1, row['rating'], date)
            cur.execute(query_3, values2)
    conn.commit()