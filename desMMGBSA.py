import os
import pandas as pd
import matplotlib.pyplot as plt

def load_csv_files():
    """
    Function to load all CSV files in the current directory.
    """
    csv_files = [file for file in os.listdir() if file.endswith('.csv')]
    return csv_files

def choose_csv_file(csv_files):
    """
    Function to prompt the user to choose a CSV file.
    """
    print("\nAvailable CSV files:")
    for i, file in enumerate(csv_files):
        print(f"{i + 1}. {file}")
    choice = int(input("Enter the number corresponding to the CSV file you want to analyze: ")) - 1
    return csv_files[choice]

def get_compound_name(data):
    """
    Function to retrieve the compound name from the first row of the data.
    """
    return data.iloc[0, 0]

def filter_columns(data):
    """
    Function to filter out string columns.
    """
    return data.select_dtypes(exclude=['object'])

def generate_statistics(data):
    """
    Function to generate statistics from a given CSV file.
    """
    statistics = data.describe().transpose()
    statistics['median'] = data.median()
    statistics = statistics[['mean', '50%', 'std', 'min', 'max']]
    statistics.columns = ['average', 'median', 'standard deviation', 'min_value', 'max_value']
    return statistics

def filter_zero_rows(statistics):
    """
    Function to filter out rows where all statistics are equal to zero.
    """
    return statistics[(statistics != 0).any(axis=1)]

def filter_nan_rows(statistics):
    """
    Function to filter out rows producing NaN values in the statistical results.
    """
    return statistics.dropna()

def save_statistics_to_file(statistics, csv_file, compound_name):
    """
    Function to save statistics to a text file.
    """
    with open('output.txt', 'w') as f:
        f.write(f'Statistics for {csv_file}:\n')
        f.write(f'Compound Name: {compound_name}\n')
        f.write(statistics.to_string())

def main():
    csv_files = load_csv_files()
    if not csv_files:
        print("No CSV files found in the current directory.")
        return
    
    csv_file = choose_csv_file(csv_files)
    data = pd.read_csv(csv_file)
    compound_name = get_compound_name(data)
    data = filter_columns(data.drop(columns=['title']))
    statistics = generate_statistics(data)
    statistics_filtered = filter_zero_rows(statistics)
    statistics_filtered = filter_nan_rows(statistics_filtered)  
    save_statistics_to_file(statistics_filtered, csv_file, compound_name)
    print("\nThank you byebye!\n")

if __name__ == "__main__":
    main()

