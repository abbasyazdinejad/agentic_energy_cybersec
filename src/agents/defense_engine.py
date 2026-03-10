import numpy as np

class DefenseEngine:
    def __init__(self,
                 w_anom=0.4,
                 w_clf=0.4,
                 w_crit=0.2,
                 tau_alert=0.45,
                 tau_critical=0.7):
        self.w_anom = w_anom
        self.w_clf = w_clf
        self.w_crit = w_crit
        self.tau_alert = tau_alert
        self.tau_critical = tau_critical

    # -----------------------------
    # 1. Risk Fusion
    # -----------------------------
    def compute_risk(self, anomaly_score, clf_prob, component_criticality):
        return (
            self.w_anom * anomaly_score +
            self.w_clf * clf_prob +
            self.w_crit * component_criticality
        )

    # -----------------------------
    # 2. Escalation Logic
    # -----------------------------
    def escalation_level(self, risk):
        if risk < self.tau_alert:
            return "NORMAL"
        elif risk < self.tau_critical:
            return "ALERT"
        else:
            return "CRITICAL"

    # -----------------------------
    # 3. Compromise Localization
    # -----------------------------
    def localize_components(self, x, baseline_mean, threshold_std):
        deviation = np.abs(x - baseline_mean)
        compromised = deviation > threshold_std
        compromised_idx = np.where(compromised)[0]
        severity = np.mean(deviation[compromised]) if len(compromised_idx) > 0 else 0
        return compromised_idx, severity

    # -----------------------------
    # 4. Mitigation Policy
    # -----------------------------
    def select_action(self, level, num_compromised):
        if level == "NORMAL":
            return "monitor"
        elif level == "ALERT":
            return "sanitize"
        else:
            if num_compromised > 5:
                return "isolate_subsystem"
            return "rollback_and_hold"

    # -----------------------------
    # 5. Safety Shield
    # -----------------------------
    def safety_check(self, action):
        safe_actions = [
            "monitor",
            "sanitize",
            "rollback_and_hold",
            "isolate_subsystem"
        ]
        return action if action in safe_actions else "monitor"