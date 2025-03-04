from config import run_elo, run_score_accuracy_rankings, output_elo_predictions, install_requirements
install_requirements()
from load_data import load_data, to_dict
from feat_engi import master_data, team_stats
from calculations import composite_score, elo_rating, elo_region_rankings, game_outcomes, expected_score
import csv
import sys

if output_elo_predictions is True and run_elo is False:
    print("Error: output_elo_predictions is True but run_elo is False. No output will be generated.")
    sys.exit(0)

# Clear output folder
import os
import shutil
if os.path.exists('output'):
    shutil.rmtree('output')
os.makedirs('output')

# Load and process data
data_directory = 'games_2022.csv'
user_input = input('Enter the directory of the game data: ')
if user_input != '':
    data_directory = user_input
data = master_data(load_data(data_directory))
data.to_csv('output/master_data.csv')

# Save teams list (for ELO)
if run_elo is True: 
    teams = data['team'].unique()
    with open('output/teams.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
            
        writer.writerow(['Team'])
        
        for team in teams:
            writer.writerow([team])
    print("Teams list saved to output/teams.csv\n")


# Organize into teams (for Score Accuracy Prediction)
if run_score_accuracy_rankings is True: team_data = team_stats(data)

# Elo Rating
if run_elo is True: elo = elo_rating(teams, game_outcomes(data))

# Output Score Accuracy Rankings
if run_score_accuracy_rankings is True:
    with open('output/team_rank_%', mode='w') as file:
        file.write(str(composite_score(team_data).head(32))
    )
    print("Rankings saved to output/team_rank_%\n")

# Elo Rankings based on region
if run_elo is True: elo_region_rankings(to_dict(load_data('regions.csv')), elo)

# Predictions (ELO)
if output_elo_predictions is True:
    data_directory = 'predict.csv'
    user_input = input('Enter the directory of data to predict: ')
    if user_input != '':
        data_directory = user_input
    data = load_data(data_directory)
    win_rates = []
    for i in range(len(data)):
        if data.iloc[i, 0] == 'game_id':
            continue
        win_rates.append(str(expected_score(data.iloc[i, 2], data.iloc[i, 3], 
                                            elo, data.iloc[i, 2])[1]))
        # expected_score[1] will always be the expected winrate for team 1, which in this case is always the home team.
    data['WINNING %'] = win_rates
    data.to_csv('output/predicted.csv')
    print("Predictions saved to output/predicted.csv")