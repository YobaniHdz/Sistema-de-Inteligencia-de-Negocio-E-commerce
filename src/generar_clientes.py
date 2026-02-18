import pandas as pd
from faker import Faker

# reproducibilidad
fake = Faker("es_MX")
Faker.seed(42)
fake.unique.clear()

CLIENTE_MIN = 1000
CLIENTE_MAX = 1999

clientes = []

for cliente_id in range(CLIENTE_MIN, CLIENTE_MAX + 1):

    nombre = fake.first_name()
    apellido = fake.last_name()

    clientes.append({
        "cliente_id": cliente_id,
        "nombre": nombre,
        "apellido": apellido,
        "nombre_completo": f"{nombre} {apellido}",
        "email": fake.unique.email()
    })

df_clientes = pd.DataFrame(clientes)

df_clientes.to_csv("../data/raw/clientes.csv", index=False)

print(f"{len(df_clientes)} clientes generados correctamente ✅")
