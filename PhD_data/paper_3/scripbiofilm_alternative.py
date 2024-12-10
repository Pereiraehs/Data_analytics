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

filename = os.path.join(os.getcwd(), 'PhD_data', 'paper_3', 'Anti-biofilm_.ods')
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

# Filter organisms with positive results
positive_results = {}
for organism, stats in statistics.items():
    stats_positive = stats[stats['mean'] > 0]
    if not stats_positive.empty:
        positive_results[organism] = stats_positive

if positive_results:  # Only create figure if there are positive results
    # Create figure with appropriate size based on number of plots
    n_plots = len(positive_results)
    fig = plt.figure(figsize=(10 * min(2, n_plots), 10 * ((n_plots + 1) // 2)))
    
    # Create GridSpec
    rows = (n_plots + 1) // 2  # Calculate needed rows
    gs = GridSpec(rows, min(2, n_plots), figure=fig, height_ratios=[1] * rows, hspace=0.6, wspace=0.3)
    
    # Create and populate subplots
    for idx, (organism, stats_positive) in enumerate(positive_results.items()):
        row = idx // 2
        col = idx % 2
        ax = fig.add_subplot(gs[row, col])
        
        bars = ax.bar(stats_positive.index, stats_positive['mean'], 
                      yerr=stats_positive['sem'], capsize=5)
        
        ax.set_title(fr'$\mathit{{{organism}}}$', fontsize=14, loc='left')
        ax.set_xlabel('Composition', fontsize=12)
        ax.set_ylabel('Inhibition (%)', fontsize=12)
        
        # Set y-axis to start from 0
        y_max = stats_positive['mean'].max() + stats_positive['sem'].max()
        ax.set_ylim(0, y_max * 1.2)  # Add 20% padding
        
        ax.tick_params(axis='x', rotation=45)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{height:.1f}%', ha='center', va='bottom')
        
        ax.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    
    plt.tight_layout()
    plt.show()
    print("\nThe subplots have been displayed.")
else:
    print("\nNo positive results to display.")

# Add this new visualization function
def create_combined_visualization(statistics):
    # Prepare data for visualization
    organisms = list(statistics.keys())
    compositions = list(statistics[organisms[0]].index)
    
    # Create matrices for mean values and standard errors
    means = np.zeros((len(organisms), len(compositions)))
    sems = np.zeros((len(organisms), len(compositions)))
    
    for i, org in enumerate(organisms):
        means[i,:] = statistics[org]['mean']
        sems[i,:] = statistics[org]['sem']
    
    # Create figure
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create heatmap
    im = ax.imshow(means, cmap='RdYlBu_r', aspect='auto')
    
    # Add bubbles for significant positive values
    for i in range(len(organisms)):
        for j in range(len(compositions)):
            value = means[i,j]
            if value > 0:  # Only show positive values
                size = value * 50  # Scale bubble size based on value
                ax.scatter(j, i, s=size, color='black', alpha=0.3)
                # Add text annotation
                ax.text(j, i, f'{value:.1f}±{sems[i,j]:.1f}%', 
                       ha='center', va='center', fontsize=8)
    
    # Customize axes
    ax.set_xticks(np.arange(len(compositions)))
    ax.set_yticks(np.arange(len(organisms)))
    ax.set_xticklabels(compositions, rotation=45, ha='right')
    ax.set_yticklabels([fr'$\mathit{{{org}}}$' for org in organisms])
    
    # Add colorbar
    cbar = plt.colorbar(im)
    cbar.set_label('Inhibition (%)', rotation=270, labelpad=15)
    
    # Add grid to better separate the cells
    ax.set_xticks(np.arange(-.5, len(compositions), 1), minor=True)
    ax.set_yticks(np.arange(-.5, len(organisms), 1), minor=True)
    ax.grid(which='minor', color='black', linestyle='-', linewidth=1)
    
    plt.title('Biofilm Inhibition Activity', pad=20)
    plt.tight_layout()
    plt.show()

# Add this after your existing plotting code
print("\nGenerating alternative visualization...")
create_combined_visualization(statistics)
