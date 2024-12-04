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

df_ecoli = pd.DataFrame(data)
df_ecoli.index = range(1, 9)

# Calcular médias das duplicatas
data_mean = {
    'Cinnamon': df_ecoli[['Cin_1', 'Cin_2']].mean(axis=1),
    'Eucalyptus': df_ecoli[['Euc_1', 'Euc_2']].mean(axis=1),
    'Thyme': df_ecoli[['Thy_1', 'Thy_2']].mean(axis=1),
    'Lemongrass': df_ecoli[['Lem_1', 'Lem_2']].mean(axis=1),
    'Clove': df_ecoli[['Clo_1', 'Clo_2']].mean(axis=1),
    'Ginger': df_ecoli[['Gin_1', 'Gin_2']].mean(axis=1)
}

# Criar novo DataFrame com as médias
df_mean = pd.DataFrame(data_mean)

# Definir as concentrações (em mg/mL)
concentrations = np.array([180, 90, 45, 22.5, 11.25, 5.625, 2.8125])

# Calcular o log10 das concentrações
log10_concentrations = np.log10(concentrations)

# Criar df_dilutions com log10
df_dilutions = df_mean.iloc[:-1].copy()
df_dilutions.index = log10_concentrations

# Calcular controles usando as médias
negative_control = df_mean.iloc[7, :3].mean()  # Média do controle negativo
positive_control = df_mean.iloc[7, 3:].mean()  # Média do controle positivo
mic_threshold = negative_control + (positive_control - negative_control) * 0.1

# Dicionário para armazenar os MICs
mic_values = {}

# Criar o gráfico
plt.figure(figsize=(12, 8))

# Cores personalizadas para cada óleo
colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEEAD', '#D4A5A5']

# Plotar dados
for idx, (oil, color) in enumerate(zip(df_dilutions.columns, colors)):
    # Encontrar MIC primeiro
    mic_found = False
    for i, conc in enumerate(concentrations):
        if df_dilutions.iloc[i][oil] <= mic_threshold:
            mic_values[oil] = conc
            mic_found = True
            break
    
    # Plotar linha e pontos com MIC na legenda
    if mic_found:
        label = f'{oil} (MIC: {mic_values[oil]:.1f})'
    else:
        label = f'{oil} (MIC: >180)'  # Valor máximo testado
        
    plt.plot(log10_concentrations, df_dilutions[oil], 
             marker='o', color=color, 
             linewidth=2, markersize=8,
             label=label)
    
    # Marcar ponto MIC com triângulo apenas se encontrado
    if mic_found:
        plt.plot(np.log10(mic_values[oil]), df_dilutions.iloc[i][oil], 
                marker='^', color=color, markersize=15)

# Adicionar linhas de controle (sem adicionar à legenda)
plt.axhline(y=positive_control, color='#00FF00', linestyle='--', alpha=0.5)
plt.axhline(y=negative_control, color='red', linestyle='--', alpha=0.5)
plt.axhline(y=mic_threshold, color='black', linestyle=':', alpha=0.5)

# Configurar legenda
plt.legend(bbox_to_anchor=(1.02, 0.98), loc='upper left', 
          frameon=True, framealpha=0.8, 
          fontsize=10, ncol=1)

# Configurar eixos
plt.xlabel('log [Concentração (mg/mL)]', fontsize=12)
plt.ylabel('Absorbance (λ = 630 nm)', fontsize=12)

# Configurar eixo X
plt.xscale('linear')  # Mudando para linear já que estamos usando log

# Definir ticks exatamente nos pontos dos dados
major_ticks = log10_concentrations
labels = [f'{x:.1f}' for x in log10_concentrations]  # Mostra valores log com 1 decimal

plt.xticks(major_ticks, labels, rotation=0)  # Sem rotação pois números são menores
plt.xlim(0.4, 2.3)  # Limites ajustados para os valores em log

# Ajustar grid para melhor visualização
plt.grid(True, which='both', linestyle='--', alpha=0.2)

# Aumentar tamanho das fontes dos ticks
plt.tick_params(axis='both', which='major', labelsize=10)

# Ajustar layout para não cortar os labels
plt.tight_layout()

plt.show(block=True)

# Calcular e mostrar MIC
print("\nMIC aproximado para cada óleo (mg/mL):")
for oil in df_dilutions.columns:
    for idx, conc in enumerate(concentrations):
        if df_dilutions.iloc[idx][oil] <= mic_threshold:
            print(f"{oil}: {conc}")
            break
