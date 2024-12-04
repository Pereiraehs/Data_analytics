import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy import stats
import matplotlib

# Configurar o estilo
plt.style.use('classic')
sns.set_theme(style="whitegrid")
sns.set_palette("husl")

# Função para processar dados e criar gráfico
def create_mic_plot(data, ax, title):
    # Criar DataFrame
    df = pd.DataFrame(data)
    
    # Calcular médias das duplicatas
    data_mean = {
        'Cinnamon': df[['Cin_1', 'Cin_2']].mean(axis=1),
        'Eucalyptus': df[['Euc_1', 'Euc_2']].mean(axis=1),
        'Thyme': df[['Thy_1', 'Thy_2']].mean(axis=1),
        'Lemongrass': df[['Lem_1', 'Lem_2']].mean(axis=1),
        'Clove': df[['Clo_1', 'Clo_2']].mean(axis=1),
        'Ginger': df[['Gin_1', 'Gin_2']].mean(axis=1)
    }
    
    df_mean = pd.DataFrame(data_mean)
    
    # Definir concentrações e calcular log10
    concentrations = np.array([180, 90, 45, 22.5, 11.25, 5.625, 2.8125])
    log10_concentrations = np.log10(concentrations)
    
    # Criar df_dilutions
    df_dilutions = df_mean.iloc[:-1].copy()
    df_dilutions.index = log10_concentrations
    
    # Calcular controles
    negative_control = df_mean.iloc[7, :3].mean()
    positive_control = df_mean.iloc[7, 3:].mean()
    mic_threshold = negative_control + (positive_control - negative_control) * 0.1
    
    # Cores personalizadas mais distintas
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD', '#D4A5A5']
    
    # Plotar dados com elementos padrão
    for idx, (oil, color) in enumerate(zip(df_dilutions.columns, colors)):
        mic_found = False
        for i, conc in enumerate(concentrations):
            if df_dilutions.iloc[i][oil] <= mic_threshold:
                mic_found = True
                break
        
        if mic_found:
            label = f'{oil} (MIC: {conc:.1f})'
        else:
            label = f'{oil} (MIC: >180)'
            
        ax.plot(log10_concentrations, df_dilutions[oil], 
                marker='o', color=color, 
                linewidth=1, markersize=3,  # Tamanhos padrão
                label=label)
        
        if mic_found:
            ax.plot(np.log10(conc), df_dilutions.iloc[i][oil], 
                    marker='^', color=color, markersize=4)
    
    # Linhas de controle padrão
    ax.axhline(y=positive_control, color='#00FF00', linestyle='--', alpha=0.3, linewidth=1)
    ax.axhline(y=negative_control, color='red', linestyle='--', alpha=0.3, linewidth=1)
    ax.axhline(y=mic_threshold, color='black', linestyle=':', alpha=0.3, linewidth=1)
    
    # Configurar eixos com fontes padrão
    ax.set_xlabel('log [Concentração (mg/mL)]', fontsize=8)
    ax.set_ylabel('Absorbance (λ = 630 nm)', fontsize=8)
    ax.set_title(title, fontsize=10, loc='left', pad=5, weight='bold')
    
    # Configurar eixo X
    ax.set_xlim(0.4, 2.3)
    ax.set_xticks(log10_concentrations)
    ax.set_xticklabels([f'{x:.1f}' for x in log10_concentrations], fontsize=7)
    ax.tick_params(axis='y', labelsize=7)
    
    # Grid padrão
    ax.grid(True, which='both', linestyle='--', alpha=0.2, linewidth=0.5)
    
    # Legenda padrão
    ax.legend(bbox_to_anchor=(1.02, 1), loc='upper left', 
             frameon=True, framealpha=0.8, 
             fontsize=6, ncol=1)

# Tamanho da figura mantido compacto
width_inches = 0.9
height_inches = 1.25

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, 
                                   figsize=(width_inches, height_inches), 
                                   dpi=600)

# Dados para E. coli
data_ecoli = {
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

# Dados para S. aureus
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

# Dados para C. albicans
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

# Criar plots
create_mic_plot(data_ecoli, ax1, 'A')
create_mic_plot(data_saureus, ax2, 'B')
create_mic_plot(data_calbicans, ax3, 'C')

# Ajustar espaçamento
plt.subplots_adjust(hspace=0.5, right=0.75, left=0.25, top=0.95, bottom=0.1)

# Salvar com alta resolução
plt.savefig('MIC_plot.png', dpi=600, bbox_inches='tight')
plt.savefig('MIC_plot.pdf', bbox_inches='tight')

plt.show()
