import time
import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score


# ---------------------------------
# I
# ---------------------------------
def detect_isolation_forest(X_train, X_test, y_test):
    print("\n Isolation Forest Detection")

    model = IsolationForest(
        n_estimators=100,
        contamination=0.1,
        random_state=42,
        n_jobs=-1
    )

    start = time.time()
    model.fit(X_train)
    preds = model.predict(X_test)
    latency = time.time() - start

    # Convert IF labels: {-1,1} → {1,0}
    preds = np.where(preds == -1, 1, 0)

    return evaluate_results(y_test, preds, latency)


# ---------------------------------
# Random Forest 
# ---------------------------------
def detect_random_forest(X_train, X_test, y_train, y_test):
    print("\n Random Forest Detection")

    model = RandomForestClassifier(
        n_estimators=150,
        random_state=42,
        n_jobs=-1
    )

    start = time.time()
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    latency = time.time() - start

    return evaluate_results(y_test, preds, latency)


# ---------------------------------
# Evaluation Metrics
# ---------------------------------
def evaluate_results(y_true, y_pred, latency):
    acc = accuracy_score(y_true, y_pred)
    prec = precision_score(y_true, y_pred)
    rec = recall_score(y_true, y_pred)
    f1 = f1_score(y_true, y_pred)

    print(f"Accuracy : {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall   : {rec:.4f}")
    print(f"F1-score : {f1:.4f}")
    print(f"Latency  : {latency:.3f}s")

    return {
        "accuracy": acc,
        "precision": prec,
        "recall": rec,
        "f1": f1,
        "latency": latency
    }