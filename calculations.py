import csv
import math
from config import detailed_logs, wWL, wCS

def composite_score(data):
    # Composite Score = Sum of weighted team stats
    data['composite_score'] = (wCS['w_eFG'] * data['eFGp'] + wCS['w_TOV'] * data['TOVp'] +
                                wCS['w_OREB'] * data['OREBp'] + wCS['w_FTR'] * data['FTR'] + 
                                wCS.get('w_home_adv', 0) * data['home_away_NS'])
    # eFGp (Effective Field Goal Percentage)
    # FTR (Free Throw Rate)
    # TOVp (Turnover Percentage)
    # OREBp (Offensive Rebound Percentage)
    
    # Rank teams through composite score
    return data.sort_values(by='composite_score', ascending=False).reset_index(drop=True)

def game_outcomes(data):
    results = []
    data = data.sort_values(by='game_id')
    for i in range(math.floor(len(data)/2)):
        round_outcome = []
        if (data.iloc[2*i, 0] == data.iloc[2*i + 1, 0]):
            round_outcome.append(data.iloc[2*i, 0])
            round_outcome.append(data.iloc[2*i, 2])
            round_outcome.append(data.iloc[2*i + 1, 2])
            score1 = data.iloc[2*i, 18]
            score2 = data.iloc[2*i + 1, 18]
            if score1 > score2:
                # Team1 wins
                round_outcome.append('team1')
                if (data.iloc[2*i, 28]) == 1:
                    round_outcome.append('home')
                elif (data.iloc[2*i, 28]) == 0:
                    round_outcome.append('neutral')
                else:
                    round_outcome.append('away')
            elif score2 > score1:
                # Team2 wins
                round_outcome.append('team2')
                if (data.iloc[2*i, 28]) == 1:
                    round_outcome.append('home')
                elif (data.iloc[2*i, 28]) == 0:
                    round_outcome.append('neutral')
                else:
                    round_outcome.append('away')
            else:
                # Tie
                round_outcome.append('tie')
                if (data.iloc[2*i, 28]) == 1:
                    round_outcome.append('home')
                elif (data.iloc[2*i, 28]) == 0:
                    round_outcome.append('neutral')
                else:
                    round_outcome.append('away')
            round_outcome.append(data.loc[2*i, 'twoPp'] * 2 + data.loc[2*i, 'threePp'] * 3)
            round_outcome.append(data.loc[2*i + 1, 'twoPp'] * 2 + data.loc[2*i + 1, 'threePp'] * 3)
            round_outcome.append(score1 - score2)
            results.append(round_outcome)
            if detailed_logs is True: print(f'{round_outcome}')
    if detailed_logs is True: print('\nFinished Game_Outcomes\n')
    return results

# Get a high win rate team as our max
# Result Array = [Game_ID, Team1, Team2, Winning Team, Location, %2P, %3P, Pt diff]
# Win rate = WR, RATING (new) = Rn, RATING (old) = Ro
# Game result = S (1 for WIN, 0.5 for TIE, 0 for loss)
# a modified elo equation, I have the normal one but for basketball we should consider mor vars like
# home court advantage, margin of victory, etc.

def expected_score(team1, team2, elo, home_adv):
    elo1, elo2 = elo[team1], elo[team2]
    if home_adv == 'team1':
        elo1 += 100
    elif home_adv == 'team2':
        elo2 += 100
    expected1 = 1 / (1 + 10 ** ((elo2 - elo1) / 400))
    expected2 = 1 / (1 + 10 ** ((elo1 - elo2) / 400))
    if expected1 > expected2:
        return ['team1', expected1, expected2]
    elif expected2 > expected1:
        return ['team2', expected1, expected2]
    else:
        return ['tie', expected1, expected2]

def elo_rating(teams, results):
    if detailed_logs is True: print('Starting ELO Rating\n')
    elo = {}
    for i in teams:
        elo[i] = 1500
    for i in results:
        team1, team2, winner, location = i[1], i[2], i[3], i[4]
        if detailed_logs is True: print('Evaluating' + team1 + ' vs ' + team2 + 
                                        ' where ' + winner + ' wins at ' + location)
        if location == 'neutral':
            home_adv= 'neutral'
        elif (winner == 'team1' and location == 'away') or (winner == 'team2' and location == 'home'):
            home_adv = 'team2'
        else:
            home_adv = 'team1'
        expected = expected_score(team1, team2, elo, home_adv)
        margin_of_victory = abs(i[7])
        S1 = 1 / (1 + math.exp(-1 * i[7] / 10))
        S2 = 1 - S1
        def K_factor(margin_of_victory):
            return 24 * (1 + margin_of_victory / 30) 
        elo[team1] += K_factor(margin_of_victory) * (S1 - expected[1])
        elo[team2] += K_factor(margin_of_victory) * (S2 - expected[2])
        if detailed_logs is True: print(f'Team1: {team1} ELO: {elo[team1]}')
        if detailed_logs is True: print(f'Team2: {team2} ELO: {elo[team2]}\n')
    
    # Sort the dictionary by value in descending order
    elo = dict(sorted(elo.items(), key=lambda item: item[1], reverse=True))

    # Write the dictionary to the CSV file
    with open('output/team_elo.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(['Team', 'Elo Rating'])
        
        for team, elo_rating in elo.items():
            writer.writerow([team, elo_rating])

    print("ELO saved to output/team_elo.csv\n")

    return elo

def elo_region_rankings(team_data, elo):
    north = {}
    south = {}
    west = {}
    for i in team_data.keys():
        if team_data[i] == 'North':
            north[i] = elo[i]
        elif team_data[i] == 'South':
            south[i] = elo[i]
        elif team_data[i] == 'West':
            west[i] = elo[i]
    north = dict(sorted(north.items(), key=lambda item: item[1], reverse=True))
    south = dict(sorted(south.items(), key=lambda item: item[1], reverse=True))
    west = dict(sorted(west.items(), key=lambda item: item[1], reverse=True))

    with open('output/north_rankings.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(['Team', 'Elo Rating'])
        
        for team, elo_rating in north.items():
            writer.writerow([team, elo_rating])

    print("ELO saved to output/north_rankings.csv\n")

    with open('output/south_rankings.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(['Team', 'Elo Rating'])
        
        for team, elo_rating in south.items():
            writer.writerow([team, elo_rating])

    print("ELO saved to output/south_rankings.csv\n")

    with open('output/west_rankings.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        
        writer.writerow(['Team', 'Elo Rating'])
        
        for team, elo_rating in west.items():
            writer.writerow([team, elo_rating])

    print("ELO saved to output/west_rankings.csv\n")
