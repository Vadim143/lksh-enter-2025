# from imghdr import test_exr
# from logging import StringTemplateStyle

from console_sol.api import *
import sys

teams = fetch_teams()
matches = fetch_matches()
team_by_id = dict()
team_by_name = dict()

players = set()
for team in teams:
    team_by_name[team['name']] = team
    team_by_id[team['id']] = team
    for id in team['players']:
        players.add(id)


def convert_id(id):
    player = fetch_player(id)
    name = player.name
    if player.surname is not None:
        name += f' {player.surname}'
    return name


players = sorted(map(convert_id, players))
print(*players, sep='\n')

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    else:
        request, tmp = line.split("?")
        tmp = tmp.strip()
        request = request.strip()
        if request == 'stats':
            name = tmp[1:-1]
            id = team_by_name[name]['id']
            wins = loses = scored = missed = 0
            for match in matches:
                t1s = match['team1_score']
                t2s = match['team2_score']
                if match['team1'] == id:
                    scored += t1s
                    missed += t2s
                    if t1s > t2s:
                        wins += 1
                    else:
                        loses += 1
                elif match['team2'] == id:
                    scored += t2s
                    missed += t1s
                    if t1s < t2s:
                        wins += 1
                    else:
                        loses += 1
            print(wins, loses, scored - missed)
        elif request == 'versus':
            p1, p2 = map(int, tmp.split())
            cnt = 0
            for match in matches:
                t1 = team_by_id[match['team1']]
                t2 = team_by_id[match['team2']]
                t1ps = t1['players']
                t2ps = t2['players']
                if (p1 in t1ps and p2 in t2ps) or (p2 in t1ps and p1 in t2ps):
                    cnt += 1
            print(cnt)

