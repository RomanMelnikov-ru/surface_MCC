import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import streamlit as st

# Функция для расчета M
def calculate_M(phi_deg):
    phi_rad = np.deg2rad(phi_deg)  # Переводим градусы в радианы
    return 6 * np.sin(phi_rad) / (3 - np.sin(phi_rad))

# Функция для вычисления координат поверхности
def f(theta, p, M, p0):
    # Ограничиваем p, чтобы p0 - p >= 0
    p = np.clip(p, 0, p0)
    q = np.sqrt(M ** 2 * p * (p0 - p))  # Девиаторное напряжение
    # Вычисляем синусы для всех углов заранее
    sin_theta = np.sin(theta)
    sin_theta_minus_120 = np.sin(theta - 2 * np.pi / 3)
    sin_theta_plus_120 = np.sin(theta + 2 * np.pi / 3)
    x = p + (2 / 3) * q * sin_theta_minus_120
    y = p + (2 / 3) * q * sin_theta
    z = p + (2 / 3) * q * sin_theta_plus_120
    return x, y, z

# Создание интерфейса Streamlit
st.title("Поверхность текучести MODIFIED CAM CLAY")

# Слайдеры для управления параметрами
phi_deg = st.slider("Угол внутреннего трения φ (°):", min_value=10.0, max_value=30.0, value=15.0, step=0.1)
p0 = st.slider("Давление пред. уплотнения p0 (кПа):", min_value=0.0, max_value=50.0, value=50.0, step=1.0)

# Инициализация параметров
M = calculate_M(phi_deg)

# Создание сетки для theta и p
theta = np.linspace(-np.pi, np.pi, 70)
p = np.linspace(0.01, p0, 70)  # Ограничиваем p до p0
theta, p = np.meshgrid(theta, p)

# Вычисление координат поверхности
x, y, z = f(theta, p, M, p0)

# Создание графика
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(111, projection='3d')
ax.set_title('Поверхность текучести MODIFIED CAM CLAY')

# Построение поверхности
surface = ax.plot_surface(x, y, z, color='orange', alpha=0.5, edgecolor='red')

# Настройка осей
ax.set_xlabel("σ1")
ax.set_ylabel("σ2")
ax.set_zlabel("σ3")
axis_limit = 60  # Оси дальше, чем поверхность
ax.set_xlim(0, axis_limit)
ax.set_ylim(0, axis_limit)
ax.set_zlim(0, axis_limit)

# Добавляем оси координат
ax.quiver(0, 0, 0, axis_limit * 0.5, 0, 0, color='r', arrow_length_ratio=0.1, linewidth=1)  # Ось X
ax.quiver(0, 0, 0, 0, axis_limit * 0.5, 0, color='g', arrow_length_ratio=0.1, linewidth=1)  # Ось Y
ax.quiver(0, 0, 0, 0, 0, axis_limit * 0.5, color='b', arrow_length_ratio=0.1, linewidth=1)  # Ось Z

# Отображение графика в Streamlit
st.pyplot(fig)
