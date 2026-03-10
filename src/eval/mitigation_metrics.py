import numpy as np

def evaluate_mitigation(num_compromised,
                        severity,
                        action,
                        detection_delay):

    base_recovery = 20 + 2 * num_compromised + 5 * severity
    delay_penalty = 0.8 * detection_delay

    if action == "monitor":
        containment = 0.2
        disruption = 0.05
    elif action == "sanitize":
        containment = 0.6
        disruption = 0.1
    elif action == "rollback_and_hold":
        containment = 0.85
        disruption = 0.2
    else:  # isolate_subsystem
        containment = 0.95
        disruption = 0.35

    recovery_time = base_recovery + delay_penalty
    residual_risk = max(0, 1 - containment)
    stability_score = max(0, 1 - disruption)

    return {
        "containment_rate": containment,
        "recovery_time": recovery_time,
        "residual_risk": residual_risk,
        "stability_score": stability_score
    }