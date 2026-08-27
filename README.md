# Predicción de Deserción de Clientes (Customer Churn) + Dashboard Ejecutivo

Proyecto de analítica predictiva end-to-end: desde datos crudos hasta un dashboard
ejecutivo accionable para un equipo de retención de clientes.

## Resumen del proyecto

Usando el dataset público de IBM Telco Customer Churn (7,043 clientes), este proyecto:

1. Limpia y explora los datos, identificando los factores más asociados a la deserción.
2. Entrena y compara dos modelos de clasificación (Regresión Logística y Random Forest).
3. Genera probabilidades de churn y segmenta a **todos** los clientes en 3 niveles de riesgo (Alto / Medio / Bajo).
4. Exporta un dataset limpio conectado a un **dashboard ejecutivo en Power BI**, con medidas DAX personalizadas, pensado para que un equipo de retención no técnico priorice acciones.

## Resultados clave

- **AUC-ROC: 0.847** con Random Forest.
- **80% de recall** en la clase Churn — el modelo detecta 8 de cada 10 clientes que realmente se van a ir.
- Los contratos **mes a mes** tienen 15 veces más deserción que los contratos a 2 años (42.7% vs 2.8%).
- El riesgo se concentra en clientes **nuevos** (0-12 meses): 47.7% de deserción en ese grupo.
- **$156,359** mensuales en ingresos concentrados en el segmento de riesgo Alto.
- La segmentación de riesgo se valida contra la tasa de churn real: 3.9% (Bajo) → 23.7% (Medio) → 62.5% (Alto) — una relación perfectamente monótona.

## Estructura del repositorio

```
├── data/
│   ├── telco_churn.csv              # Dataset original (IBM)
│   ├── telco_churn_clean.csv        # Dataset limpio (post-EDA)
├── Analisis_Prediccion_Churn.ipynb  # Notebook completo: EDA, modelado, evaluación
├── 01_eda_cleaning.py               # Script modular: limpieza y EDA
├── 02_modelo_churn.py               # Script modular: entrenamiento de modelos
├── 03_exportar_powerbi.py           # Script modular: segmentación y exportación
├── churn_dashboard_dataset.csv      # Dataset final listo para Power BI
├── modelo_rf_churn.pkl              # Modelo entrenado (serializado)
├── POWERBI_GUIDE.md                 # Guía paso a paso del dashboard + medidas DAX
└── requirements.txt                 # Dependencias del proyecto
```

## Cómo reproducir el análisis

```bash
pip install -r requirements.txt
python 01_eda_cleaning.py
python 02_modelo_churn.py
python 03_exportar_powerbi.py
```

O simplemente abre `Analisis_Prediccion_Churn.ipynb` para ver todo el proceso con explicaciones.

## Stack técnico

- **Python**: pandas, numpy, scikit-learn, joblib
- **Modelos**: Regresión Logística, Random Forest
- **Visualización final**: Power BI (medidas DAX, segmentadores, formato condicional)

## Sobre este proyecto

Lo construí para profundizar en el ciclo completo de un problema de churn — desde
la limpieza de datos hasta un entregable que un equipo de negocio realmente usaría,
conectando mi experiencia previa en análisis de KPIs e indicadores operativos con
técnicas de ciencia de datos aplicadas.

**Autor:** Juan Diego Roncancio Melo
[LinkedIn](https://linkedin.com/in/juandiegomelo)
