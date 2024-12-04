import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Create DataFrame
data = {
    'Sample': ['BNC', 'BPHB2', 'BPHB5', 'BPHB10'],
    'Young\'s modulus at 0.2% (E) [MPa]': [1703.5, 491.7, 1173.7, 657.4],
    'Ultimate tensile strength (UTS) [MPa]': [27.9, 9.1, 15.5, 6.9],
    'Strain at UTS (εUTS) [%]': [8.8, 9.0, 3.6, 3.3],
    'Stress at break (σB) [MPa]': [27.8, 5.8, 15.5, 6.7],
    'Strain at break (εB) [%]': [9.0, 10.3, 3.7, 3.5]
}

df = pd.DataFrame(data)

# Melt DataFrame to long format
df_melted = pd.melt(df, id_vars=['Sample'], var_name='Measurement', value_name='Value')

# Create grouped bar chart
plt.figure(figsize=(12, 6))
sns.barplot(data=df_melted, x='Sample', y='Value', hue='Measurement')

# Customize chart
plt.title('Mechanical Properties of Different Samples', pad=20)
plt.xlabel('Sample')
plt.ylabel('Value')
plt.xticks(rotation=45)
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')

# Adjust layout to prevent label cutoff
plt.tight_layout()

plt.show()
