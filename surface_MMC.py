import numpy as np
import plotly.graph_objects as go
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

# Создание графика с помощью Plotly
fig = go.Figure()

# Добавление поверхности
fig.add_trace(go.Surface(z=z, x=x, y=y, colorscale='Viridis', showscale=False))

# Настройка осей напряжений
axis_limit_positive = 100
axis_limit_negative = -50

fig.add_trace(go.Scatter3d(
    x=[0, axis_limit_positive], y=[0, 0], z=[0, 0],
    mode="lines", line=dict(color="red"), name="σ₁"
))
fig.add_trace(go.Scatter3d(
    x=[0, 0], y=[0, axis_limit_positive], z=[0, 0],
    mode="lines", line=dict(color="green"), name="σ₂"
))
fig.add_trace(go.Scatter3d(
    x=[0, 0], y=[0, 0], z=[0, axis_limit_positive],
    mode="lines", line=dict(color="blue"), name="σ₃"
))

# Настройка осей без меток
fig.update_layout(
    scene=dict(
        xaxis=dict(range=[axis_limit_negative, axis_limit_positive], title="σ₁", showticklabels=True, showgrid=True, zeroline=True),
        yaxis=dict(range=[axis_limit_negative, axis_limit_positive], title="σ₂", showticklabels=True, showgrid=True, zeroline=True),
        zaxis=dict(range=[axis_limit_negative, axis_limit_positive], title="σ₃", showticklabels=True, showgrid=True, zeroline=True),
        aspectmode="cube"  # Сохраняем пропорции осей
    ),
    legend=dict(title="Оси напряжений")
)

# Отображение графика в Streamlit
st.plotly_chart(fig)
