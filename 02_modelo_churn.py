"""
Paso 2: Feature Engineering, entrenamiento y evaluación del modelo de churn
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report, roc_auc_score, confusion_matrix, roc_curve
)
import joblib

df = pd.read_csv("data/telco_churn_clean.csv")

# --- Feature Engineering ---
# Variables binarias Yes/No -> 1/0
binary_cols = ["Partner", "Dependents", "PhoneService", "PaperlessBilling"]
for col in binary_cols:
    df[col] = (df[col] == "Yes").astype(int)

df["gender"] = (df["gender"] == "Male").astype(int)

# Variables categóricas -> One-Hot Encoding
categorical_cols = [
    "MultipleLines", "InternetService", "OnlineSecurity", "OnlineBackup",
    "DeviceProtection", "TechSupport", "StreamingTV", "StreamingMovies",
    "Contract", "PaymentMethod"
]
df_model = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

feature_cols = [c for c in df_model.columns if c not in
                ["customerID", "Churn", "Churn_Flag", "tenure_group"]]

X = df_model[feature_cols]
y = df_model["Churn_Flag"]

print(f"Features usados en el modelo: {len(feature_cols)}")
print(f"Total de clientes: {len(X)} | Tasa de churn: {y.mean():.1%}")

# --- Split train/test ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# --- Escalado (para regresión logística) ---
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# --- Modelo 1: Regresión Logística (interpretable, buena base) ---
log_reg = LogisticRegression(max_iter=1000, random_state=42)
log_reg.fit(X_train_scaled, y_train)
y_pred_lr = log_reg.predict(X_test_scaled)
y_proba_lr = log_reg.predict_proba(X_test_scaled)[:, 1]

print("\n" + "=" * 60)
print("MODELO 1: REGRESIÓN LOGÍSTICA")
print("=" * 60)
print(classification_report(y_test, y_pred_lr, target_names=["No Churn", "Churn"]))
print(f"AUC-ROC: {roc_auc_score(y_test, y_proba_lr):.3f}")

# --- Modelo 2: Random Forest (mejor para relaciones no lineales) ---
rf = RandomForestClassifier(
    n_estimators=200, max_depth=8, min_samples_leaf=20,
    random_state=42, class_weight="balanced"
)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
y_proba_rf = rf.predict_proba(X_test)[:, 1]

print("\n" + "=" * 60)
print("MODELO 2: RANDOM FOREST")
print("=" * 60)
print(classification_report(y_test, y_pred_rf, target_names=["No Churn", "Churn"]))
print(f"AUC-ROC: {roc_auc_score(y_test, y_proba_rf):.3f}")

# --- Comparación e importancia de variables (Random Forest) ---
importances = pd.Series(rf.feature_importances_, index=feature_cols).sort_values(ascending=False)
print("\n" + "=" * 60)
print("TOP 10 VARIABLES MÁS IMPORTANTES (Random Forest)")
print("=" * 60)
print(importances.head(10).round(4))

# --- Elegir el mejor modelo por AUC ---
auc_lr = roc_auc_score(y_test, y_proba_lr)
auc_rf = roc_auc_score(y_test, y_proba_rf)
best_model, best_proba, best_name = (
    (rf, y_proba_rf, "Random Forest") if auc_rf >= auc_lr
    else (log_reg, y_proba_lr, "Regresión Logística")
)
print(f"\n✓ Mejor modelo: {best_name} (AUC={max(auc_lr, auc_rf):.3f})")

# Guardar artefactos
joblib.dump(rf, "modelo_rf_churn.pkl")
joblib.dump(scaler, "scaler.pkl")
importances.to_csv("feature_importance.csv", header=["importance"])

print("\n✓ Modelo y artefactos guardados")
