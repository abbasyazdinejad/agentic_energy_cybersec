import numpy as np
import matplotlib.pyplot as plt

# Load results
results = np.load("outputs/defense_results.npy", allow_pickle=True)

risk = results[:,0].astype(float)
actions = results[:,3]
containment = results[:,4].astype(float)
stability = results[:,6].astype(float)

# Color map by action
colors = {
    "monitor": "#1f77b4",            # blue
    "sanitize": "#ff7f0e",           # orange
    "rollback_and_hold": "#d62728",  # red
    "isolate_subsystem": "#9467bd"   # purple
}

point_colors = [colors.get(a, "#333333") for a in actions]

# -----------------------------
# Figure 1: Risk vs Containment
# -----------------------------
plt.figure(figsize=(4.5,3.5), dpi=300)
plt.scatter(risk, containment, c=point_colors, alpha=0.7, edgecolors='none')
plt.xlabel("Risk Score")
plt.ylabel("Containment Rate")
plt.title("Risk–Containment Relationship")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("outputs/figures/risk_vs_containment.png", bbox_inches="tight")
plt.close()

# -----------------------------
# Figure 2: Risk vs Stability
# -----------------------------
plt.figure(figsize=(4.5,3.5), dpi=300)
plt.scatter(risk, stability, c=point_colors, alpha=0.7, edgecolors='none')
plt.xlabel("Risk Score")
plt.ylabel("System Stability")
plt.title("Risk–Stability Trade-off")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("outputs/figures/risk_vs_stability.png", bbox_inches="tight")
plt.close()

print("Publication-quality figures saved.")