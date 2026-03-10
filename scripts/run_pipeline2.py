# -------------------------------------------
# Agentic Energy Cybersecurity Pipeline
# -------------------------------------------

import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.agents.defense_workflow import run_agentic_defense
from src.agents.mitigation_simulator import simulate_mitigation, mitigation_result_to_dict

from src.data.loaders import load_grid_stability, load_swat
from src.data.preprocess import preprocess_grid, preprocess_swat

from src.attacks.inject import (
    false_data_injection,
    replay_attack,
    drift_attack,
    actuator_attack,
)

from agentic_energy_cybersec.src.models.detect_o import detect_isolation_forest, detect_random_forest
from src.eval.plots import plot_model_comparison
from src.eval.ablation import run_ablation_study
from src.eval.save_tables import save_dataframe_table
from src.eval.resilience_plots import plot_mitigation_comparison, plot_ablation_study


def main():
    print("=" * 60)
    print("⚡ Agentic Energy Cybersecurity Pipeline")
    print("=" * 60)

    # 1. Load Datasets
    print("\n[1] Loading datasets...")
    grid_df = load_grid_stability("data/raw/grid_stability/Data_for_UCI_named.csv")
    swat_df = load_swat("data/raw/swat")

    # 2. Preprocess
    print("\n[2] Preprocessing datasets...")
    grid_data = preprocess_grid(grid_df)
    swat_data = preprocess_swat(swat_df)

    Xg_train, Xg_test, yg_train, yg_test = grid_data
    Xs_train, Xs_test, ys_train, ys_test = swat_data
    print(" Preprocessing complete")

    # 3. Inject Cyber Attacks
    print("\n[3] Injecting cyber attacks...")
    Xg_fdi = false_data_injection(Xg_test)
    Xg_replay = replay_attack(Xg_test)
    Xs_drift = drift_attack(Xs_test)
    Xs_actuator = actuator_attack(Xs_test)
    print("Attack simulation complete")

    # 4. Detection Models
    print("\n[4] Training detection models...")

    print("\n=== GRID DATASET ===")
    grid_if = detect_isolation_forest(Xg_train, Xg_test, yg_test)
    grid_rf = detect_random_forest(Xg_train, Xg_test, yg_train, yg_test)

    print("\n=== SWAT DATASET ===")
    swat_if = detect_isolation_forest(Xs_train, Xs_test, ys_test)
    swat_rf = detect_random_forest(Xs_train, Xs_test, ys_train, ys_test)

    print("\n Detection complete")

    # Save detection results
    detection_df = pd.DataFrame([
        {"Dataset": "Grid Stability", "Model": "Isolation Forest", **grid_if},
        {"Dataset": "Grid Stability", "Model": "Random Forest", **grid_rf},
        {"Dataset": "SWaT ICS", "Model": "Isolation Forest", **swat_if},
        {"Dataset": "SWaT ICS", "Model": "Random Forest", **swat_rf},
    ])
    save_dataframe_table(detection_df, "detection_results")

    # 
    print("\n[5] Generating figures...")
    plot_model_comparison()

    # 
    print("\n[6] Running Agentic AI defense workflow...")
    incident_context = {
        "dataset": "SWaT",
        "scenario": "actuator_manipulation_and_drift",
        "detection_summary": {
            "random_forest_accuracy": round(swat_rf["accuracy"], 4),
            "random_forest_f1": round(swat_rf["f1"], 4),
            "isolation_forest_accuracy": round(swat_if["accuracy"], 4),
            "isolation_forest_f1": round(swat_if["f1"], 4),
        },
        "affected_components": ["P101", "P201", "MV101", "MV201"],
        "observed_symptoms": [
            "unexpected actuator state changes",
            "slow telemetry drift",
            "anomalous process behavior"
        ]
    }

    run_agentic_defense(
        model_name="llama3.1:latest",
        incident_context=incident_context
    )
    print(" Agentic AI defense workflow complete")

    # 
    print("\n[7] Running mitigation experiments...")
    mitigation_rows = []
    for scenario in ["fdi", "replay", "drift", "actuator"]:
        mitigation_rows.append(mitigation_result_to_dict(simulate_mitigation(scenario, False, seed=42)))
        mitigation_rows.append(mitigation_result_to_dict(simulate_mitigation(scenario, True, seed=42)))

    mitigation_df = pd.DataFrame(mitigation_rows)
    save_dataframe_table(mitigation_df, "mitigation_results")
    plot_mitigation_comparison(mitigation_df)

    # 
    print("\n[8] Running ablation study...")
    ablation_df = run_ablation_study()
    save_dataframe_table(ablation_df, "ablation_results")
    plot_ablation_study(ablation_df)

    # 
    print("\n[9] Summary")
    print(f"Grid test shape: {Xg_test.shape}")
    print(f"SWaT test shape: {Xs_test.shape}")
    print("\n Autonomous cyber-resilience pipeline finished successfully")


if __name__ == "__main__":
    main()