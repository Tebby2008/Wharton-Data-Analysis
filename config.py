# config
run_elo = True
run_score_accuracy_rankings = False
output_elo_predictions = True
detailed_logs = True # Recommended True for debugging
wCS = {'w_eFG': 0.4, 'w_TOV': -0.25, 'w_OREB': 0.2, 'w_FTR': 0.15} # Weight for Composite Score

# Install Requirements
def install_requirements():
    import sys
    import subprocess
    def install(package):
        try:
            print(f"Checking {package}")
            __import__(package)
        except ImportError:
            print(f"Package {package} not found. Installing...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])
    install('pandas')
    install('numpy')
    install('statsmodels')
    install('matplotlib')
    print("All required packages are installed and imported successfully.")