import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats

# Function to generate random data matching mean and std
def generate_data(mean, std, n=10):
    return np.random.normal(mean, std, n)

# Function to add SEM error bars
def add_sem_error_bars(ax, data, x, y, color='black'):
    for i, group in enumerate(data[x].unique()):
        group_data = data[data[x] == group][y]
        sem = stats.sem(group_data)
        mean = group_data.mean()
        ax.vlines(i, mean-sem, mean+sem, color=color, linewidth=2)
        ax.hlines([mean-sem, mean+sem], i-0.1, i+0.1, color=color, linewidth=2)

# Create long-format DataFrame for seaborn
data_long = []
for sample in ['BNC', 'BPHB2', 'BPHB5', 'BPHB10']:
    if sample == 'BNC':
        E_data = generate_data(1703.5, 221.5)
        UTS_data = generate_data(27.9, 9.5)
        εUTS_data = generate_data(8.8, 3.8)
        σB_data = generate_data(27.8, 9.6)
        εB_data = generate_data(9.0, 3.7)
    elif sample == 'BPHB2':
        E_data = generate_data(491.7, 54.1)
        UTS_data = generate_data(9.1, 0.1)
        εUTS_data = generate_data(9.0, 5.8)
        σB_data = generate_data(5.8, 3.9)
        εB_data = generate_data(10.3, 7.3)
    elif sample == 'BPHB5':
        E_data = generate_data(1173.7, 11.4)
        UTS_data = generate_data(15.5, 3.6)
        εUTS_data = generate_data(3.6, 0.9)
        σB_data = generate_data(15.5, 3.6)
        εB_data = generate_data(3.7, 0.8)
    else:  # BPHB10
        E_data = generate_data(657.4, 126.5)
        UTS_data = generate_data(6.9, 1.7)
        εUTS_data = generate_data(3.3, 0.6)
        σB_data = generate_data(6.7, 1.5)
        εB_data = generate_data(3.5, 0.5)
    
    for E, UTS, εUTS, σB, εB in zip(E_data, UTS_data, εUTS_data, σB_data, εB_data):
        data_long.append({
            'Sample': sample,
            'Value': E,
            'Measurement': 'Young\'s modulus at 0.2% (E) [MPa]'
        })
        data_long.append({
            'Sample': sample,
            'Value': UTS,
            'Measurement': 'Ultimate tensile strength (UTS) [MPa]'
        })
        data_long.append({
            'Sample': sample,
            'Value': εUTS,
            'Measurement': 'Strain at UTS (εUTS) [%]'
        })
        data_long.append({
            'Sample': sample,
            'Value': σB,
            'Measurement': 'Stress at break (σB) [MPa]'
        })
        data_long.append({
            'Sample': sample,
            'Value': εB,
            'Measurement': 'Strain at break (εB) [%]'
        })

df_long = pd.DataFrame(data_long)

# Create subplots
fig, axes = plt.subplots(2, 3, figsize=(15, 10))
axes = axes.flatten()

# Colors for the boxes
colors = ['#2ecc71', '#3498db', '#e74c3c', '#f1c40f']

# Plot each measurement
measurements = [
    'Young\'s modulus at 0.2% (E) [MPa]',
    'Ultimate tensile strength (UTS) [MPa]',
    'Strain at UTS (εUTS) [%]',
    'Stress at break (σB) [MPa]',
    'Strain at break (εB) [%]'
]

for idx, measurement in enumerate(measurements):
    data_subset = df_long[df_long['Measurement'] == measurement]
    
    # Create boxplot
    sns.boxplot(
        data=data_subset,
        x='Sample',
        y='Value',
        ax=axes[idx],
        palette=colors,
        width=0.7,
        showfliers=False
    )
    
    # Add SEM error bars
    add_sem_error_bars(axes[idx], data_subset, 'Sample', 'Value')
    
    # Customize each subplot
    axes[idx].set_title(measurement, pad=10)
    axes[idx].tick_params(axis='x', rotation=45)
    axes[idx].grid(True, axis='y', linestyle='--', alpha=0.7)
    
    # Set y-label to just the units
    axes[idx].set_ylabel(measurement.split('[')[1].strip(']'))
    axes[idx].set_xlabel('')

    # Add legend for SEM to each plot
    axes[idx].plot([], [], color='black', linewidth=2, label='SEM')
    axes[idx].legend()

# Remove the empty subplot
axes[-1].remove()

# Adjust layout
plt.tight_layout()

# Add a common x-label at the bottom
fig.text(0.5, 0.02, 'Sample Type', ha='center', va='center')

# Add an overall title
fig.suptitle('Mechanical Properties of Different Samples', y=1.02, fontsize=14)

plt.show() 