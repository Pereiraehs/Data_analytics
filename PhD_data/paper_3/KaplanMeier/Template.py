import csv

# Define the structure of the CSV template
groups = ['Control', 'Group1', 'Group2', 'Group3', 'Group4', 'Group5', 'Group6', 'Group7', 'Group8']
time_points = [0, 24, 48, 72]
replicates = 3

# Create the CSV file
with open('c_elegans_data_template.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    
    # Write instructions as comments
    writer.writerow(['# Instructions:'])
    writer.writerow(['# 1. Open this CSV file in a spreadsheet program.'])
    writer.writerow(['# 2. For each group, time point, and replicate, fill in the "Dead" and "Total" columns.'])
    writer.writerow(['# 3. "Dead" represents the number of dead worms at that time point.'])
    writer.writerow(['# 4. "Total" represents the total number of worms at the start of the experiment for that replicate.'])
    writer.writerow(['# 5. Save the file after entering all your data.'])
    writer.writerow(['# 6. Use this filled CSV file as input for your Kaplan-Meier analysis script.'])
    writer.writerow([])  # Add an empty row for separation
    
    # Write the header
    header = ['Group', 'Time', 'Replicate', 'Dead', 'Total']
    writer.writerow(header)
    
    # Write the data rows
    for group in groups:
        for time in time_points:
            for replicate in range(1, replicates + 1):
                row = [group, time, f'Rep{replicate}', '', '']
                writer.writerow(row)

print("CSV template 'c_elegans_data_template.csv' has been created.")
print("The file includes instructions and is ready for data entry.")

# Print the instructions to the console as well
print("\nInstructions:")
print("1. Open the 'c_elegans_data_template.csv' file in a spreadsheet program.")
print("2. For each group, time point, and replicate, fill in the 'Dead' and 'Total' columns.")
print("3. 'Dead' represents the number of dead worms at that time point.")
print("4. 'Total' represents the total number of worms at the start of the experiment for that replicate.")
print("5. Save the file after entering all your data.")
print("6. Use this filled CSV file as input for your Kaplan-Meier analysis script.")
