import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.image as mpimg
from scipy.interpolate import make_interp_spline

# Arquivo da imagem (ajuste o nome do arquivo)
filename = 'densidadeXcapacidade.png'  # substitua pelo seu arquivo real

# Limites do gráfico na escala do gráfico real (ajuste se necessário)
theta_min, theta_max = 0, 900
rho_min, rho_max = 3, 9  # valores extremos no gráfico original

# Carrega a imagem
caminho_arquivo = os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)
img = mpimg.imread(caminho_arquivo)

# Variáveis globais
pontos_x, pontos_y = [], []

# Função de clique para obter pontos
def onclick(event):
    if event.xdata is not None and event.ydata is not None:
        # salvar coordenadas pixel
        pontos_x.append(event.xdata)
        pontos_y.append(event.ydata)
        # desenhar ponto na imagem
        plt.scatter(event.xdata, event.ydata, c='blue')
        plt.draw()

# Prepara a figura
fig, ax = plt.subplots()
ax.imshow(img, extent=[0, 1, 0, 1])
cid = fig.canvas.mpl_connect('button_press_event', onclick)

print("Clique nos pontos do gráfico para obter coordenadas. Quando terminar, feche a janela.")

plt.show()  # janela para clicar

# Após fechamento, transformar pontos de pixel para coordenadas do gráfico real
# para isso, precisamos de referência: os limites do plot (extent) e escala
def transformar_coordenadas(px, py):
    # px, py estão em [0, 1], onde o eixo x vai de 0 a 1
    # Mapear para o intervalo real usando os limites do gráfico
    theta = px * (theta_max - theta_min) + theta_min
    rho = py * (rho_max - rho_min) + rho_min

    # Se o gráfico estiver em escala logarítmica, aplique a transformação inversa
    # Aqui, supondo que as escalas são lineares, ajuste se necessário
    return theta, rho

# Converte pontos coletados
theta_vals = []
rho_vals = []

for px, py in zip(pontos_x, pontos_y):
    theta, rho = transformar_coordenadas(px, py)
    theta_vals.append(theta)
    rho_vals.append(rho)

# Ajuste de polinômio ou interpolação
# Opção 1: ajuste polinomial de grau n (exemplo: grau 3)
grau = 3
coef = np.polyfit(theta_vals, rho_vals, grau)

# Cria a função do polinômio
poly_func = np.poly1d(coef)

# Gera pontos para plotar o polinômio
theta_plot = np.linspace(theta_min, theta_max, 500)
rho_fit = poly_func(theta_plot)

# Plot do gráfico original (com pontos) e ajuste
fig2, ax2 = plt.subplots()

# Recarregar imagem original
ax2.imshow(img, extent=[4,200])

# Traçar os pontos clicados
ax2.scatter(pontos_x, pontos_y, c='blue', label='Pontos coletados')

# Traçar o polinômio ajustado
# Converter os pontos do ajuste para o espaço da imagem se desejar
ax2.plot(theta_plot / (theta_max - theta_min), (rho_fit - rho_min) / (rho_max - rho_min), c='red', label='Ajuste polinomial')
ax2.legend()
ax2.set_xlabel('x (relativo)')
ax2.set_ylabel('y (relativo)')
plt.title('Ajuste do polinômio aos pontos')
plt.show()

# Agora, você terá o polinômio e uma visualização dele frente ao gráfico original
print("Coeficientes do polinômio de grau", grau, ":", coef)
