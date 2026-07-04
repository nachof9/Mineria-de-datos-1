import streamlit as st

st.set_page_config(page_title="Streaming LATAM — Minería de Datos I", page_icon="🎬", layout="wide")

st.title("🎬 Análisis de usuarios de una plataforma de streaming en Latinoamérica")

st.markdown(
    """
**Proyecto Integrador — Minería de Datos I**

| | |
|---|---|
| **Integrante** | Ignacio Fonzo |
| **Fecha** | Julio 2026 |

---

### Contexto

Analizamos un dataset de **8.160 registros de usuarios** de una plataforma de streaming
(edad, país, plan de suscripción, minutos vistos por mes, género favorito, último acceso y
tickets de soporte). El dataset original presentaba problemas de calidad típicos de datos reales:
duplicados, valores imposibles, categorías escritas de múltiples formas y fechas inválidas.

El proyecto recorre el proceso completo: **inspección → limpieza documentada → análisis
exploratorio → PCA → conclusiones**, con cada decisión justificada por evidencia y trazada en un
log de transformaciones.

### Qué vas a encontrar en esta aplicación

- **Dataset**: qué contiene, qué problemas tenía y cómo se preparó.
- **EDA**: cinco visualizaciones con su interpretación.
- **PCA**: qué pasa al intentar resumir el comportamiento de los usuarios en pocas dimensiones.
- **Conclusiones**: hallazgos, limitaciones y próximos pasos.

---

🔗 **Repositorio del proyecto:** [github.com/nachof9/Mineria-de-datos-1](https://github.com/nachof9/Mineria-de-datos-1)
"""
)
