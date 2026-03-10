import numpy as np
import pandas as pd

results = np.load("outputs/defense_results.npy", allow_pickle=True)

df = pd.DataFrame(results, columns=[
    "Risk", "Level", "Compromised",
    "Action", "Containment",
    "RecoveryTime", "Stability"
])

summary = df.groupby("Action").agg({
    "Containment": "mean",
    "RecoveryTime": "mean",
    "Stability": "mean",
    "Compromised": "mean"
})

summary.to_csv("outputs/tables/mitigation_summary.csv")
print(summary)