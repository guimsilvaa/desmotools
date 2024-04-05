import os
import re
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def select_number_of_files():
    while True:
        try:
            num_files = int(input("\nEnter the number of PDF plots you wanna generate within the output image: "))
            if num_files > 0:
                return num_files
            else:
                print("Invalid input. Please enter a positive number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def list_eaf_files():
    eaf_files = [file for file in os.listdir() if file.endswith(".eaf")]
    return eaf_files

def select_file(eaf_files):
    print("\nFound the following .eaf files:")
    for i, file in enumerate(eaf_files, 1):
        print(f"{i}) {file}")
    while True:
        try:
            selection = int(input("Select which one you wanna use (one at a time): "))
            if 1 <= selection <= len(eaf_files):
                return eaf_files[selection - 1]
            else:
                print("Invalid selection. Please enter a number within the range.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def select_structure_type():
    while True:
        try:
            structure_type = int(input("\nSelect the type of structure:\n1) Apo\n2) Holo\nEnter the corresponding number: "))
            if structure_type in [1, 2]:
                return structure_type
            else:
                print("Invalid selection. Please enter either 1 or 2.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def extract_rmsd_values(file_path, structure_type):
    if structure_type == 1:  # Apo
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if 'ASL = "(((protein) and backbone) and not (atom.ele H) )"' in line:
                    # Find the line with RMSD values after ASL
                    for j in range(i+1, min(i+5, len(lines))):  # Search within the next 5 lines
                        if "Result =" in lines[j]:
                            try:
                                rmsd_values = [float(val) for val in lines[j].split("[")[1].split("]")[0].split()]
                                return rmsd_values
                            except (IndexError, ValueError):
                                return None
            return None
    elif structure_type == 2:  # Holo
        # Prompt user to select what to consider for building the PDF plot for holo structure
        print("\nYour PDF plot for holo structure will be based on:")
        print("1) Ligand fit by protein")
        print("2) Ligand fit by ligand")
        print("3) Bound protein's backbone")
        user_choice = int(input("Enter the corresponding number: "))
        
        # Define the variable based on user's choice
        if user_choice == 1:
            search_term = 'FitBy = "(protein)"'
        elif user_choice == 2:
            search_term = 'ASL = "at.n'
        elif user_choice == 3:
            search_term = 'ASL = "(((protein) and backbone) and not (atom.ele H)'

        with open(file_path, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(lines):
                if search_term in line:
                    # Find the line with RMSD values after the selected term
                    for j in range(i+1, min(i+5, len(lines))):  # Search within the next 5 lines
                        if "Result =" in lines[j]:
                            try:
                                rmsd_values = [float(val) for val in lines[j].split("[")[1].split("]")[0].split()]
                                return rmsd_values
                            except (IndexError, ValueError):
                                return None
            return None
    else:
        return None
  
def plot_pdf(rmsd_values_list, structure_types, names):
    max_density = 0
    for rmsd_values in rmsd_values_list:
        kde = sns.kdeplot(rmsd_values, linewidth=2)
        max_density = max(max_density, max(kde.get_lines()[0].get_ydata()))
    # Calculate the number of ticks
    num_ticks = int(np.ceil(max_density * 10)) + 1
    # Plot each curve
    for rmsd_values, name in zip(rmsd_values_list, names):
        sns.kdeplot(rmsd_values, label=name, linewidth=2)
    # Format x-axis ticks
    plt.xlabel('RMSD (Angstrom)')
    max_rmsd = max(max(sublist) for sublist in rmsd_values_list)
    plt.xticks(np.arange(0, int(max_rmsd) + 2, 1))
    # Format y-axis ticks
    plt.ylabel('Probability Density')
    plt.yticks(np.linspace(0, max_density, num_ticks), ['{:.2f}'.format(i) for i in np.linspace(0, max_density, num_ticks)])
    # Adjust legend colors
    handles, labels = plt.gca().get_legend_handles_labels()
    for handle in handles:
        handle.set_color(handle.get_color())  # Match legend colors with curve colors
    plt.legend(handles=handles, labels=names)
    plt.show()
    
def calculate_metrics(rmsd_values):
    if rmsd_values:
        metrics = {
            "Average": np.mean(rmsd_values),
            "Median": np.median(rmsd_values),
            "Standard Deviation": np.std(rmsd_values),
            "Minimum Value": np.min(rmsd_values),
            "Maximum Value": np.max(rmsd_values)
        }
        return metrics
    else:
        return None
        
def write_metrics_to_file(metrics, name):
    with open("metrics.txt", "a") as file:
        file.write(f"Metrics for {name}:\n")
        for key, value in metrics.items():
            file.write(f"{key}: {value}\n")
        file.write("\n")

def main():
    eaf_files = list_eaf_files()
    if not eaf_files:
        print("No .eaf files found in the directory.")
        return
    
    num_files = select_number_of_files()
    rmsd_values_list = []
    structure_types = []
    names = []
    
    for _ in range(num_files):
        selected_file = select_file(eaf_files)
        structure_type = select_structure_type()
        rmsd_values = extract_rmsd_values(selected_file, structure_type)
        if rmsd_values:
            rmsd_values_list.append(rmsd_values)
            structure_types.append(structure_type)
            name = input("\nSelect a name for your plot: ")
            names.append(name)
            
            metrics = calculate_metrics(rmsd_values)
            if metrics:
                write_metrics_to_file(metrics, name)
        else:
            print(f"Failed to extract RMSD values from {selected_file}. Skipping...")
    
    if rmsd_values_list:
        plot_pdf(rmsd_values_list, structure_types, names)
    else:
        print("No valid RMSD values extracted. Exiting...")

if __name__ == "__main__":
    main()
    
print(f"\nThank you byebye!\n")
