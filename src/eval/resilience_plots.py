from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd


def plot_mitigation_comparison(df: pd.DataFrame):
    out_dir = Path("outputs/figures")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Attack duration
    plt.figure(figsize=(8, 5))
    pivot = df.pivot(index="scenario", columns="with_agentic_defense", values="attack_duration_s")
    pivot.columns = ["Without Agentic Defense", "With Agentic Defense"]
    pivot.plot(kind="bar")
    plt.ylabel("Attack Duration (s)")
    plt.title("Attack Duration Before and After Agentic Defense")
    plt.tight_layout()
    plt.savefig(out_dir / "mitigation_attack_duration.pdf")
    plt.close()

    # Recovery time
    plt.figure(figsize=(8, 5))
    pivot = df.pivot(index="scenario", columns="with_agentic_defense", values="recovery_time_s")
    pivot.columns = ["Without Agentic Defense", "With Agentic Defense"]
    pivot.plot(kind="bar")
    plt.ylabel("Recovery Time (s)")
    plt.title("Recovery Time Comparison")
    plt.tight_layout()
    plt.savefig(out_dir / "mitigation_recovery_time.pdf")
    plt.close()

    # Stability score
    plt.figure(figsize=(8, 5))
    pivot = df.pivot(index="scenario", columns="with_agentic_defense", values="stability_score")
    pivot.columns = ["Without Agentic Defense", "With Agentic Defense"]
    pivot.plot(kind="bar")
    plt.ylabel("Stability Score")
    plt.title("Energy System Stability Under Attack")
    plt.tight_layout()
    plt.savefig(out_dir / "mitigation_stability_score.pdf")
    plt.close()

    print(" Mitigation comparison plots saved.")


def plot_ablation_study(df: pd.DataFrame):
    out_dir = Path("outputs/figures")
    out_dir.mkdir(parents=True, exist_ok=True)

    # Resilience score
    plt.figure(figsize=(9, 5))
    plt.bar(df["Configuration"], df["Resilience_Score"])
    plt.xticks(rotation=20, ha="right")
    plt.ylabel("Resilience Score")
    plt.title("Ablation Study: Agent Contribution to Resilience")
    plt.tight_layout()
    plt.savefig(out_dir / "ablation_resilience_score.pdf")
    plt.close()

    # Mitigation success
    plt.figure(figsize=(9, 5))
    plt.bar(df["Configuration"], df["Mitigation_Success"])
    plt.xticks(rotation=20, ha="right")
    plt.ylabel("Mitigation Success")
    plt.title("Ablation Study: Agent Contribution to Mitigation Success")
    plt.tight_layout()
    plt.savefig(out_dir / "ablation_mitigation_success.pdf")
    plt.close()

    print(" Ablation plots saved.")