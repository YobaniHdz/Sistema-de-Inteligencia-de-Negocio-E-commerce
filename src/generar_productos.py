import pandas as pd
import numpy as np

np.random.seed(42)

categorias = {
    "Electrónica": [
        "Laptop", "Smartphone", "Tablet",
        "Audífonos", "Smartwatch"
    ],
    "Hogar": [
        "Cafetera", "Silla", "Mesa",
        "Lámpara", "Aspiradora"
    ],
    "Ropa": [
        "Playera", "Pantalón", "Sudadera",
        "Tenis", "Chaqueta"
    ]
}

productos = []
id_counter = 1

for categoria, items in categorias.items():
    for item in items:
        nombre = f"{item} Pro"
        producto_id = f"P{id_counter:03d}"

        productos.append((
            producto_id,
            nombre,
            categoria
        ))

        id_counter += 1

df = pd.DataFrame(
    productos,
    columns=[
        "producto_id",
        "nombre_producto",
        "categoria"
    ]
)

df.to_csv("../data/raw/productos.csv", index=False)

print("Catálogo de productos generado ✅")
