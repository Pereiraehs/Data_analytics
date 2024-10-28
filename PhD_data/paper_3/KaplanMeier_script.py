import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('c_elegans_data_template.csv', comment='#')

# Create a single figure with two subplots stacked vertically
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 16))

# Define colors for each group
colors = plt.cm.tab10(np.linspace(0, 1, len(df['Group'].unique())))

# Perform Kaplan-Meier analysis and log-rank tests
significant_groups = set()
groups = df['Group'].unique()
control_group = 'Control'  # Assuming 'Control' is the reference group
for group in groups:
    if group != control_group:
        group_data = df[df['Group'] == group]
        control_data = df[df['Group'] == control_group]
        
        T1 = np.repeat(group_data['Time'].values, group_data['Dead'].values)
        E1 = np.ones_like(T1)
        T2 = np.repeat(control_data['Time'].values, control_data['Dead'].values)
        E2 = np.ones_like(T2)
        
        result = logrank_test(T1, T2, E1, E2)
        if result.p_value < 0.05:
            significant_groups.add(group)
        print(f"Log-rank test {group} vs {control_group}: p-value = {result.p_value:.4f}")

# Plot Kaplan-Meier curves
for i, group in enumerate(groups):
    group_data = df[df['Group'] == group]
    
    kmf = KaplanMeierFitter()
    kmf.fit(group_data['Time'], group_data['Dead'], label=group)
    
    # Plot on the first subplot (all curves)
    kmf.plot(ax=ax1, ci_show=True, color=colors[i])
    
    # Plot on the second subplot (only significant curves and Control)
    if group in significant_groups or group == control_group:
        kmf.plot(ax=ax2, ci_show=True, color=colors[i])

# Customize the first subplot (all curves)
ax1.set_title('A', loc='left', pad=10)
ax1.set_xlabel('Time (hours)')
ax1.set_ylabel('Survival Probability')
ax1.grid(True)
ax1.legend(title='All Groups', loc='center left', bbox_to_anchor=(1, 0.5))

# Customize the second subplot (significant curves)
ax2.set_title('B', loc='left', pad=10)
ax2.set_xlabel('Time (hours)')
ax2.set_ylabel('Survival Probability')
ax2.grid(True)
ax2.legend(title='Sig* Groups (p < 0.05 vs Control)', loc='center left', bbox_to_anchor=(1, 0.5))

# Add a main title to the figure
fig.suptitle('Kaplan-Meier Survival Curves for C. elegans Groups', fontsize=16)

# Adjust the layout and show the plot
plt.tight_layout()
plt.subplots_adjust(top=0.95, right=0.85, hspace=0.3)  # Make room for the main title, legends, and space between subplots
plt.show()
