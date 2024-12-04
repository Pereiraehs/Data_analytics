import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib

# Configurar o estilo
plt.style.use('classic')  # Usando estilo classic do matplotlib
sns.set_theme(style="whitegrid")  # Configuração do seaborn
sns.set_palette("husl")  # Paleta de cores mais distintas

# Remova ou comente a linha do matplotlib.use('Agg')
# matplotlib.use('Agg')  # Comente esta linha!

# Configuração para exibir o plot
plt.ion()  # Turn on interactive mode
# %matplotlib inline  # Descomente esta linha se estiver usando Jupyter notebook

# Seus dados originais
data = {
    'Cin_1': [0.156, 0.132, 0.093, 0.066, 0.059, 0.051, 0.569, 0.047],
    'Cin_2': [0.206, 0.231, 0.278, 0.086, 0.068, 0.277, 0.506, 0.046],
    'Euc_1': [0.050, 0.052, 0.048, 0.048, 0.516, 0.714, 0.919, 0.045],
    'Euc_2': [0.935, 0.052, 0.047, 0.049, 0.678, 0.830, 0.890, 0.046],
    'Thy_1': [0.064, 0.060, 0.050, 0.247, 0.632, 0.752, 0.851, 0.046],
    'Thy_2': [0.064, 0.058, 0.050, 0.251, 0.398, 0.642, 0.767, 0.047],
    'Lem_1': [0.197, 0.092, 0.058, 0.062, 0.339, 0.552, 0.785, 0.047],
    'Lem_2': [0.253, 0.083, 0.053, 0.061, 0.339, 0.565, 0.700, 0.047],
    'Clo_1': [0.096, 0.188, 0.236, 0.303, 0.444, 0.599, 0.713, 0.882],
    'Clo_2': [0.115, 0.187, 0.288, 0.361, 0.498, 0.553, 0.690, 0.922],
    'Gin_1': [0.061, 0.115, 0.072, 0.108, 0.057, 0.067, 0.077, 0.670],
    'Gin_2': [0.070, 0.117, 0.069, 0.081, 0.062, 0.055, 0.057, 0.773]
}

# Add new data dictionaries for S. aureus and C. albicans
data_saureus = {
    'Cin_1': [0.113, 0.148, 0.147, 0.091, 0.062, 0.066, 0.061, 0.047],
    'Cin_2': [0.132, 0.145, 0.154, 0.103, 0.067, 0.067, 0.054, 0.046],
    'Euc_1': [0.075, 0.046, 0.047, 0.054, 0.306, 0.585, 0.871, 0.045],
    'Euc_2': [0.051, 0.045, 0.046, 0.227, 0.471, 0.749, 0.842, 0.045],
    'Thy_1': [0.075, 0.049, 0.052, 0.206, 0.496, 0.597, 0.764, 0.044],
    'Thy_2': [0.064, 0.049, 0.056, 0.215, 0.376, 0.643, 0.865, 0.046],
    'Lem_1': [0.248, 0.086, 0.071, 0.056, 0.303, 0.491, 0.673, 0.045],
    'Lem_2': [0.235, 0.076, 0.068, 0.055, 0.402, 0.522, 0.708, 0.044],
    'Clo_1': [0.176, 0.058, 0.167, 0.291, 0.510, 0.643, 0.878, 1.000],
    'Clo_2': [0.100, 0.065, 0.270, 0.330, 0.471, 0.595, 0.803, 1.016],
    'Gin_1': [0.121, 0.192, 0.123, 0.113, 0.075, 0.062, 0.052, 0.805],
    'Gin_2': [0.090, 0.180, 0.150, 0.088, 0.069, 0.062, 0.053, 0.853]
}

data_calbicans = {
    'Cin_1': [0.147, 0.099, 0.120, 0.103, 0.099, 0.099, 0.151, 0.086],
    'Cin_2': [0.273, 0.225, 0.137, 0.174, 0.117, 0.103, 0.100, 0.084],
    'Euc_1': [0.093, 0.096, 0.097, 0.111, 1.478, 1.516, 1.593, 0.082],
    'Euc_2': [0.104, 0.093, 0.095, 0.169, 1.495, 1.504, 1.534, 0.083],
    'Thy_1': [0.112, 0.133, 0.098, 0.101, 1.188, 1.508, 1.512, 0.098],
    'Thy_2': [0.108, 0.093, 0.102, 0.098, 0.209, 1.391, 1.527, 0.095],
    'Lem_1': [0.158, 0.096, 0.095, 0.098, 0.101, 0.099, 1.498, 0.099],
    'Lem_2': [0.156, 0.096, 0.095, 0.099, 0.104, 0.100, 0.114, 0.095],
    'Clo_1': [0.413, 0.142, 0.138, 0.110, 0.112, 0.136, 1.526, 1.421],
    'Clo_2': [0.398, 0.170, 0.149, 0.116, 0.105, 0.285, 1.534, 1.485],
    'Gin_1': [0.192, 0.192, 0.204, 0.120, 0.122, 0.098, 0.186, 1.530],
    'Gin_2': [0.153, 0.248, 0.139, 0.119, 0.098, 0.096, 0.100, 1.519]
}

