# WHSBKT Data Prediction Algorithm

The WHSBKT Data Prediction Algorithm is an algorithm designed for the Wharton High School Data Science Competition. It is written in 100% Python and utilizes the ELO ranking system as its core underlying theory.

## Usage

To install, download the .zip file or go to the following link: https://github.com/Tebby2008/Wharton-Data-Analysis/blob/fa5ae9fb7cce5f7c28af185f6fa8073f72508ea4/WhartonDataAnalysis.zip

The required inputs should be already present in the main folder.

Output files will be created in the ``/outputs`` folder.

Run the main file ``main.py`` for the algorithm to start.

## Config

You may find the config in the main file ``config.py``.

``run_elo`` - Runs the algorithm to determine the ELO of the input Basketball teams and then ranks them from greatest to least amount of points.

``run_score_accuracy_rankings`` - Runs the algorithm to determine and output the rankings of each team based on shot accuracies, etc.

``output_elo_predictions`` - Uses the previously determined ELO rankings to predict the win rate of the scenario matches from the input file.

``detailed_logs`` - Provides more detailed console outputs by logging smaller processes, useful for debugging. (Program will run slower)

``wCS`` - The weightings for eFGp (Effective Field Goal Percentage), FTR (Free Throw Rate), TOVp (Turnover Percentage), and OREBp (Offensive Rebound Percentage) respectively in the calculation for the composite score. (Default 'w_eFG': 0.4, 'w_TOV': -0.25, 'w_OREB': 0.2, 'w_FTR': 0.15)

## game_predictions.py

``game_predictions.py`` is a separate executable python algorithm that graphs out the correlation between the point difference and external factors found on the spreadsheet. You may change the external factors by editing the ``y_var`` within the ``round_data_comparison`` function.

## References

All data used were provided by the Wharton High School Data Science Competition from the NCAA Women's Division I Basketball games. This model was one of the 25 semifinalists in the 2025 Wharton HS Data Science Competition. 
