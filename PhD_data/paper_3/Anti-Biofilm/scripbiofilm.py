import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

print("Current working directory:", os.getcwd())

def extract_data(filename, sheet_name):
    df = pd.read_excel(filename, engine='odf', sheet_name=sheet_name, header=None)
    data = df.iloc[26:32, 2:14].reset_index(drop=True)
    data.index = [chr(65 + i) for i in range(6)]  # A to F
    data.columns = [str(i) for i in range(1, 13)]
    return data

def calculate_biofilm_inhibition(df, control_column, discard_cells=None):
    processed_df = df.loc['A':'F', :].apply(pd.to_numeric, errors='coerce')
    
    if discard_cells:
        for cell in discard_cells:
            processed_df.loc[cell[0], cell[1]] = np.nan
    
    control_od = processed_df[control_column].mean()
    
    for col in processed_df.columns:
        if col != control_column:
            processed_df[col] = ((control_od - processed_df[col]) / control_od) * 100
    
    processed_df = processed_df.drop(columns=[control_column])  # Remove control column
    return processed_df

def remove_outliers(df):
    Q1 = df.quantile(0.25)
    Q3 = df.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df >= lower_bound) & (df <= upper_bound)]

def create_box_visualization(statistics):
    # Prepare data for box plots
    all_data = []
    labels = []
    positions = []
    no_activity_positions = []
    no_activity_labels = []
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Different color for each organism
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Process data for each organism
    current_pos = 0
    for org_idx, (organism, stats) in enumerate(statistics.items()):
        # Skip S. aureus
        if organism == 'S. aureus':
            continue
            
        for comp_idx, composition in enumerate(stats.index):
            # Get raw data for this composition
            if organism == 'E. coli':
                data = ecoli_inhibition.loc[:, composition]
            else:  # C. albicans
                data = calbicans_inhibition.loc[:, composition]
            
            # Format label with italic strain name
            formatted_label = f"{composition}\n($\mathit{{{organism}}}$)"
            
            # Special case for C. albicans BPHB5%
            if organism == 'C. albicans' and composition == 'BPHB5%':
                all_data.append(data)
                labels.append(formatted_label)
                positions.append(current_pos)
            else:
                # Check if any value is negative for other cases
                if (data <= 0).any():
                    no_activity_positions.append(current_pos)
                    no_activity_labels.append(formatted_label)
                else:
                    # Only include data if all values are positive
                    all_data.append(data)
                    labels.append(formatted_label)
                    positions.append(current_pos)
            
            current_pos += 1
        
        # Add space between organisms
        current_pos += 1
    
    # Create box plot without outliers
    if all_data:  # Only create if there's data to plot
        bp = ax.boxplot(all_data, positions=positions, patch_artist=True, showfliers=False)
        
        # Customize box plots and make lines thicker
        for element in ['boxes', 'whiskers', 'fliers', 'means', 'medians', 'caps']:
            plt.setp(bp[element], linewidth=2)
            
        for patch in bp['boxes']:
            patch.set_facecolor('white')
            patch.set_alpha(0.7)
    
    # Set all x-tick positions
    all_positions = sorted(positions + no_activity_positions)
    
    # Create list of labels and their colors
    all_labels = []
    label_colors = []
    for pos in all_positions:
        if pos in positions:
            idx = positions.index(pos)
            all_labels.append(labels[idx])
            label_colors.append('black')
        else:
            idx = no_activity_positions.index(pos)
            all_labels.append(no_activity_labels[idx])
            label_colors.append('red')
    
    # Customize plot
    ax.set_xticks(all_positions)
    # Set labels with their respective colors and larger font size
    ax.set_xticklabels(all_labels, rotation=45, ha='right', fontsize=18)
    for tick, color in zip(ax.get_xticklabels(), label_colors):
        tick.set_color(color)
        tick.set_fontsize(14)  # Explicitly set font size for each label
    
    ax.set_ylabel('Inhibition (%)', fontsize=22)
    ax.set_title('Biofilm Inhibition Activity', fontsize=22)
    
    # Make axis lines thicker
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)
    ax.spines['top'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    
    # Increase tick label size and thickness
    ax.tick_params(axis='both', which='major', labelsize=14, width=2)
    
    # Set y-axis to start from 0
    ymin, ymax = ax.get_ylim()
    ax.set_ylim(bottom=0, top=ymax)
    
    # Add grid for better readability with thicker lines
    ax.yaxis.grid(True, linestyle='--', alpha=0.7, linewidth=1.5)
    
    # Add zero line with increased thickness
    ax.axhline(y=0, color='black', linestyle='-', linewidth=2)
    
    plt.tight_layout()
    plt.show()

filename = os.path.join(os.getcwd(), 'PhD_data', 'paper_3', 'Anti-biofilm_.ods')
print("Attempting to open file:", filename)

# Extract data from both sheets
ecoli_data = extract_data(filename, 0)
other_data = extract_data(filename, 1)

# Calculate biofilm inhibition for each organism
ecoli_inhibition = calculate_biofilm_inhibition(ecoli_data.iloc[:, :6], '5')
saureus_inhibition = calculate_biofilm_inhibition(other_data.iloc[:, :6], '5', discard_cells=[('A', '2'), ('B', '2'), ('C', '2')])
calbicans_inhibition = calculate_biofilm_inhibition(other_data.iloc[:, 6:], '11')

# Rename columns
new_column_names = {
    '1': 'BNC', '2': 'BPHB2%', '3': 'BPHB5%',
    '4': 'BPHB10%', '6': 'PHB',
    '7': 'BNC', '8': 'BPHB2%', '9': 'BPHB5%',
    '10': 'BPHB10%', '12': 'PHB'
}

ecoli_inhibition.rename(columns=new_column_names, inplace=True)
saureus_inhibition.rename(columns=new_column_names, inplace=True)
calbicans_inhibition.rename(columns=new_column_names, inplace=True)

# Calculate statistics
def calculate_statistics(df):
    df_no_outliers = remove_outliers(df)
    return df_no_outliers.agg(['mean', 'std', 'sem']).T

statistics = {
    'E. coli': calculate_statistics(ecoli_inhibition),
    'S. aureus': calculate_statistics(saureus_inhibition),
    'C. albicans': calculate_statistics(calbicans_inhibition)
}

# Only show the box plot visualization
print("\nGenerating box plot visualization...")
create_box_visualization(statistics)
