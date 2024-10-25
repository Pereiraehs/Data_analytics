import pandas as pd
import numpy as np
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test
import matplotlib.pyplot as plt

# Load the data
data = {
    'time': [0, 24, 48, 72] * 27,  # 9 groups * 3 replicates
    'dead': [
        # Group 1
        11, 8, 13,    # 0h
        13, 12, 15,   # 24h
        28, 24, 29,   # 48h
        41, 43, 43,   # 72h
        # Group 2
        7, 3, 4,      # 0h
        15, 17, 17,   # 24h
        20, 20, 22,   # 48h
        30, 32, 32,   # 72h
        # Group 3
        5, 7, 5,      # 0h (placeholder data)
        15, 17, 24,      # 24h (placeholder data)
        27, 28, 28,      # 48h (placeholder data)
        38, 27, 34,      # 72h (placeholder data)
        # Group 4
        10, 6, 5,      # 0h (placeholder data)
        25, 16, 18,      # 24h (placeholder data)
        31, 38, 28,      # 48h (placeholder data)
        42, 38, 29,      # 72h (placeholder data)
        # Group 5
        7, 7, 6,      # 0h (placeholder data)
        16, 22, 10,      # 24h (placeholder data)
        24, 26, 26,      # 48h (placeholder data)
        30, 42, 40,      # 72h (placeholder data)
        # Group 6
        4, 12, 7,      # 0h (placeholder data)
        22, 18, 29,      # 24h (placeholder data)
        36, 45, 46,      # 48h (placeholder data)
        30, 49, 40,      # 72h (placeholder data)
        # Group 7
        37, 55, 82,      # 0h (placeholder data)
        40, 56, 80,      # 24h (placeholder data)
        45, 56, 82,      # 48h (placeholder data)
        45, 56, 82,      # 72h (placeholder data)
        # Group 8
        20, 12, 29,      # 0h (placeholder data)
        36, 40, 30,      # 24h (placeholder data)
        54, 46, 45,      # 48h (placeholder data)
        54, 48, 52,      # 72h (placeholder data)
        # Group 9
        17, 15, 24,      # 0h (placeholder data)
        31, 26, 46,      # 24h (placeholder data)
        48, 39, 48,      # 48h (placeholder data)
        61, 48, 66,      # 72h (placeholder data)
    ],
    'total': [
        # Group 1
        60, 49, 49,   # 0h
        60, 49, 49,   # 24h
        60, 49, 49,   # 48h
        60, 49, 49,   # 72h
        # Group 2
        49, 45, 56,   # 0h
        49, 45, 56,   # 24h
        49, 45, 56,   # 48h
        49, 45, 56,   # 72h
        # Group 3
        42, 40, 31,   # 0h (placeholder data)
        42, 40, 31,   # 24h (placeholder data)
        42, 40, 31,   # 48h (placeholder data)
        42, 40, 31,   # 72h (placeholder data)
        # Group 4
        47, 41, 34,   # 0h (placeholder data)
        47, 41, 34,   # 24h (placeholder data)
        47, 41, 34,   # 48h (placeholder data)
        47, 41, 34,   # 72h (placeholder data)
        # Group 5
        34, 47, 46,   # 0h (placeholder data)
        34, 47, 46,   # 24h (placeholder data)
        34, 47, 46,   # 48h (placeholder data)
        34, 47, 46,   # 72h (placeholder data)
        # Group 6
        41, 58, 50,   # 0h (placeholder data)
        41, 58, 50,   # 24h (placeholder data)
        41, 58, 50,   # 48h (placeholder data)
        41, 58, 50,   # 72h (placeholder data)
        # Group 7
        45, 56, 82,   # 0h (placeholder data)
        45, 56, 82,   # 24h (placeholder data)
        45, 56, 82,   # 48h (placeholder data)
        45, 56, 82,   # 72h (placeholder data)
        # Group 8
        54, 50, 52,   # 0h (placeholder data)
        54, 50, 52,   # 24h (placeholder data)
        54, 50, 52,   # 48h (placeholder data)
        54, 50, 52,   # 72h (placeholder data)
        # Group 9
        64, 49, 66,   # 0h (placeholder data)
        64, 49, 66,   # 24h (placeholder data)
        64, 49, 66,   # 48h (placeholder data)
        64, 49, 66,   # 72h (placeholder data)
    ],
    'group': ['Control'] * 12 + ['BNC'] * 12 + ['BPHB2%'] * 12 + ['BPHB5%'] * 12 + ['BPHB10%'] * 12 + ['PHB'] * 12 + ['EoC'] * 12 + ['EoD1'] * 12 + ['EoD2'] * 12
}

