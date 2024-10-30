import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats
import pandas as pd

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

# Create a figure with two subplots
plt.figure(figsize=(15, 10))

# 1. Distribution plot
plt.subplot(2, 1, 1)
sns.kdeplot(data=df, x='Halo', hue='Bacteria', fill=True, common_norm=False)
plt.xlabel('Inhibition Halo (mm)')
plt.ylabel('Density')
plt.title('Distribution of Inhibition Halos by Bacteria')
plt.grid(True, linestyle='--', alpha=0.7)

# 2. Heatmap
plt.subplot(2, 1, 2)
# Create matrix for heatmap
heatmap_data = pd.DataFrame({
    'E. coli': [np.mean(oils_data[oil]['E_coli']) for oil in oils_data],
    'S. aureus': [np.mean(oils_data[oil]['S_aureus']) for oil in oils_data]
}, index=oils_data.keys())

# Create regular heatmap
sns.heatmap(heatmap_data, 
            annot=True,
            fmt='.2f',
            cmap='YlOrRd',
            cbar_kws={'label': 'Inhibition Halo (mm)'},
            center=np.mean(df['Halo']))

plt.title('Heatmap of Mean Inhibition Halos', pad=20)
plt.tight_layout()
plt.show()

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

# Create visualizations
plt.figure(figsize=(15, 10))

# 1. Bar plot with error bars
plt.subplot(2, 1, 1)
x = np.arange(len(oils_data))
width = 0.35

e_coli_means = [means[oil]['E_coli'] for oil in oils_data]
s_aureus_means = [means[oil]['S_aureus'] for oil in oils_data]
e_coli_std = [std_devs[oil]['E_coli'] for oil in oils_data]
s_aureus_std = [std_devs[oil]['S_aureus'] for oil in oils_data]

plt.bar(x - width/2, e_coli_means, width, label='E. coli', 
        yerr=e_coli_std, capsize=5, color='skyblue')
plt.bar(x + width/2, s_aureus_means, width, label='S. aureus', 
        yerr=s_aureus_std, capsize=5, color='lightcoral')

plt.xlabel('Essential Oils')
plt.ylabel('Inhibition Halo (mm)')
plt.title('Inhibition Halos by Essential Oil and Bacteria')
plt.xticks(x, list(oils_data.keys()))
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)

# 2. Box plot
plt.subplot(2, 1, 2)
sns.boxplot(data=df, x='Oil', y='Halo', hue='Bacteria', 
            palette={'E. coli': 'skyblue', 'S. aureus': 'lightcoral'})
plt.xlabel('Essential Oils')
plt.ylabel('Inhibition Halo (mm)')
plt.title('Distribution of Inhibition Halos')
plt.grid(True, linestyle='--', alpha=0.7)

plt.tight_layout()
plt.show()

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

# Create figure with two subplots
plt.figure(figsize=(15, 10))

# 1. Box plot
plt.subplot(2, 1, 1)
# Create box plot
ax = sns.boxplot(data=df, x='Oil', y='Halo', hue='Bacteria', 
                 palette={r'$\it{E. coli}$': 'lightgray', r'$\it{S. aureus}$': 'lightgray'})

# Highlight Cinnamon boxes
cin_data = df[df['Oil'] == 'Cin']
sns.boxplot(data=cin_data, x='Oil', y='Halo', hue='Bacteria',
            palette={r'$\it{E. coli}$': 'skyblue', r'$\it{S. aureus}$': 'lightcoral'})

plt.xlabel('Essential Oils')
plt.ylabel('Inhibition Halo (mm)')
plt.title('A', pad=20, loc='left')
plt.grid(True, linestyle='--', alpha=0.7)
plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left')

# 2. Heatmap
plt.subplot(2, 1, 2)
# Create matrix for heatmap
heatmap_data = pd.DataFrame({
    r'$\it{E. coli}$': [np.mean(oils_data[oil]['E_coli']) for oil in oils_data],
    r'$\it{S. aureus}$': [np.mean(oils_data[oil]['S_aureus']) for oil in oils_data]
}, index=oils_data.keys())

# Create regular heatmap
sns.heatmap(heatmap_data, 
            annot=True,
            fmt='.2f',
            cmap='YlOrRd',
            cbar_kws={'label': 'Inhibition Halo (mm)'},
            center=np.mean(df['Halo']))

plt.title('B', pad=20, loc='left')
plt.tight_layout()
plt.show()


