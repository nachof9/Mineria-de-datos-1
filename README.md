# Proyecto Integrador — Minería de Datos I

## Información general

- **Integrante:** Ignacio Fonzo
- **Fecha de entrega:** Julio 2026
- **Aplicación pública:** [Streamlit Cloud](https://COMPLETAR.streamlit.app) *(completar tras el despliegue)*
- **Informe final:** [reports/informe_final.pdf](reports/informe_final.pdf)

## Objetivo del proyecto

Aplicar el proceso completo de minería de datos —inspección, calidad y limpieza, análisis
exploratorio, escalamiento y PCA— sobre un dataset de usuarios de una plataforma de streaming,
con decisiones justificadas por evidencia y trazabilidad de todas las transformaciones.
Las preguntas de análisis se definen en el notebook de inspección: distribución del consumo (P1),
consumo por plan (P2), relación edad-consumo (P3), preferencias de género por país (P4) y
posibilidad de reducir dimensionalidad (P5).

## Dataset

- **Original:** [data/raw/streaming_users_dirty.json](data/raw/streaming_users_dirty.json) — 8.160 registros, 8 variables. Se preserva sin modificaciones.
- **Procesado:** [data/processed/streaming_users_clean.csv](data/processed/streaming_users_clean.csv) — 8.000 registros, 9 variables (retención 98 %).

Cada registro representa un usuario: edad, país (7 países de Latinoamérica), plan de suscripción,
minutos vistos por mes, género favorito, fecha de último acceso y tickets de soporte.
El dataset procesado agrega la variable derivada `days_since_last_login` (recencia respecto de la
fecha de referencia 2026-07-04).

## Estructura del repositorio

- `data/raw/` — dataset original intacto · `data/processed/` — dataset final del análisis.
- `notebooks/01..05` — inspección, calidad y limpieza, EDA, PCA y conclusiones (ejecutables en orden).
- `app/` — aplicación Streamlit (Home + 4 páginas).
- `reports/informe_final.pdf` — informe final (máx. 2 páginas).
- `logs/pipeline_log.csv` — registro de transformaciones del proceso ETL.

## Preparación y calidad de datos

La evidencia se documenta en [01_inspeccion_inicial.ipynb](notebooks/01_inspeccion_inicial.ipynb) y
las decisiones en [02_calidad_y_limpieza.ipynb](notebooks/02_calidad_y_limpieza.ipynb), todas con el
esquema evidencia → decisión → impacto y registradas en [logs/pipeline_log.csv](logs/pipeline_log.csv):

1. **Duplicados:** 126 filas exactas + 34 `user_id` repetidos eliminados (única pérdida de filas).
2. **Categóricas:** 69 variantes de escritura unificadas a 3 planes, 7 países y 7 géneros;
   los 240 géneros faltantes se recategorizaron como "Desconocido".
3. **Valores imposibles:** edades fuera de [13, 100], minutos negativos, centinela 99999 y
   tickets -1/99/150 convertidos a faltante e imputados con medianas (por plan en el caso del consumo).
4. **Fechas:** dos formatos unificados; fechas inválidas y futuras a `NaT` sin eliminar filas (7,6 % final).

Retención final: **98 %** (8.160 → 8.000 filas). Ninguna fila se eliminó por faltantes.

## Resumen del análisis exploratorio

Desarrollado en [03_eda.ipynb](notebooks/03_eda.ipynb) con interpretación por visualización:

- El consumo mensual es asimétrico a la derecha: mediana ~770 min/mes con una cola de usuarios
  intensivos, por lo que el proyecto reporta medianas (P1).
- **Hallazgo principal (P2):** el consumo escala con el plan — mediana de 553 (Básico), 840
  (Estándar) y 1.127 min (Premium) — y el patrón se repite en los 7 países.
- La edad no se relaciona con el consumo (r ≈ 0,006) (P3).
- Las preferencias de género son homogéneas entre países (12–16 % por género en cada mercado) (P4).
- Las variables numéricas están incorrelacionadas entre sí (|r| < 0,02), lo que anticipa el
  resultado del PCA (P5).

## Reducción de dimensionalidad

Desarrollada en [04_pca.ipynb](notebooks/04_pca.ipynb) sobre las 4 variables numéricas de
comportamiento (edad, minutos mensuales, tickets, días desde el último acceso), estandarizadas con
`StandardScaler` por sus escalas dispares. La varianza explicada resulta casi uniforme
(~25 % por componente; 3 de 4 componentes para alcanzar el 75 %): al no existir correlación entre
las variables, **no hay redundancia que comprimir**. El resultado se documenta como hallazgo:
cada variable aporta una dimensión independiente del usuario y la segmentación útil pasa por las
categóricas (plan), no por combinaciones lineales de las numéricas.

## Visualización interactiva

Aplicación desarrollada en Streamlit y desplegada en
[Streamlit Cloud](https://COMPLETAR.streamlit.app) *(completar tras el despliegue)*.
Incluye descripción del dataset y su preparación, 5 visualizaciones de EDA con interpretación,
resultados del PCA y conclusiones para público general.

## Cómo ejecutar localmente

```bash
git clone https://github.com/nachof9/Mineria-de-datos-1.git
cd Mineria-de-datos-1
pip install -r requirements.txt
streamlit run app/Home.py
```

Los notebooks se ejecutan en orden (01 → 05); el 02 regenera el dataset procesado y el log ETL.

## Conclusiones

Detalladas en [05_conclusiones.ipynb](notebooks/05_conclusiones.ipynb) y en el
[informe final](reports/informe_final.pdf). En síntesis: el plan de suscripción es el mejor
diferenciador del consumo (un Premium típico mira el doble que un Básico, en todos los países),
mientras que edad, tickets y recencia no aportan segmentación (correlaciones nulas, confirmado por
PCA). Limitaciones: corte transversal sin dimensión temporal, 7,6 % de fechas faltantes y alcance
condicionado por las decisiones de limpieza documentadas.
