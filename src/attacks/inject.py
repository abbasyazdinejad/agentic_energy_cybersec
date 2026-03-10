import numpy as np
import pandas as pd


# -----------------------------
# 
# -----------------------------
def false_data_injection(X: pd.DataFrame, severity=0.2, cols_ratio=0.3):
    X_att = X.copy()

    n_cols = int(len(X.columns) * cols_ratio)
    cols = np.random.choice(X.columns, n_cols, replace=False)

    noise = np.random.normal(0, severity, size=(len(X), n_cols))
    X_att[cols] = X_att[cols] + noise

    print(f" FDI attack injected on {n_cols} features")
    return X_att


# -----------------------------
# 
# -----------------------------
def replay_attack(X: pd.DataFrame, window=500):
    X_att = X.copy()

    if len(X) <= window:
        return X_att

    start = np.random.randint(0, len(X) - window)
    X_att.iloc[start:start+window] = X_att.iloc[start-1:start+window-1].values

    print(f" Replay attack injected (window={window})")
    return X_att


# -----------------------------
# Drift Attack
# -----------------------------
def drift_attack(X: pd.DataFrame, drift_rate=0.001):
    X_att = X.copy()

    drift = np.linspace(0, drift_rate * len(X), len(X))
    for col in X.columns:
        X_att[col] = X_att[col] + drift

    print(" Drift attack injected")
    return X_att


# -----------------------------
# Actuator Manipulation
# -----------------------------
def actuator_attack(X: pd.DataFrame, cols_prefix=("P", "MV")):
    X_att = X.copy()

    actuator_cols = [c for c in X.columns if c.startswith(cols_prefix)]
    for col in actuator_cols:
        X_att[col] = np.random.choice([0, 1], size=len(X))

    print(f" Actuator attack injected on {len(actuator_cols)} features")
    return X_att