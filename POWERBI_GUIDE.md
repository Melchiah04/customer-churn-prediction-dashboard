# Guía: Dashboard Ejecutivo de Churn en Power BI

Este documento explica paso a paso cómo construir el dashboard en Power BI Desktop
usando el archivo `churn_dashboard_dataset.csv` generado por el análisis en Python.

## 1. Cargar los datos

1. Abre Power BI Desktop → **Obtener datos** → **Texto/CSV**.
2. Selecciona `churn_dashboard_dataset.csv`.
3. En la vista previa, verifica que Power BI detectó bien los tipos de dato:
   - `Probabilidad_Churn` → Número decimal
   - `MonthlyCharges`, `TotalCharges`, `Ingreso_Mensual_En_Riesgo` → Número decimal
   - `tenure`, `SeniorCitizen` → Número entero
   - El resto → Texto
4. Clic en **Cargar** (o **Transformar datos** si quieres revisar en Power Query primero).

## 2. Medidas DAX a crear

Ve a **Vista de Modelo** o **Vista de Datos** → botón derecho sobre la tabla → **Nueva medida**.
Crea estas medidas una por una (cópialas tal cual):

### Total de clientes
```dax
Total Clientes = COUNTROWS(churn_dashboard_dataset)
```

### Tasa de Churn Real (%)
```dax
Tasa Churn Real =
DIVIDE(
    CALCULATE(COUNTROWS(churn_dashboard_dataset), churn_dashboard_dataset[Churn] = "Yes"),
    [Total Clientes]
)
```

### Clientes en Riesgo Alto
```dax
Clientes Riesgo Alto =
CALCULATE(
    COUNTROWS(churn_dashboard_dataset),
    churn_dashboard_dataset[Segmento_Riesgo] = "Alto"
)
```

### % de Clientes en Riesgo Alto
```dax
Pct Riesgo Alto = DIVIDE([Clientes Riesgo Alto], [Total Clientes])
```

### Ingreso Mensual Total en Riesgo
```dax
Ingreso En Riesgo = SUM(churn_dashboard_dataset[Ingreso_Mensual_En_Riesgo])
```

### Ingreso Mensual Total (todos los clientes)
```dax
Ingreso Mensual Total = SUM(churn_dashboard_dataset[MonthlyCharges])
```

### Probabilidad Promedio de Churn
```dax
Prob Promedio Churn = AVERAGE(churn_dashboard_dataset[Probabilidad_Churn])
```

### Medida con variable (práctica de sintaxis DAX más avanzada)
```dax
Clasificacion Cartera =
VAR PctRiesgo = [Pct Riesgo Alto]
RETURN
    SWITCH(
        TRUE(),
        PctRiesgo >= 0.35, "Cartera Crítica",
        PctRiesgo >= 0.20, "Cartera en Alerta",
        "Cartera Saludable"
    )
```

## 3. Visuales recomendados para el dashboard

Organiza el dashboard en una sola página así:

**Fila superior — Tarjetas KPI (visual "Tarjeta")**
- Total Clientes
- Tasa Churn Real (formato %)
- Clientes en Riesgo Alto
- Ingreso en Riesgo (formato moneda)

**Fila media — Gráficos de barras**
- Gráfico de barras: `Segmento_Riesgo` (eje X) vs `Total Clientes` (valores), con color por segmento (Alto=rojo, Medio=amarillo, Bajo=verde — cámbialo manualmente en Formato → Colores de datos)
- Gráfico de barras: `Contract` (eje X) vs `Tasa Churn Real` (valores) — para mostrar el hallazgo de contrato mes a mes

**Fila inferior — Tabla de detalle**
- Tabla con: `customerID`, `tenure`, `Contract`, `MonthlyCharges`, `Probabilidad_Churn`, `Segmento_Riesgo`
- Ordenada por `Probabilidad_Churn` descendente
- Esta es la tabla que un equipo de retención usaría en la práctica para priorizar llamadas

**Filtro (segmentador / slicer)**
- Agrega un segmentador de `Segmento_Riesgo` en la parte superior para que el dashboard
  sea interactivo — al hacer clic en "Alto", todo el dashboard se filtra a esos clientes.

## 4. Formato profesional (rápido)

- Vista → Tema → elige un tema con buen contraste (o usa el tema de tu CV: azules).
- Agrega un título de texto arriba: "Dashboard de Retención de Clientes — Segmentación de Riesgo de Churn".
- En las tarjetas KPI, usa **Formato condicional** en "Clientes en Riesgo Alto" para que se pinte de rojo si supera cierto umbral — esto demuestra dominio de formato condicional, otra habilidad valorada.

## 5. Qué decir en la entrevista sobre este dashboard

- "El modelo de Random Forest identificó que el 29% de la cartera concentra el riesgo real de deserción, con $156.359 mensuales en ingresos en el segmento de alto riesgo."
- "Construí las medidas DAX desde cero, incluyendo una medida con variables (`VAR`/`RETURN`) para clasificar el estado de la cartera dinámicamente."
- "El dashboard está pensado para uso de un equipo de retención no técnico: pueden filtrar por segmento y ver de inmediato a qué clientes priorizar."

## 6. Guardar y subir a GitHub

- Guarda el archivo como `Dashboard_Churn_Retencion.pbix`.
- Como los archivos `.pbix` son binarios, no se ven en la vista previa de GitHub, pero
  igual súbelo al repositorio — lo importante es que el reclutador vea que existe y
  pueda descargarlo. Agrega 2-3 capturas de pantalla del dashboard (`.png`) al repo
  para que se vea sin necesidad de abrir el archivo.
