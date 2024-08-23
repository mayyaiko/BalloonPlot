import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import cm
import rpy2.robjects as robjects
from rpy2.robjects import pandas2ri

# Ativa a conversão de objetos R para pandas
pandas2ri.activate()

# Carrega o dataset msleep de R
robjects.r('library(ggplot2)')
msleepR = robjects.r('msleep')

# Converte o dataset R para um DataFrame pandas
msleep = pandas2ri.rpy2py(msleepR)

# Definir as variáveis que serão exibidas nas colunas
vars = ['awake', 'sleep_total', 'sleep_rem']

# Preparar os dados: selecionar as colunas necessárias e fazer um subconjunto aleatório
df = msleep.dropna(subset=['vore'])[["name", "vore"] + vars].copy()
df = df.groupby('vore').apply(lambda x: x.sample(5)).reset_index(drop=True)
df = df.melt(id_vars=['name', 'vore'], value_vars=vars, var_name='variable', value_name='value')
df = df.dropna().sort_values(by=['vore', 'name']).reset_index(drop=True)

# Adicionar colunas para posicionamento no gráfico
df['row'] = pd.Categorical(df['name'], categories=df['name'].unique()).codes + 1
df['col'] = pd.Categorical(df['variable'], categories=vars).codes + 1

# Criar o balloon plot
plt.figure(figsize=(10, 8))
cmap = cm.get_cmap('viridis')

# Plotar os pontos como círculos
sns.scatterplot(
    data=df, 
    x='col', 
    y='row', 
    hue='vore', 
    size='value', 
    sizes=(100, 500), 
    alpha=0.7, 
    palette='Set1',
    legend=False
)

# Adicionar os valores ao lado dos "balões"
for _, row in df.iterrows():
    plt.text(row['col'] + 0.25, row['row'], f"{row['value']:.1f}", 
             va='center', ha='left', fontsize=10, alpha=1.0)

# Definir os labels dos eixos
plt.xticks(ticks=range(1, len(vars) + 1), labels=vars, rotation=90)
plt.yticks(ticks=range(1, len(df['name'].unique()) + 1), labels=df['name'].unique())

# Customizar o layout do plot
plt.gca().invert_yaxis()
plt.xlabel('')
plt.ylabel('')
plt.grid(False)
plt.title('Balloon Plot')

# Mostrar o plot
plt.show()