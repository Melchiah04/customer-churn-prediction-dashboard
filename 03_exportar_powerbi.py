"""
Paso 3: Generar predicciones para TODOS los clientes, segmentar por riesgo,
y exportar un dataset limpio listo para conectar a Power BI.
"""
import pandas as pd
import numpy as np
import joblib

df = pd.read_csv("data/telco_churn_clean.csv")
rf = joblib.load("modelo_rf_churn.pkl")

# --- Reconstruir el mismo feature engineering que en el paso 2 ---
binary_cols = ["Partner", "Dependents", "PhoneService", "PaperlessBilling"]
for col in binary_cols:
    df[col + "_enc"] = (df[col] == "Yes").astype(int)

df["gender_enc"] = (df["gender"] == "Male").astype(int)

categorical_cols = [
    "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
    "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
    "Contract", "PaymentMethod"
]
df_enc = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# Renombrar encoded cols de vuelta a nombres esperados por el modelo
df_enc = df_enc.drop(columns=binary_cols + ["gender"])
rename_map = {c + "_enc": c for c in binary_cols + ["gender"]}
df_enc = df_enc.rename(columns=rename_map)

model_features = rf.feature_names_in_
X_full = df_enc.reindex(columns=model_features, fill_value=0)

# --- Predicción de probabilidad de churn para TODOS los clientes ---
df["Probabilidad_Churn"] = rf.predict_proba(X_full)[:, 1]

# --- Segmentación de riesgo (útil para priorizar acciones de retención) ---
def segmentar_riesgo(p):
    if p >= 0.60:
        return "Alto"
    elif p >= 0.30:
        return "Medio"
    else:
        return "Bajo"

df["Segmento_Riesgo"] = df["Probabilidad_Churn"].apply(segmentar_riesgo)

# --- Estimación de ingreso mensual en riesgo (impacto de negocio) ---
df["Ingreso_Mensual_En_Riesgo"] = np.where(
    df["Segmento_Riesgo"] == "Alto", df["MonthlyCharges"], 0
)

# --- Dataset final limpio para Power BI ---
cols_powerbi = [
    "customerID", "gender", "SeniorCitizen", "Partner", "Dependents",
    "tenure", "tenure_group", "Contract", "PaymentMethod", "InternetService",
    "MonthlyCharges", "TotalCharges", "Churn",
    "Probabilidad_Churn", "Segmento_Riesgo", "Ingreso_Mensual_En_Riesgo"
]
df_final = df[cols_powerbi].copy()
df_final["Probabilidad_Churn"] = df_final["Probabilidad_Churn"].round(4)

df_final.to_csv("churn_dashboard_dataset.csv", index=False, encoding="utf-8-sig")

# --- Tabla resumen ejecutiva (para validar antes de abrir Power BI) ---
print("=" * 60)
print("RESUMEN EJECUTIVO - LISTO PARA POWER BI")
print("=" * 60)
print(f"\nTotal clientes: {len(df_final)}")
print(f"\nDistribución por segmento de riesgo:")
print(df_final["Segmento_Riesgo"].value_counts())
print(f"\nIngreso mensual total en riesgo alto: "
      f"${df_final['Ingreso_Mensual_En_Riesgo'].sum():,.0f}")
print(f"\nTasa de churn REAL vs. probabilidad promedio predicha por segmento:")
resumen = df_final.groupby("Segmento_Riesgo").agg(
    clientes=("customerID", "count"),
    churn_real=("Churn", lambda x: (x == "Yes").mean()),
    prob_promedio=("Probabilidad_Churn", "mean")
).round(3)
print(resumen)

print(f"\n✓ Archivo exportado: churn_dashboard_dataset.csv "
      f"({len(df_final)} filas, {len(cols_powerbi)} columnas)")
