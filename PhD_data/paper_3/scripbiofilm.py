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

filename = '/home/m/Data_analytics/PhD_data/paper_3/Anti-biofilm_.ods'
print("Attempting to open file:", filename)

# Extract data from both sheets
ecoli_data = extract_data(filename, 0)
other_data = extract_data(filename, 1)

# Print raw extracted data
print("\nRaw extracted data for E. coli:")
print(ecoli_data)
print("\nRaw extracted data for S. aureus and C. albicans:")
print(other_data)

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

# Print statistics for all organisms
print("\nStatistics for E. coli:")
print(statistics['E. coli'])
print("\nStatistics for S. aureus:")
print(statistics['S. aureus'])
print("\nStatistics for C. albicans:")
print(statistics['C. albicans'])

# Create figure
fig = plt.figure(figsize=(20, 20))
fig.suptitle('', fontsize=16)

# Create GridSpec
gs = GridSpec(2, 2, figure=fig, height_ratios=[1, 1], hspace=0.6, wspace=0.3)

# Create subplots
axes = [fig.add_subplot(gs[0, 0]),
        fig.add_subplot(gs[0, 1]),
        fig.add_subplot(gs[1, 0])]

for ax, (organism, stats) in zip(axes, statistics.items()):
    bars = ax.bar(stats.index, stats['mean'], yerr=stats['sem'], capsize=5)
    
    # Set title in italic and left-aligned
    ax.set_title(f'$\it{{{organism}}}$', fontsize=14, loc='left')
    
    ax.set_xlabel('Composition', fontsize=12)
    ax.set_ylabel('Inhibition (%)', fontsize=12)
    
    # Adjust y-axis to show negative values
    y_min = min(0, stats['mean'].min() - stats['sem'].max())  # Lower bound
    y_max = max(0, stats['mean'].max() + stats['sem'].max())  # Upper bound
    ax.set_ylim(y_min * 1.2, y_max * 1.2)  # Add 20% padding
    
    ax.tick_params(axis='x', rotation=45)
    
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%', ha='center', va='bottom' if height >= 0 else 'top')
    
    ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

plt.tight_layout()
plt.show()

print("\nThe subplots have been displayed.")