# Create DataFrames for each organism
df_ecoli = pd.DataFrame(data)
df_saureus = pd.DataFrame(data_saureus)
df_calbicans = pd.DataFrame(data_calbicans)

# Set index for all DataFrames
for df in [df_ecoli, df_saureus, df_calbicans]:
    df.index = range(1, 9)

# Definir as concentrações (em mg/mL)
concentrations = np.array([180, 90, 45, 22.5, 11.25, 5.625, 2.8125])

# Calcular o log10 das concentrações
log10_concentrations = np.log10(concentrations)

# Criar uma única figura para todos os plots
fig = plt.figure(figsize=(8, 15))  # Ajustado para formato vertical

def plot_mic_data(df, organism_name, subplot_position):
    # Initialize mic_values dictionary
    mic_values = {}
    
    # Calculate means of duplicates for this specific organism
    data_mean = {
        'Cinnamon': df[['Cin_1', 'Cin_2']].mean(axis=1),
        'Eucalyptus': df[['Euc_1', 'Euc_2']].mean(axis=1),
        'Thyme': df[['Thy_1', 'Thy_2']].mean(axis=1),
        'Lemongrass': df[['Lem_1', 'Lem_2']].mean(axis=1),
        'Clove': df[['Clo_1', 'Clo_2']].mean(axis=1),
        'Ginger': df[['Gin_1', 'Gin_2']].mean(axis=1)
    }
    
    # Create DataFrame with means
    df_mean = pd.DataFrame(data_mean)
    
    # Calculate controls
    negative_control = df_mean.iloc[7, :3].mean()
    positive_control = df_mean.iloc[7, 3:].mean()
    mic_threshold = negative_control + (positive_control - negative_control) * 0.1
    
    print(f"\n{organism_name} Controls:")
    print(f"Negative Control: {negative_control:.3f}")
    print(f"Positive Control: {positive_control:.3f}")
    print(f"MIC Threshold: {mic_threshold:.3f}")
    
    # Create df_dilutions without control row
    df_dilutions = df_mean.iloc[:-1].copy()
    df_dilutions.index = log10_concentrations
    
    # Create subplot
    ax = plt.subplot(3, 1, subplot_position)  # Mudado para 3 linhas, 1 coluna
    
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD', '#D4A5A5']
    
    # Plot data
    for idx, (oil, color) in enumerate(zip(df_dilutions.columns, colors)):
        mic_found = False
        for i, conc in enumerate(concentrations):
            if df_dilutions[oil].iloc[i] <= mic_threshold:
                mic_values[oil] = conc
                mic_found = True
                break
        
        if mic_found:
            label = f'{oil} (MIC: {mic_values[oil]:.1f})'
        else:
            label = f'{oil} (MIC: >180)'
            
        plt.plot(log10_concentrations, df_dilutions[oil], 
                marker='o', color=color, 
                linewidth=2, markersize=8,
                label=label)
        
        if mic_found:
            plt.plot(np.log10(mic_values[oil]), df_dilutions[oil].iloc[i], 
                    marker='^', color=color, markersize=15)

    # Add control lines
    plt.axhline(y=positive_control, color='#00FF00', linestyle='--', alpha=0.5)
    plt.axhline(y=negative_control, color='red', linestyle='--', alpha=0.5)
    plt.axhline(y=mic_threshold, color='black', linestyle=':', alpha=0.5)

    # Configure legend for each subplot
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', 
              frameon=True, framealpha=0.8, 
              fontsize=12, ncol=1)

    # Configure axes
    plt.xlabel('log [Concentration (mg/mL)]', fontsize=10)
    
    # Ajuste do rótulo y baseado no organismo
    if subplot_position == 3:  # Para C. albicans
        plt.ylabel('Absorbance (λ = 530 nm)', fontsize=10)
    else:  # Para E. coli e S. aureus
        plt.ylabel('Absorbance (λ = 630 nm)', fontsize=10)
    
    plt.title(f'{organism_name}', fontsize=12, loc='left')

    # Configure X axis
    plt.xscale('linear')
    major_ticks = log10_concentrations
    labels = [f'{x:.1f}' for x in log10_concentrations]
    plt.xticks(major_ticks, labels, rotation=45, fontsize=8)
    plt.xlim(0.4, 2.3)

    # Adjust grid
    plt.grid(True, which='both', linestyle='--', alpha=0.2)
    plt.tick_params(axis='both', which='major', labelsize=8)

# Plot for each organism
plot_mic_data(df_ecoli, "A", 1)      # Top
plot_mic_data(df_saureus, "B", 2)    # Middle
plot_mic_data(df_calbicans, "C", 3)  # Bottom

# Ajustar layout para prevenir sobreposição
plt.tight_layout()

# Apenas mostrar a figura e manter aberta
plt.show(block=True)  # block=True manterá a janela aberta
