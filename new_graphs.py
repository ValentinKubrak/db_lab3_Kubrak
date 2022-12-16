import psycopg2
import matplotlib.pyplot as plt

username = 'Valentin'
password = 'qwerty123'
database = 'LW3'
host = 'localhost'
port = '5432'

#Топ 10 країн по кількості професійних гравців
query_1 = '''
select * from TopCountCountry
'''
#Створення view TopCountCountry
'''
create view TopCountCountry as
select trim(player_country), count(player_country) 
from players group by player_country 
order by count(player_country) desc limit 10
'''
#Кільіксть гравців, що грають у команах своєї карїни та кількість гравців, що грають у закордонних командах
query_2 = '''
select * from TeamStatus
'''
#Створення view TeamStatus
'''
create view TeamStatus as
select 'in "home" team' as "status", count(*) 
from teams join players on teams.team_id = players.team_id where teams.team_country = players.player_country
union
select 'in foreign team', count(*) 
from teams join players on teams.team_id = players.team_id where teams.team_country != players.player_country
'''
#Відношення гравця до своїх набраних балів (5 найкращих та 5 найгірших гравців)
query_3 = '''
select * from BestAndWorst
'''
#Створення view BestAndWorst
'''
create view BestAndWorst as
(select * from top5_players
union
select * from bad5_players) order by score desc
'''
#Створення проміжних view top5_players та bad5_players
'''
create view top5_players as
select trim(player_name), score from statistic join players on statistic.player_id = players.player_id limit 5
'''
'''
create view bad5_players as
select trim(player_name), score from statistic join players on statistic.player_id = players.player_id order by score limit 5
'''
conn = psycopg2.connect(user=username, password=password, dbname=database, host=host, port=port)

with conn:
    cur = conn.cursor()
    cur.execute(query_1)
    country = []
    count = []

    for row in cur:
        country.append(row[0])
        count.append(row[1])

    x_range = range(len(country))

    figure, (bar_ax, pie_ax, graph_ax) = plt.subplots(1, 3)

    bar_ax.bar(x_range, count, label='Total')
    bar_ax.set_title('Top 10 countries by number of pro players')
    bar_ax.set_xlabel('Country')
    bar_ax.set_ylabel('Count')
    bar_ax.set_xticks(x_range)
    bar_ax.set_xticklabels(country,  rotation=30)

    cur.execute(query_2)
    players = []
    count = []

    for row in cur:
        players.append(row[0])
        count.append(row[1])

    pie_ax.pie(count, labels=players, autopct='%1.1f%%')
    pie_ax.set_title('The ratio of the player to the team of his country')

    cur.execute(query_3)
    player = []
    score = []

    for row in cur:
        player.append(row[0])
        score.append(row[1])

    graph_ax.plot(player, score, marker='o')
    graph_ax.set_xticks(player)
    graph_ax.set_xticklabels(player, rotation=30)
    graph_ax.set_xlabel('Player')
    graph_ax.set_ylabel('Score')
    graph_ax.set_title('The ratio of the best 5 players to the worst 5 by points')

    for i, j in zip(player, score):
        graph_ax.annotate(j, xy=(i, j), xytext=(7, 2), textcoords='offset points')

mng = plt.get_current_fig_manager()
mng.resize(1920, 1080)

plt.show()