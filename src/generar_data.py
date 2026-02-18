import pandas as pd
import numpy as np

np.random.seed(42)

n = 5000

# -------------------------
# Catálogo de productos realista
# -------------------------

catalogo = {
    "Electrónica": [
        ("Laptop Lenovo IdeaPad", 800, 500),
        ("Smartphone Samsung Galaxy", 600, 350),
        ("Audífonos Bluetooth Sony", 120, 60),
        ("Monitor LG 24 pulgadas", 220, 140)
    ],
    "Ropa": [
        ("Playera deportiva Nike", 35, 15),
        ("Tenis Adidas Running", 90, 50),
        ("Sudadera Puma", 60, 30),
        ("Jeans Levi's", 70, 40)
    ],
    "Hogar": [
        ("Silla ergonómica", 150, 90),
        ("Lámpara LED moderna", 45, 20),
        ("Mesa de centro", 200, 120),
        ("Cafetera automática", 180, 100)
    ]
}

# -------------------------
# Generar productos coherentes
# -------------------------

categorias = list(catalogo.keys())

productos = []
precios = []
costos = []
cats = []

for _ in range(n):
    categoria = np.random.choice(categorias)
    producto, precio_base, costo_base = catalogo[categoria][
        np.random.randint(len(catalogo[categoria]))
    ]

    # variación realista
    precio = np.random.normal(precio_base, precio_base * 0.1)
    costo = np.random.normal(costo_base, costo_base * 0.1)

    productos.append(producto)
    precios.append(max(precio, costo + 1))  # asegura margen positivo
    costos.append(costo)
    cats.append(categoria)

# -------------------------
# Dataset principal
# -------------------------

data = {
    "fecha": pd.date_range("2024-01-01", periods=n, freq="H"),
    "cliente_id": np.random.randint(1000, 2000, n),
    "producto": productos,
    "categoria": cats,
    "precio": precios,
    "costo": costos,
    "canal": np.random.choice(["Web", "App móvil", "Marketplace"], n),
    "region": np.random.choice(
        ["CDMX", "Norte", "Occidente", "Sur"],
        n
    ),
    "descuento": np.random.uniform(0, 0.25, n)
}

df = pd.DataFrame(data)

# -------------------------
# Métricas derivadas
# -------------------------

df["ingreso"] = df["precio"] * (1 - df["descuento"])
df["ganancia"] = df["ingreso"] - df["costo"]

# -------------------------
# Guardar
# -------------------------

df.to_csv("../data/raw/ventas_empresa.csv", index=False)

print("Dataset realista generado ✅")
