import matplotlib.pyplot as plt
import numpy as np
import glob
import os
import pandas as pd

def extract_rg_values(file_path):
    try:
        df = pd.read_csv(file_path)
        time_values = df['Time (ns)'].values
        rg_column = [col for col in df.columns if 'Radius of Gyration' in col][0]
        rg_values = df[rg_column].values
        return time_values, rg_values
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None, None

def get_all_csv_files():
    return glob.glob('*.csv')

def get_curve_name(file_path):
    return os.path.basename(file_path).replace('.csv', '')

def plot_rg_time(selected_files, curve_names, unit_conversion):
    colors = plt.cm.get_cmap('tab10', len(selected_files))

    for i, file in enumerate(selected_files):
        time_values, rg_values = extract_rg_values(file)
        if time_values is None or rg_values is None:
            print(f"Could not extract data from {file}")
            continue

        rg_values = [value / unit_conversion for value in rg_values]  # Apply unit conversion to Y-axis
        plt.plot(time_values, rg_values, label=curve_names[i], color=colors(i))

    plt.xlabel('Time (ns)')
    plt.ylabel(f'Radius of Gyration ({"Å" if unit_conversion == 1 else "nm"})')
    plt.legend()
    plt.title('Radius of Gyration over Time')
    plt.show()

def main():
    unit_conversion = float(input("Enter the unit conversion factor for Radius of Gyration (1 for Å, 10 for nm): "))

    csv_files = get_all_csv_files()
    if not csv_files:
        print("No CSV files found in the current directory.")
        return

    print("Available CSV files:")
    for idx, file in enumerate(csv_files):
        print(f"{idx + 1}. {file}")

    selected_indices = input("Enter the numbers of the files you want to select, separated by commas: ")
    selected_indices = [int(i) - 1 for i in selected_indices.split(",")]
    selected_files = [csv_files[i] for i in selected_indices]
    curve_names = [get_curve_name(file) for file in selected_files]

    plot_rg_time(selected_files, curve_names, unit_conversion)

if __name__ == "__main__":
    main()

