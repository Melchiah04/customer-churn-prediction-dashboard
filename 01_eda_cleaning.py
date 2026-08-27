"""
Proyecto: Predicción de Deserción (Churn) con Dashboard Ejecutivo
Paso 1: Carga, limpieza y análisis exploratorio de datos (EDA)
Dataset: IBM Telco Customer Churn (7,043 clientes)
"""
import pandas as pd
import numpy as np

pd.set_option("display.max_columns", None)

df = pd.read_csv("data/telco_churn.csv")

print("=" * 60)
print("INVENTARIO INICIAL")
print("=" * 60)
print(f"Filas: {df.shape[0]}, Columnas: {df.shape[1]}")
print(f"\nTipos de datos:\n{df.dtypes}")
print(f"\nValores nulos por columna:\n{df.isnull().sum()[df.isnull().sum() > 0]}")

# --- Limpieza: TotalCharges viene como texto con espacios en blanco para clientes nuevos (tenure=0) ---
print("\n" + "=" * 60)
print("HALLAZGO DE CALIDAD DE DATOS")
print("=" * 60)
blanks = df[df["TotalCharges"].str.strip() == ""]
print(f"Filas con TotalCharges vacío (texto): {len(blanks)}")
print(blanks[["customerID", "tenure", "MonthlyCharges", "TotalCharges"]].head())
print("\n-> Son clientes nuevos (tenure=0). Se imputa TotalCharges = MonthlyCharges,")
print("   ya que representan el primer mes de facturación, no un dato faltante real.")

df["TotalCharges"] = df["TotalCharges"].replace(" ", np.nan).astype(float)
df["TotalCharges"] = df["TotalCharges"].fillna(df["MonthlyCharges"])

# Variable objetivo a binaria
df["Churn_Flag"] = (df["Churn"] == "Yes").astype(int)

print("\n" + "=" * 60)
print("DISTRIBUCIÓN DE LA VARIABLE OBJETIVO (CHURN)")
print("=" * 60)
churn_rate = df["Churn_Flag"].mean()
print(f"Tasa de deserción global: {churn_rate:.1%}")
print(df["Churn"].value_counts())

print("\n" + "=" * 60)
print("DESERCIÓN POR TIPO DE CONTRATO")
print("=" * 60)
print(df.groupby("Contract")["Churn_Flag"].agg(["mean", "count"]).round(3))

print("\n" + "=" * 60)
print("DESERCIÓN POR ANTIGÜEDAD (TENURE, agrupado)")
print("=" * 60)
df["tenure_group"] = pd.cut(
    df["tenure"], bins=[0, 12, 24, 48, 72],
    labels=["0-12 meses", "13-24 meses", "25-48 meses", "49-72 meses"]
)
print(df.groupby("tenure_group", observed=True)["Churn_Flag"].agg(["mean", "count"]).round(3))

print("\n" + "=" * 60)
print("DESERCIÓN POR MÉTODO DE PAGO")
print("=" * 60)
print(df.groupby("PaymentMethod")["Churn_Flag"].agg(["mean", "count"]).round(3))

# Guardar dataset limpio para el siguiente paso
df.to_csv("data/telco_churn_clean.csv", index=False)
print("\n✓ Dataset limpio guardado en data/telco_churn_clean.csv")
