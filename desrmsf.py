import os
import re
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def list_eaf_files():
    eaf_files = [file for file in os.listdir() if file.endswith(".eaf")]
    return eaf_files

def select_files(eaf_files):
    print("\nFound the following .eaf files:")
    for i, file in enumerate(eaf_files, 1):
        print(f"{i}) {file}")
    try:
        selections = input("Select which ones you want to use (separated by comma): ")
        selected_indices = [int(index) - 1 for index in selections.split(",")]
        selected_files = [eaf_files[index] for index in selected_indices]
        return selected_files
    except (ValueError, IndexError):
        print("Invalid selection. Please enter comma-separated numbers within the range.")
        return []

def enter_curve_names(num_curves):
    try:
        names = input(f"Enter the names for each curve (separated by comma, {num_curves} names expected): ")
        curve_names = [name.strip() for name in names.split(",")]
        if len(curve_names) != num_curves:
            print("Number of names doesn't match the number of selected files.")
            return None
        return curve_names
    except ValueError:
        print("Invalid input. Please enter comma-separated names.")
        return None

def extract_rmsf_values(file_path):
    first_term = '{RMSF = {'
    second_term = 'FitBy = "(((protein) and backbone) and not (atom.ele H)'

    with open(file_path, 'r') as file:
        lines = file.readlines()
        found_first_term = False
        found_second_term = False
        rmsf_values = []
        
        for line in lines:
            if first_term in line:
                found_first_term = True
            elif found_first_term and second_term in line:
                found_second_term = True
            elif found_first_term and found_second_term and "Result =" in line:
                try:
                    values_str = re.search(r'\[(.*?)\]', line).group(1)
                    rmsf_values = [float(val) for val in values_str.split()]
                    return rmsf_values
                except (IndexError, ValueError, AttributeError):
                    return None

    return None

def extract_residue_numbers(file_path):
    keyword = 'ProteinResidues ='
    with open(file_path, 'r') as file:
        for line in file:
            if keyword in line:
                try:
                    residue_numbers = re.findall(r'\d+', line)
                    return [int(number) for number in residue_numbers]
                except ValueError:
                    return None
    return None

def plot_rmsf_residue(selected_files, curve_names, time_step=0.1):
    plt.figure(figsize=(10, 6))  # Adjust figure size if needed
    colors = sns.color_palette("hsv", len(selected_files))  # Generate a list of colors
    for i, selected_file in enumerate(selected_files):
        rmsf_values = extract_rmsf_values(selected_file)
        residue_numbers = extract_residue_numbers(selected_file)
        if rmsf_values and residue_numbers:
            plt.plot(residue_numbers, rmsf_values, label=curve_names[i], color=colors[i])
        else:
            print(f"Failed to extract RMSF values or residue numbers from {selected_file}. Skipping...")
    plt.xlabel('Residue Number')
    plt.ylabel('RMSF (Angstrom)')
    plt.title('RMSF vs Residue Number')
    plt.legend()
    plt.show()

def main():
    eaf_files = list_eaf_files()
    if not eaf_files:
        print("No .eaf files found in the directory.")
        return

    selected_files = select_files(eaf_files)
    if not selected_files:
        return
    
    curve_names = enter_curve_names(len(selected_files))
    if not curve_names:
        return

    plot_rmsf_residue(selected_files, curve_names)

if __name__ == "__main__":
    main()

print("\nThank you byebye!\n")

