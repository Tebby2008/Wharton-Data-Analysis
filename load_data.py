import pandas as pd
def load_data(file_path):
    return pd.read_csv(file_path)

def to_dict(data):
    dictionary = {}
    for i in range(len(data)): dictionary[data.iloc[i, 0]] = data.iloc[i, 1]
    return dictionary