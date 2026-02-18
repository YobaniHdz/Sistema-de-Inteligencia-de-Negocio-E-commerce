import pandas as pd
import numpy as np

np.random.seed(42)

n = 5000

# cargar dimensiones
df_prod = pd.read_csv("../data/raw/productos.csv")
df_cli = pd.read_csv("../data/raw/clientes.csv")

# muestreo real de IDs existentes
productos_sample = df_prod.sample(n=n, replace=True)
clientes_sample = np.random.choice(
    df_cli["cliente_id"],
    n
)

precios = np.random.uniform(50, 1200, n)
costos = precios * np.random.uniform(0.5, 0.8, n)
descuentos = np.random.uniform(0, 0.25, n)

ventas = pd.DataFrame({
    "fecha": pd.date_range("2024-01-01", periods=n, freq="h"),
    "cliente_id": clientes_sample,
    "producto_id": productos_sample["producto_id"].values,
    "precio": precios,
    "costo": costos,
    "canal": np.random.choice(
        ["Web", "App móvil", "Marketplace"],
        n
    ),
    "region": np.random.choice(
        ["CDMX", "Norte", "Occidente", "Sur"],
        n
    ),
    "descuento": descuentos
})

# métricas de negocio
ventas["ingreso"] = ventas["precio"] * (1 - ventas["descuento"])
ventas["ganancia"] = ventas["ingreso"] - ventas["costo"]

ventas.to_csv("../data/raw/ventas_empresa.csv", index=False)

print("Ventas generadas correctamente ✅")
