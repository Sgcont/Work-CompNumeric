import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline

# Pontos originais
pontos = [
    (0.113, 0.136), (0.2 , 0.217), (0.267 , 0.309), (0.313 , 0.512), (0.343 , 0.688),
    (0.392 , 0.826), (0.430 , 0.720), (0.454 ,  0.598), (0.481 , 0.469), (0.524 , 0.363),
    (0.592 , 0.309), (0.692 , 0.350), (0.814 , 0.355), (0.903 , 0.366)
]

# Conversão para arrays e mudança de escala no eixo x
x_original = np.array([p[0] for p in pontos])
y_original = np.array([p[1] for p in pontos])

# Escala 
x_escalado = x_original * (1000)-113
y_escalado = (y_original) * (10) + 1.36

print(x_escalado)
print(y_escalado)

# Interpolação suave usando a biblioteca spline, com uma suavização de 0.001 (bem pequena e boa)
spline = UnivariateSpline(x_escalado, y_escalado, s=0.001)  
x_interp = np.linspace(min(x_escalado), max(x_escalado), 300)
y_interp = spline(x_interp)

# Nós (pontos de quebra entre os polinômios)
print("Nós (knots):", spline.get_knots())

# Coeficientes dos polinômios
print("Coeficientes B-spline:", spline.get_coeffs())

# Plot do gráfico com interpolação suave
plt.figure(figsize=(8, 5))
plt.plot(x_interp, y_interp, label='Interpolação', color='blue')
plt.scatter(x_escalado, y_escalado, color='red', label='Pontos originais')
plt.title("Interpolação dos pontos")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

#Função da Interpolação de Newton
def newton(x, y):
    n = len(x)
    coef = np.copy(y)
    for j in range(1, n):
        coef[j:n] = (coef[j:n] - coef[j - 1]) / (x[j:n] - x[j - 1])

    def N(x_valor):
        total = coef[-1]
        for i in range(n - 2, -1, -1):
            total = total * (x_valor - x[i]) + coef[i]
        return total

    return N

#Interpolação por partes - dividido em 3 partes
partes = 3
x_total = []
y_total = []

for i in range(0, len(x_escalado) - (partes - 1), partes - 1):
    x_parte = x_escalado[i:i + partes]
    y_parte = y_escalado[i:i + partes]

    N = newton(x_parte, y_parte)

    x_interp = np.linspace(x_parte[0], x_parte[-1], 100)
    y_interp = [N(xi) for xi in x_interp]

    x_total.extend(x_interp)
    y_total.extend(y_interp)

# Gráfico utilizando o método de Newton em 3 partes
plt.figure(figsize=(8, 5))
plt.plot(x_total, y_total, label='Interpolação Newton (Interpolação por 3 partes)', color='blue')
plt.title("Interpolação Newton (Interpolação por 3 partes)")
plt.xlabel("X")
plt.ylabel("Y")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

plt.show()
