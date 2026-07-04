from pathlib import Path

import pandas as pd
import streamlit as st

st.set_page_config(page_title="Dataset", page_icon="📋", layout="wide")

ROOT = Path(__file__).resolve().parents[2]


@st.cache_data
def cargar_datos():
    return pd.read_csv(ROOT / "data" / "processed" / "streaming_users_clean.csv",
                       parse_dates=["last_login_date"])


df = cargar_datos()

st.title("📋 El dataset")

st.markdown(
    """
### Descripción general

Cada fila representa **un usuario** de la plataforma. Variables disponibles:

| Variable | Descripción |
|---|---|
| `user_id` | Identificador único del usuario |
| `age` | Edad |
| `subscription_plan` | Plan: Básico, Estándar o Premium |
| `monthly_watch_time_mins` | Minutos vistos por mes |
| `country` | País (7 países de Latinoamérica) |
| `favorite_genre` | Género favorito declarado |
| `last_login_date` | Fecha del último inicio de sesión |
| `days_since_last_login` | Días desde el último acceso (variable derivada) |
"""
)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Usuarios (final)", f"{len(df):,}".replace(",", "."))
c2.metric("Filas originales", "8.160")
c3.metric("Retención", "98 %")
c4.metric("Países", df["country"].nunique())

st.markdown(
    """
### Resumen de calidad del dataset original

El archivo original (`streaming_users_dirty.json`) presentaba:

- **160 registros duplicados** (126 filas idénticas + 34 repetidos por `user_id`).
- **Valores imposibles**: edades de -5 a 150 años, minutos negativos, el centinela 99999
  y tickets de soporte con valores -1, 99 y 150.
- **Categorías inconsistentes**: 15 formas de escribir 3 planes, 26 formas para 7 países y
  28 para 7 géneros (mayúsculas, idiomas mezclados, códigos ISO, errores de tipeo).
- **Fechas problemáticas**: dos formatos mezclados, fechas inexistentes (`31-02-2022`,
  `0000-00-00`) y futuras (`2029-01-01`).

### Transformaciones principales

1. Eliminación de duplicados (única pérdida de filas: 8.160 → 8.000).
2. Unificación de las categorías de plan, país y género a sus valores reales.
3. Valores imposibles convertidos a faltante e imputados con **medianas**
   (mediana por plan en el caso del consumo).
4. Fechas unificadas; las inválidas quedaron como faltantes sin eliminar usuarios.

El detalle completo, con la evidencia de cada decisión, está en el notebook
`02_calidad_y_limpieza.ipynb` y en el log `logs/pipeline_log.csv` del repositorio.
"""
)

st.markdown("### Vista previa del dataset procesado")
st.dataframe(df.head(50), width="stretch")

with st.expander("Ver log de transformaciones (pipeline ETL)"):
    log = pd.read_csv(ROOT / "logs" / "pipeline_log.csv")
    st.dataframe(log, width="stretch")
