import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats
import pandas as pd

# Set global font sizes - reduced sizes
plt.rcParams.update({
    'font.size': 10,          # Reduced from 14
    'axes.titlesize': 12,     # Reduced from 16
    'axes.labelsize': 10,     # Reduced from 14
    'xtick.labelsize': 8,     # Reduced from 12
    'ytick.labelsize': 8,     # Reduced from 12
    'legend.fontsize': 8,     # Reduced from 12
    'figure.titlesize': 12    # Reduced from 16
})

# Essential oil names
essential_oils = ['Lem', 'Clo', 'Gin', 'Euc', 'Thy', 'Cin', 'IS'] 

# Data for Lemongrass (Lem) in triplicate
# Format: [E. coli data, S. aureus data]
lem_data = {
    'E_coli': [6.815, 6.835, 4.653],
    'S_aureus': [4.226, 3.057, 2.097]
}
# Data for Clove (Clo) in triplicate
clo_data = {
    'E_coli': [7.267, 7.267, 6.256],
    'S_aureus': [4.747, 4.689, 4.006]
}

# Data for Ginger (Gin) in triplicate 
gin_data = {
    'E_coli': [0, 0, 0],
    'S_aureus': [0, 0, 0]
}

# Data for Eucalyptus (Euc) in triplicate
euc_data = {
    'E_coli': [4.923, 3.816, 6.330], 
    'S_aureus': [4.923, 5.861, 8.440]
}

# Data for Thyme (Thy) in triplicate
thy_data = {
    'E_coli': [6.095, 6.330, 4.479],
    'S_aureus': [6.815, 3.357, 7.049]
}

# Data for Cinnamon (Cin) in triplicate
cin_data = {
    'E_coli': [7.033, 5.631, 5.315],
    'S_aureus': [12.193, 9.131, 10.552]
}

# Your data is already defined above
oils_data = {
    'Lem': lem_data,
    'Clo': clo_data,
    'Gin': gin_data,
    'Euc': euc_data,
    'Thy': thy_data,
    'Cin': cin_data
}

# Calculate means and standard deviations
means = {oil: {
    'E_coli': np.mean(data['E_coli']),
    'S_aureus': np.mean(data['S_aureus'])
} for oil, data in oils_data.items()}

std_devs = {oil: {
    'E_coli': np.std(data['E_coli'], ddof=1),
    'S_aureus': np.std(data['S_aureus'], ddof=1)
} for oil, data in oils_data.items()}

# Create DataFrame for plotting
df = pd.DataFrame([
    {'Oil': oil, 'Bacteria': 'E. coli', 'Halo': value}
    for oil, data in oils_data.items()
    for value in data['E_coli']
] + [
    {'Oil': oil, 'Bacteria': 'S. aureus', 'Halo': value}
    for oil, data in oils_data.items()
    for value in data['S_aureus']
])
# Print statistical summary
print("\nStatistical Analysis (E. coli vs S. aureus for each oil):")
for oil in oils_data:
    t_stat, p_val = stats.ttest_ind(
        oils_data[oil]['E_coli'],
        oils_data[oil]['S_aureus']
    )
    print(f"\n{oil}:")
    print(f"t-statistic: {t_stat:.4f}")
    print(f"p-value: {p_val:.4f}")

# Print means and standard deviations
print("\nMeans and Standard Deviations:")
for oil in oils_data:
    print(f"\n{oil}:")
    print(f"E. coli: {means[oil]['E_coli']:.2f} ± {std_devs[oil]['E_coli']:.2f} mm")
    print(f"S. aureus: {means[oil]['S_aureus']:.2f} ± {std_devs[oil]['S_aureus']:.2f} mm")

# Create heatmap data before the plotting section
heatmap_data = pd.DataFrame({
    r'$\it{E. coli}$': [means[oil]['E_coli'] for oil in essential_oils[:-1]],  # Excluding 'IS'
    r'$\it{S. aureus}$': [means[oil]['S_aureus'] for oil in essential_oils[:-1]]  # Excluding 'IS'
}, index=essential_oils[:-1])

# Create DataFrame for box plot
df = pd.DataFrame([
    {'Oil': oil, 'Bacteria': r'$\it{E. coli}$', 'Halo': value}
    for oil, data in oils_data.items()
    for value in data['E_coli']
] + [
    {'Oil': oil, 'Bacteria': r'$\it{S. aureus}$', 'Halo': value}
    for oil, data in oils_data.items()
    for value in data['S_aureus']
])

# Create figure with publication-standard size and resolution
plt.figure(figsize=(6, 5))

# 1. Box plot
plt.subplot(2, 1, 1)

# Combine all data for the box plot
sns.boxplot(data=df, x='Oil', y='Halo', hue='Bacteria', 
            palette={r'$\it{E. coli}$': 'lightgray', 
                     r'$\it{S. aureus}$': 'lightgray',
                     r'$\it{E. coli}$ (Selected)': 'skyblue', 
                     r'$\it{S. aureus}$ (Selected)': 'lightcoral'},
            width=0.7,    # Standard width
            linewidth=1)  # Clear lines

# Add grid
plt.grid(True, axis='y', linestyle='--', alpha=0.7)

# Clear existing legend and add custom legend for highlighted Cinnamon boxes
plt.legend().remove()  # Remove the existing legend

# Create a custom legend for the highlighted boxes
plt.legend(title=None, bbox_to_anchor=(1.05, 0.5),  # Adjusted position
           loc='center left', fontsize=12, 
           handletextpad=0.5,
           handlelength=1.5,
           labels=[r'$\it{E. coli}$', r'$\it{S. aureus}$', 
                   r'$\it{E. coli}$ (Selected)', r'$\it{S. aureus}$ (Selected)'],  
           handles=[plt.Line2D([0], [0], color='lightgray', lw=4),  
                    plt.Line2D([0], [0], color='lightgray', lw=4),  
                    plt.Line2D([0], [0], color='skyblue', lw=4),  
                    plt.Line2D([0], [0], color='lightcoral', lw=4)])  

plt.xlabel('Essential Oils', fontsize=16)
plt.ylabel('Inhibition Zone (mm)', fontsize=16)
plt.title('A', pad=5, loc='left', fontsize=16)
plt.xticks(fontsize=14)
plt.yticks(fontsize=14)

# 2. Heatmap (ensure this is below the box plot)
plt.subplot(2, 1, 2)
hm = sns.heatmap(heatmap_data, 
            annot=True,
            fmt='.1f',
            cmap='YlOrRd',
            cbar_kws={'label': 'Inhibition Zone (mm)'},
            center=np.mean(df['Halo']),
            annot_kws={'size': 16})

plt.title('B', pad=5, loc='left', fontsize=16)
plt.xticks(fontsize=16)
plt.yticks(fontsize=16, rotation=0)

# Adjust colorbar label and tick label sizes
cbar = hm.collections[0].colorbar
cbar.ax.tick_params(labelsize=16)  
plt.gcf().axes[-1].yaxis.label.set_size(16)

# Save with publication-quality settings
plt.show()


