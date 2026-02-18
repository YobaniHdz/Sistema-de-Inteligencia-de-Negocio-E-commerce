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
# Cargar datos procesados
# -------------------------

DATA_PATH = Path("../data/processed/ventas_limpias.csv")

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["fecha"] = pd.to_datetime(df["fecha"])
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

df = df[df["segmento_cliente"].isin(segmento)]

# -------------------------
# KPIs principales
# -------------------------

col1, col2, col3 = st.columns(3)

ingresos_totales = df["ingreso"].sum()
ganancia_total = df["ganancia"].sum()
margen_promedio = df["margen_pct"].mean()

col1.metric("💰 Ingresos totales", f"${ingresos_totales:,.0f}")
col2.metric("📈 Ganancia total", f"${ganancia_total:,.0f}")
col3.metric("📊 Margen promedio", f"{margen_promedio:.1%}")

st.divider()

# -------------------------
# Rentabilidad por producto
# -------------------------

st.subheader("Rentabilidad por producto")

rentabilidad = (
    df.groupby("producto")
    .agg({
        "ingreso": "sum",
        "ganancia": "sum"
    })
    .reset_index()
)

fig_prod = px.bar(
    rentabilidad,
    x="producto",
    y="ganancia",
    title="Ganancia total por producto"
)

st.plotly_chart(fig_prod, use_container_width=True)

ganancia_categoria = (
    df.groupby("categoria")["ganancia"]
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

clientes = (
    df.groupby(["cliente_id", "segmento_cliente"])["ingreso"]
    .sum()
    .reset_index()
)

fig_clientes = px.box(
    clientes,
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
    df.groupby("fecha")["ganancia"]
    .sum()
    .reset_index()
)

fig_time = px.line(
    tendencia,
    x="fecha",
    y="ganancia",
    title="Ganancia diaria"
)

st.plotly_chart(fig_time, use_container_width=True)

# -------------------------
# Top clientes
# -------------------------

st.subheader("Top clientes")

top_clientes = (
    df.groupby("cliente_id")["ingreso"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

st.dataframe(top_clientes, use_container_width=True)
