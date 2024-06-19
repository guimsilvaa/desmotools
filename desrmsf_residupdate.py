import os
import re

def list_eaf_files():
    return [f for f in os.listdir() if f.endswith('.eaf')]

def read_eaf_file(filename):
    with open(filename, 'r') as file:
        return file.readlines()

def write_eaf_file(filename, lines):
    with open(filename, 'w') as file:
        file.writelines(lines)

def update_protein_residues(lines, start_number):
    pattern = re.compile(r'("A:[A-Z]{3}_)(\d+)(")')
    for i, line in enumerate(lines):
        if "ProteinResidues" in line:
            new_residues = []
            matches = pattern.findall(line)
            if matches:
                new_start = start_number
                new_line = line
                for match in matches:
                    original = f'{match[0]}{match[1]}{match[2]}'
                    replacement = f'{match[0]}{new_start}{match[2]}'
                    new_line = new_line.replace(original, replacement, 1)
                    new_start += 1
                lines[i] = new_line
    return lines

def main():
    eaf_files = list_eaf_files()
    if not eaf_files:
        print("No .eaf files found in the current directory.")
        return

    print("Available .eaf files:")
    for idx, filename in enumerate(eaf_files):
        print(f"{idx + 1}. {filename}")

    file_choice = int(input("Enter the number corresponding to the desired file: ")) - 1
    if file_choice < 0 or file_choice >= len(eaf_files):
        print("Invalid choice.")
        return

    selected_file = eaf_files[file_choice]
    lines = read_eaf_file(selected_file)
    
    print("Current ProteinResidues lines:")
    for line in lines:
        if "ProteinResidues" in line:
            print(line.strip())

    start_number = int(input("Enter the starting number for the sequence: "))

    updated_lines = update_protein_residues(lines, start_number)
    new_filename = selected_file.replace('.eaf', '_updt.eaf')
    write_eaf_file(new_filename, updated_lines)

    print(f"Updated file saved as {new_filename} with new sequence starting from {start_number}.")

if __name__ == "__main__":
    main()

