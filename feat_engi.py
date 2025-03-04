import numpy as np
import pandas as pd
from config import detailed_logs
import csv

def calc_shoot_percentage(data_type, data):
    if detailed_logs: print(f'Calculating {data_type}')
    TFGA = data['FGA_2'] + data['FGA_3']
    TFGM = data['FGM_2'] + data['FGM_3']
    if data_type == 'TFGA':
        return TFGA
    elif data_type == 'TFGM':
        return TFGM
    elif data_type == 'TFGp':
        return TFGM / TFGA
    elif data_type == 'twoPp':
        return data['FGM_2'] / data['FGA_2']
    elif data_type == 'threePp':
        return data['FGM_3'] / data['FGA_3']
    elif data_type == 'FTp':
        return data['FTM'] / data['FTA']
    elif data_type == 'eFGp':
        return (data['FGM_2'] + data['FGM_3'] * 1.5) / TFGA
    elif data_type == 'eFPp':
        return (data['FGM_2'] * 2+ data['FGM_3'] * 3 + data['FTM']) / (2*(data['FGA_2'] + data['FGA_3'] + data['FTA']))
    else:
        return np.nan

def calc_metrics(data_type, data):
    if data_type == 'TOVp':
        return data['TOV'] / (data['FGA_2'] + data['FGA_3'] + 0.475 * data['FTA'] + data['TOV'])
    elif data_type == 'OREBp':
        return data['OREB'] / (data['OREB'] + data['DREB'])
    elif data_type == 'FTR':
        return data['FTA'] / (data['FGA_2'] + data['FGA_3'])
    else:
        return np.nan

def master_data(data):
    if detailed_logs: print('Compiling Master Data')
    data['TFGA'] = calc_shoot_percentage('TFGA', data)
    data['TFGM'] = calc_shoot_percentage('TFGM', data)
    data['TFGp'] = calc_shoot_percentage('TFGp', data)
    data['twoPp'] = calc_shoot_percentage('twoPp', data)
    data['threePp'] = calc_shoot_percentage('threePp', data)
    data['FTp'] = calc_shoot_percentage('FTp', data)
    data['eFGp'] = calc_shoot_percentage('eFGp', data)
    data['eFPp'] = calc_shoot_percentage('eFPp', data)
    data['TOVp'] = calc_metrics('TOVp', data)
    data['OREBp'] = calc_metrics('OREBp', data)
    data['FTR'] = calc_metrics('FTR', data)
    if detailed_logs: print('Master Data Compiled Successfully\n')
    return data

def team_stats(data):
    if detailed_logs: print('Finding Team Mean Stats')
    teams = data['team']
    data = data.drop(columns=['home_away', 'notD1_incomplete', 'team', 'game_id', 'game_date'])
    data['OT_length_min_tot'] = data['OT_length_min_tot'].fillna(0)
    grouped_data = data.groupby(teams)
    team_data = {}
    for team, group in grouped_data:
        team_data[team] = {}
        for i in group.columns:
            values = group[i].dropna()
            
            if len(values) > 0:
                mean_value = values.mean()
            else:
                mean_value = 0
            team_data[team][i] = mean_value
    team_data = pd.DataFrame.from_dict(team_data, orient='index')
    team_data = team_data.reset_index()
    team_data.rename(columns={'index': 'team'}, inplace=True)
    team_data.to_csv('output/team_stats.csv')
    return team_data

def win_percentage(teams, results):
    if detailed_logs: print('Finding Win%')
    w_data = {}
    l_data = {}
    for i in teams:
        w_data[i] = 0
        l_data[i] = 0
    for i in results:
        team1, team2, winner = i[1], i[2], i[3]
        if winner == 'team2':
            w_data[team2] += 1
            l_data[team1] += 1
        elif winner == 'team1':
            w_data[team1] += 1
            l_data[team2] += 1
    percentages = {}
    for i in teams:
        percentages[i] = w_data[i] / (w_data[i] + l_data[i])
    
    return percentages