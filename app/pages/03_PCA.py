from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

st.set_page_config(page_title="PCA", page_icon="🧭", layout="wide")
sns.set_theme(style="whitegrid")

ROOT = Path(__file__).resolve().parents[2]
VARIABLES = ["age", "monthly_watch_time_mins", "customer_support_tickets", "days_since_last_login"]


@st.cache_data
def calcular_pca():
    df = pd.read_csv(ROOT / "data" / "processed" / "streaming_users_clean.csv")
    datos = df.dropna(subset=["days_since_last_login"]).copy()
    X = StandardScaler().fit_transform(datos[VARIABLES])
    pca = PCA()
    comps = pca.fit_transform(X)
    datos["PC1"], datos["PC2"] = comps[:, 0], comps[:, 1]
    return datos, pca, len(df)


datos, pca, total = calcular_pca()

st.title("🧭 Reducción de dimensionalidad (PCA)")

n_datos = f"{len(datos):,}".replace(",", ".")
n_total = f"{total:,}".replace(",", ".")
st.markdown(
    f"""
### Variables y escalamiento

- **Variables utilizadas (4):** edad, minutos vistos por mes, tickets de soporte y días desde el
  último acceso. Son todas las numéricas de comportamiento; `user_id` se excluye por ser un
  identificador.
- **Filas utilizadas:** {n_datos} de {n_total} (se excluyen los usuarios sin fecha de
  último acceso válida, ya que PCA no admite faltantes).
- **Escalamiento:** las variables tienen escalas muy distintas (edad en decenas, minutos en miles).
  Se aplicó **StandardScaler** (media 0, desvío 1) para que ninguna domine por su escala.
"""
)

st.markdown("### Varianza explicada")

varianza = pd.DataFrame({
    "Componente": [f"PC{i+1}" for i in range(len(VARIABLES))],
    "Varianza explicada (%)": (pca.explained_variance_ratio_ * 100).round(1),
    "Acumulada (%)": (pca.explained_variance_ratio_.cumsum() * 100).round(1),
})
st.dataframe(varianza, width="stretch", hide_index=True)

fig, ax = plt.subplots(figsize=(8, 3.5))
ax.bar(varianza["Componente"], varianza["Varianza explicada (%)"], label="Individual")
ax.plot(varianza["Componente"], varianza["Acumulada (%)"], color="red", marker="o", label="Acumulada")
ax.set_ylabel("% de varianza")
ax.legend()
st.pyplot(fig)

st.info(
    "**Interpretación:** las cuatro componentes explican casi lo mismo (~25 % cada una) y hacen "
    "falta 3 de 4 para llegar al 75 %. Esto ocurre porque las variables numéricas están "
    "incorrelacionadas entre sí (|r| < 0,02): no hay información redundante que PCA pueda "
    "comprimir. El resultado es válido e informativo: cada variable aporta una dimensión propia "
    "del usuario."
)

st.markdown("### Usuarios en el plano PC1–PC2")

fig, ax = plt.subplots(figsize=(8, 4.8))
sns.scatterplot(data=datos, x="PC1", y="PC2", hue="subscription_plan",
                hue_order=["Básico", "Estándar", "Premium"], alpha=0.35, s=15, ax=ax)
st.pyplot(fig)

st.info(
    "**Interpretación:** PC1 contrasta usuarios activos (más consumo y acceso reciente) con "
    "usuarios alejados, y PC2 está dominada por los tickets de soporte. Los planes aparecen "
    "superpuestos, sin grupos separados: la diferencia de consumo por plan que encontró el EDA "
    "no alcanza para formar clusters cuando se mezcla con las otras variables independientes. "
    "**Conclusión:** la segmentación útil de estos usuarios pasa por el plan (categórica), no por "
    "combinaciones lineales de las numéricas."
)
