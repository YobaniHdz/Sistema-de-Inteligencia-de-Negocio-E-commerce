import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# -------------------------
# Configuración
# -------------------------

st.set_page_config(
    page_title="Dashboard E-commerce",
    layout="wide"
)

st.title("Sistema de Inteligencia de Negocio — E-commerce")

# -------------------------
# Paths
# -------------------------

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_PATH = BASE_DIR / "data" / "processed" / "ventas_limpias.csv"
CLIENTES_PATH = BASE_DIR / "data" / "raw" / "clientes.csv"

# -------------------------
# Cargar datos + joins
# -------------------------

@st.cache_data
def load_data():

    df = pd.read_csv(DATA_PATH)
    df["fecha"] = pd.to_datetime(df["fecha"])

    # DEBUG (puedes quitarlo luego)
    st.write("Columnas cargadas:", df.columns.tolist())

    # Fallback inteligente por si cambia el nombre
    if "nombre_producto" not in df.columns:
        if "producto" in df.columns:
            df["nombre_producto"] = df["producto"]

    return df



df = load_data()

# -------------------------
# Sidebar — filtros
# -------------------------

st.sidebar.header("Filtros")

segmento = st.sidebar.multiselect(
    "Segmento de cliente",
    options=df["segmento_cliente"].unique(),
    default=df["segmento_cliente"].unique()
)

df_filtrado = df[
    df["segmento_cliente"].isin(segmento)
]

# -------------------------
# KPIs principales
# -------------------------

col1, col2, col3 = st.columns(3)

ingresos_totales = df_filtrado["ingreso"].sum()
ganancia_total = df_filtrado["ganancia"].sum()
margen_promedio = df_filtrado["margen_pct"].mean()

col1.metric("💰 Ingresos totales", f"${ingresos_totales:,.0f}")
col2.metric("📈 Ganancia total", f"${ganancia_total:,.0f}")
col3.metric("📊 Margen promedio", f"{margen_promedio:.1%}")

st.divider()

# -------------------------
# Rentabilidad por producto
# -------------------------

st.subheader("Rentabilidad por producto")

rentabilidad = (
    df_filtrado.groupby("nombre_producto")
    .agg({
        "ingreso": "sum",
        "ganancia": "sum"
    })
    .reset_index()
)

fig_prod = px.bar(
    rentabilidad,
    x="nombre_producto",
    y="ganancia",
    title="Ganancia total por producto"
)

st.plotly_chart(fig_prod, use_container_width=True)

# -------------------------
# Ganancia por categoría
# -------------------------

ganancia_categoria = (
    df_filtrado.groupby("categoria")["ganancia"]
    .sum()
    .reset_index()
)

fig_cat = px.pie(
    ganancia_categoria,
    names="categoria",
    values="ganancia",
    title="Distribución de ganancia por categoría",
    hole=0.3,
    color_discrete_sequence=[
        "#2389d1",
        "#91d1e4",
        "#d8cbb3"
    ]
)

fig_cat.update_traces(textinfo="percent+label")

st.plotly_chart(fig_cat, use_container_width=True)

# -------------------------
# Segmentación de clientes
# -------------------------

st.subheader("Segmentación de clientes")

clientes_segmento = (
    df_filtrado.groupby(
        ["nombre_completo", "segmento_cliente"]
    )["ingreso"]
    .sum()
    .reset_index()
)

fig_clientes = px.box(
    clientes_segmento,
    x="segmento_cliente",
    y="ingreso",
    title="Distribución de valor por segmento"
)

st.plotly_chart(fig_clientes, use_container_width=True)

# -------------------------
# Tendencia temporal
# -------------------------

st.subheader("Tendencia de ganancias")

tendencia = (
    df_filtrado.groupby("fecha")["ganancia"]
    .sum()
    .reset_index()
)

fig_time = px.line(
    tendencia,
    x="fecha",
    y="ganancia",
    title="Ganancia en el tiempo"
)

st.plotly_chart(fig_time, use_container_width=True)

# -------------------------
# Top clientes
# -------------------------

st.subheader("Top 10 clientes")

top_clientes = (
    df_filtrado.groupby("nombre_completo")["ingreso"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

# Renombrar columnas para presentación
top_clientes.columns = ["Cliente", "Ingresos totales"]

# Crear ranking empezando en 1
top_clientes.index = range(1, len(top_clientes) + 1)

# Mostrar tabla con formato bonito
st.dataframe(
    top_clientes.style.format({
        "Ingresos totales": "${:,.2f}"
    }),
    use_container_width=True
)