df = pd.DataFrame(data)

# Calculate the number of censored (survived) worms at each time point
df['censored'] = df['total'] - df['dead']

# Create a single figure with two subplots stacked vertically
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 16))

# Define colors for each group
colors = ['blue', 'red', 'green', 'orange', 'purple', 'pink', 'brown', 'gray', 'cyan']

# Perform Kaplan-Meier analysis and log-rank tests
significant_groups = set()
groups = df['group'].unique()
control_group = 'Control'  # Set the control group
for group in groups:
    if group != control_group:
        group_data = df[df['group'] == group]
        control_data = df[df['group'] == control_group]
        
        T1 = np.repeat(group_data['time'].values, group_data['dead'].values)
        E1 = np.ones_like(T1)
        T2 = np.repeat(control_data['time'].values, control_data['dead'].values)
        E2 = np.ones_like(T2)
        
        result = logrank_test(T1, T2, E1, E2)
        if result.p_value < 0.05:
            significant_groups.add(group)
        print(f"Log-rank test {group} vs {control_group}: p-value = {result.p_value:.4f}")

# Plot Kaplan-Meier curves
for i, group in enumerate(groups):
    group_data = df[df['group'] == group]
    
    kmf_data = []
    kmf_observed = []
    for _, row in group_data.iterrows():
        kmf_data.extend([row['time']] * row['dead'] + [row['time']] * row['censored'])
        kmf_observed.extend([1] * row['dead'] + [0] * row['censored'])

    kmf = KaplanMeierFitter()
    kmf.fit(kmf_data, event_observed=kmf_observed, label=group)
    
    # Plot on the first subplot (all curves)
    kmf.plot(ax=ax1, ci_show=True, color=colors[i])
    
    # Plot on the second subplot (only significant curves and Control)
    if group in significant_groups or group == control_group:
        kmf.plot(ax=ax2, ci_show=True, color=colors[i])

# Function to format y-axis as percentage
def format_y_axis_as_percentage(ax):
    ax.set_ylim(0, 1)  # Ensure the y-axis goes from 0 to 1
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda y, _: '{:.0f}'.format(y*100)))
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1])  # Set ticks at 0, 25, 50, 75, 100

# Customize the first subplot (all curves)
ax1.set_title('A', loc='left', pad=10)
ax1.set_xlabel('Time (hours)')
ax1.set_ylabel('Survival Probability (%)')
ax1.grid(True)
ax1.legend(title='All Groups', loc='center left', bbox_to_anchor=(1, 0.5))
format_y_axis_as_percentage(ax1)

# Customize the second subplot (significant curves)
ax2.set_title('B', loc='left', pad=10)
ax2.set_xlabel('Time (hours)')
ax2.set_ylabel('Survival Probability (%)')
ax2.grid(True)
ax2.legend(title='Significant Groups*', loc='center left', bbox_to_anchor=(1, 0.5))
format_y_axis_as_percentage(ax2)

# Add a main title to the figure
fig.suptitle('', fontsize=16)

# Adjust the layout and show the plot
plt.tight_layout()
plt.subplots_adjust(top=0.95, right=0.85, hspace=0.3)  # Make room for the main title, legends, and space between subplots
plt.show()
