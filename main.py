import psycopg2
import matplotlib.pyplot as plt

username = 'Valentin'
password = 'qwerty123'
database = 'LW2'
host = 'localhost'
port = '5432'

#Кільіксть гравцій в тій чи іншій країні
query_1 = '''
select * from CountCountry
'''
'''
create view CountCountry as
select trim(country), count(country) from player group by country
'''
#Кільіксть гравців, що грають у команах своєї карїни та кількість гравців, що грають у закордонних командах
query_2 = '''
select * from TeamStatus
'''
'''
create view TeamStatus as
select 'in "home" team' as "status", count(*) 
from team join player on team.team_id = player.team_id where team.country = player.country
union
select 'in foreign team', count(*) 
from team join player on team.team_id = player.team_id where team.country != player.country
'''
#Відношення гравця до своїх набраних балів
query_3 = '''
select * from PlayerScore
'''
'''
create view PlayerScore as
select trim(player_name), score from statistic join player on statistic.player_id = player.player_id
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
    bar_ax.set_title('Total number of players in the country')
    bar_ax.set_xlabel('Country')
    bar_ax.set_ylabel('Count')
    bar_ax.set_xticks(x_range)
    bar_ax.set_xticklabels(country,  rotation=15)

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
    graph_ax.set_xticklabels(player, rotation=20)
    graph_ax.set_xlabel('Player')
    graph_ax.set_ylabel('Score')
    graph_ax.set_title('The ratio of the player to the points')

    for i, j in zip(player, score):
        graph_ax.annotate(j, xy=(i, j), xytext=(7, 2), textcoords='offset points')

mng = plt.get_current_fig_manager()
mng.resize(1400, 650)

plt.show()