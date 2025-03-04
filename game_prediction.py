import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm
from config import detailed_logs
from feat_engi import master_data
from load_data import load_data
from calculations import game_outcomes

def round_data_comparison(data):
    results = game_outcomes(data)
    score_df = pd.DataFrame(columns=['team', 'score_diff'])
    y_var = 'attendance'
    data = data.groupby('team')[y_var].apply(list).reset_index()
    comparison_data = data[y_var].tolist()
    for i in range(len(results)):
        j = {'team': results[i][1], 'score_diff': results[i][7]}
        score_df = pd.concat([score_df, pd.DataFrame([j])], ignore_index=True)
        j = {'team': results[i][2], 'score_diff': -1 * results[i][7]}
        score_df = pd.concat([score_df, pd.DataFrame([j])], ignore_index=True)
    score_df = score_df.groupby('team')['score_diff'].apply(list).reset_index()
    score_diff = score_df['score_diff'].tolist()
    return score_diff, comparison_data


def graph(x_var, y_var):
    if detailed_logs: print(f'{y_var}\n{x_var}\nFound {len(y_var)} items in y_var and {len(x_var)} items in x_var')
    model = sm.OLS(y_var, x_var)
    results = model.fit()
    fig, ax = plt.subplots(figsize=(8,6))
    win_fitted=results.fittedvalues
    print(results.summary())
    ax.plot(x_var, y_var, 'o', label = 'Data')
    ax.plot(x_var, win_fitted, 'r--', label = 'OLS')
    ax.autoscale()
    plt.show()
    
data_directory = 'games_2022.csv'
data = master_data(load_data(data_directory))
teams = data['team'].unique()
x, y = round_data_comparison(data)
for i in range(len(x)):
    if len(x[i]) < 2: 
        if detailed_logs: print(f'Not enough data for {teams[i]}') ; continue
    graph(x[i], y[i])