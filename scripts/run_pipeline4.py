import numpy as np
from src.agents.defense_engine import DefenseEngine
from src.eval.mitigation_metrics import evaluate_mitigation

defense = DefenseEngine()

# Example placeholders (replace with real model outputs)
anomaly_scores = np.random.rand(500)
clf_probs = np.random.rand(500)
X = np.random.randn(500, 20)

baseline_mean = np.zeros(20)
threshold_std = np.ones(20) * 2

results = []

for i in range(len(X)):
    x = X[i]
    anom = anomaly_scores[i]
    clf = clf_probs[i]

    compromised_idx, severity = defense.localize_components(
        x, baseline_mean, threshold_std
    )

    criticality = min(1.0, len(compromised_idx) / 10)
    risk = defense.compute_risk(anom, clf, criticality)
    level = defense.escalation_level(risk)

    action = defense.select_action(level, len(compromised_idx))
    action = defense.safety_check(action)

    metrics = evaluate_mitigation(
        num_compromised=len(compromised_idx),
        severity=severity,
        action=action,
        detection_delay=np.random.uniform(0.5, 2.0)
    )

    results.append([
        risk,
        level,
        len(compromised_idx),
        action,
        metrics["containment_rate"],
        metrics["recovery_time"],
        metrics["stability_score"]
    ])

results = np.array(results, dtype=object)
np.save("outputs/defense_results.npy", results)
print("Defense simulation completed.")