# Corrección: agregar gráficas de predicción

Esta versión agrega gráficas al inicio del bloque de resultados/métricas.

## Archivos modificados

1. `app.py`
   - En Random Forest se agrega `result.chart` con etiquetas y probabilidades.
   - En probabilidad/regresión se agrega `build_regression_chart()`.
   - La función `predict_linear()` ahora regresa también los datos de gráfica.

2. `templates/base.html`
   - Se agrega Chart.js desde CDN:
     `<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>`

3. `templates/random_forest.html`
   - Se agrega una gráfica de barras con las probabilidades de cada clase.
   - La gráfica aparece antes de las métricas textuales.

4. `templates/probabilidad.html`
   - Se agrega una gráfica de dispersión con datos históricos.
   - Se muestra la línea de regresión y el punto predicho.
   - La gráfica aparece antes de las métricas textuales.

5. `static/css/styles.css`
   - Se agrega estilo para `.chart-box`.

## No se modifican

- `requirements.txt`: no se agregan librerías de Python.
- Variables de entorno de Render.
- Base de datos Aiven.
- Tablas SQL.

## Pasos para aplicarlo

1. Reemplaza en GitHub los archivos modificados.
2. Haz commit y push.
3. En Render haz `Manual Deploy > Clear build cache & deploy`.
4. Prueba `/random-forest` y `/probabilidad` haciendo una predicción.

