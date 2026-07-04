from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="EDA", page_icon="📊", layout="wide")
sns.set_theme(style="whitegrid")

ROOT = Path(__file__).resolve().parents[2]
ORDEN_PLAN = ["Básico", "Estándar", "Premium"]


@st.cache_data
def cargar_datos():
    return pd.read_csv(ROOT / "data" / "processed" / "streaming_users_clean.csv",
                       parse_dates=["last_login_date"])


df = cargar_datos()

st.title("📊 Análisis exploratorio")
st.markdown(
    "Cinco visualizaciones que responden las preguntas del proyecto. "
    "Podés filtrar por país; las interpretaciones se refieren al dataset completo."
)

pais = st.selectbox("Filtrar por país", ["Todos"] + sorted(df["country"].unique()))
datos = df if pais == "Todos" else df[df["country"] == pais]
st.caption(f"Mostrando {len(datos):,} usuarios".replace(",", "."))

# ---------------------------------------------------------------- univariado 1
st.header("Análisis univariado")
st.subheader("1 · ¿Cuánto miran los usuarios por mes?")

fig, ax = plt.subplots(figsize=(9, 3.8))
sns.histplot(datos["monthly_watch_time_mins"], bins=60, ax=ax)
mediana = datos["monthly_watch_time_mins"].median()
ax.axvline(mediana, color="red", linestyle="--", label=f"Mediana: {mediana:.0f} min")
ax.set_xlabel("Minutos por mes")
ax.set_ylabel("Usuarios")
ax.legend()
st.pyplot(fig)

st.info(
    "**Interpretación:** la distribución es asimétrica a la derecha: la mitad de los usuarios "
    "mira hasta ~770 minutos por mes (unas 13 horas), pero una minoría intensiva supera los "
    "3.000. Por eso en este proyecto el consumo se resume siempre con la mediana y no con el "
    "promedio, que queda inflado por esa cola."
)

# ---------------------------------------------------------------- univariado 2
st.subheader("2 · ¿Cómo se reparten los planes?")

fig, ax = plt.subplots(figsize=(9, 3.5))
sns.countplot(data=datos, x="subscription_plan", order=ORDEN_PLAN, ax=ax)
for cont in ax.containers:
    ax.bar_label(cont)
ax.set_xlabel("Plan")
ax.set_ylabel("Usuarios")
st.pyplot(fig)

st.info(
    "**Interpretación:** la base es mayormente económica: Básico concentra el 45 % de los "
    "usuarios, Estándar el 35 % y Premium apenas el 20 %. El segmento que más paga es el más "
    "chico, lo que vuelve relevante entender qué diferencia su comportamiento (siguiente gráfico)."
)

# ---------------------------------------------------------------- bivariado 1
st.header("Análisis bivariado")
st.subheader("3 · ¿El consumo depende del plan?")

fig, ax = plt.subplots(figsize=(9, 4))
sns.boxplot(data=datos, x="subscription_plan", y="monthly_watch_time_mins",
            order=ORDEN_PLAN, ax=ax)
ax.set_xlabel("Plan")
ax.set_ylabel("Minutos por mes")
st.pyplot(fig)

st.info(
    "**Interpretación (hallazgo principal):** el consumo escala con el plan: la mediana pasa de "
    "~553 minutos en Básico a ~840 en Estándar y ~1.127 en Premium. Un usuario Premium típico "
    "mira el doble que uno Básico. El plan contratado es el mejor diferenciador del nivel de uso "
    "que existe en el dataset."
)

# ---------------------------------------------------------------- bivariado 2
st.subheader("4 · ¿La edad influye en cuánto se mira?")

fig, ax = plt.subplots(figsize=(9, 4))
sns.scatterplot(data=datos, x="age", y="monthly_watch_time_mins", alpha=0.25, s=15, ax=ax)
ax.set_xlabel("Edad")
ax.set_ylabel("Minutos por mes")
st.pyplot(fig)

r = df["age"].corr(df["monthly_watch_time_mins"])
st.info(
    f"**Interpretación:** no hay relación: la nube de puntos no muestra ninguna tendencia y la "
    f"correlación es prácticamente nula (r = {r:.3f} en el dataset completo). Jóvenes y adultos "
    "miran lo mismo: la edad no sirve para segmentar por intensidad de uso."
)

# ---------------------------------------------------------------- multivariado
st.header("Análisis multivariado")
st.subheader("5 · Consumo por país y plan a la vez")

pivote = df.pivot_table(values="monthly_watch_time_mins", index="country",
                        columns="subscription_plan", aggfunc="median")[ORDEN_PLAN]
fig, ax = plt.subplots(figsize=(9, 4.2))
sns.heatmap(pivote, annot=True, fmt=".0f", cmap="YlGnBu", ax=ax)
ax.set_xlabel("Plan")
ax.set_ylabel("País")
st.pyplot(fig)

st.info(
    "**Interpretación:** al cruzar país, plan y consumo (mediana de minutos), el escalón "
    "Básico → Estándar → Premium se repite en los 7 países con valores muy parecidos: el efecto "
    "del plan es general y no depende del mercado. No aparecen países con comportamiento atípico, "
    "por lo que las conclusiones del proyecto valen para toda la región."
)
