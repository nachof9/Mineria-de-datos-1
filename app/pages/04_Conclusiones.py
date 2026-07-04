import streamlit as st

st.set_page_config(page_title="Conclusiones", page_icon="✅", layout="wide")

st.title("✅ Conclusiones")

st.markdown(
    """
### Hallazgos

1. **El plan de suscripción es el gran diferenciador del consumo.** La mediana de minutos
   mensuales se duplica de Básico (~553) a Premium (~1.127), y el patrón se repite en los
   7 países. Como Básico concentra el 45 % de la base, los usuarios básicos de alto consumo
   son candidatos naturales a estrategias de upgrade.
2. **El usuario típico mira ~13 horas por mes**, pero la distribución tiene una cola de usuarios
   intensivos que infla los promedios: las métricas de consumo deben reportarse con medianas.
3. **La edad no explica el consumo** (correlación ≈ 0): no conviene segmentar campañas de
   intensidad de uso por edad.
4. **Las preferencias de género son homogéneas en toda la región** (cada género representa entre
   el 12 % y el 16 % en todos los países): el catálogo no requiere diferenciación por mercado.
5. **PCA confirmó que las variables numéricas son independientes entre sí** (~25 % de varianza por
   componente): no hay redundancia que comprimir y la segmentación útil pasa por las categóricas.

### Limitaciones

- El alcance de las conclusiones está condicionado por la información disponible y por las
  decisiones de limpieza documentadas (imputaciones con mediana y recategorizaciones incluidas).
- El dataset es una foto en un momento del tiempo: no permite analizar evolución, retención ni
  causalidad (¿el plan causa mayor consumo o los usuarios intensivos eligen planes superiores?).
- Un 7,6 % de los usuarios quedó sin fecha de último acceso válida, lo que reduce la muestra del
  PCA y de los análisis de recencia.
- El género favorito es una preferencia declarada única por usuario; no refleja el consumo real
  por género.

### Próximos pasos

- Incorporar historial de visualizaciones, ingresos por usuario y fecha de alta para analizar
  retención y valor del cliente.
- Repetir el análisis con cortes periódicos del dataset para estudiar la evolución temporal.
- Probar segmentaciones que combinen variables categóricas y numéricas (clustering con distancias
  mixtas), dado que PCA sobre las numéricas no encontró estructura.

---

🔗 **Repositorio con la evidencia técnica completa:**
[github.com/nachof9/Mineria-de-datos-1](https://github.com/nachof9/Mineria-de-datos-1)
"""
)
