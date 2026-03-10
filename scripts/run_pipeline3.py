# -------------------------------------------
# Agentic Energy Cybersecurity Pipeline
# -------------------------------------------

import sys
from pathlib import Path
import pandas as pd

# -------------------------------------------
# Enable project imports
# -------------------------------------------
sys.path.append(str(Path(__file__).resolve().parents[1]))

# -------------------------------------------
# Imports
# -------------------------------------------

# Agentic Layer
from src.agents.defense_workflow import run_agentic_defense
from src.agents.mitigation_simulator import simulate_mitigation, mitigation_result_to_dict

# Data
from src.data.loaders import load_grid_stability, load_swat
from src.data.preprocess import preprocess_grid, preprocess_swat

# Cyber Attacks
from src.attacks.inject import (
    false_data_injection,
    replay_attack,
    drift_attack,
    actuator_attack,
)

# Detection Models
from src.models.detect import detect_isolation_forest, detect_random_forest

# Evaluation
from src.eval.plots import plot_model_comparison
from src.eval.confusion_plots import save_confusion_matrix
from src.eval.ablation import run_ablation_study
from src.eval.save_tables import save_dataframe_table
from src.eval.resilience_plots import plot_mitigation_comparison, plot_ablation_study


# -------------------------------------------
# 
# -------------------------------------------
def main():
    print("=" * 60)
    print("⚡ Agentic Energy Cybersecurity Pipeline")
    print("=" * 60)

    # ---------------------------------------
    # 
    # ---------------------------------------
    print("\n[1] Loading datasets...")
    grid_df = load_grid_stability("data/raw/grid_stability/Data_for_UCI_named.csv")
    swat_df = load_swat("data/raw/swat")

    # ---------------------------------------
    # 
    # ---------------------------------------
    print("\n[2] Preprocessing datasets...")
    Xg_train, Xg_test, yg_train, yg_test = preprocess_grid(grid_df)
    Xs_train, Xs_test, ys_train, ys_test = preprocess_swat(swat_df)
    print(" Preprocessing complete")

    # ---------------------------------------
    # 
    # ---------------------------------------
    print("\n[3] Injecting cyber attacks...")
    false_data_injection(Xg_test)
    replay_attack(Xg_test)
    drift_attack(Xs_test)
    actuator_attack(Xs_test)
    print(" Attack simulation complete")

    # ---------------------------------------
    # 
    # ---------------------------------------
    print("\n[4] Training detection models...")

    print("\n=== GRID DATASET ===")
    grid_if = detect_isolation_forest(Xg_train, Xg_test, yg_test)
    grid_rf = detect_random_forest(Xg_train, Xg_test, yg_train, yg_test)

    print("\n=== SWAT DATASET ===")
    swat_if = detect_isolation_forest(Xs_train, Xs_test, ys_test)
    swat_rf = detect_random_forest(Xs_train, Xs_test, ys_train, ys_test)

    print("\n Detection complete")

    # ---------------------------------------
    # 
    # ---------------------------------------
    detection_df = pd.DataFrame([
        {"Dataset": "Grid Stability", "Model": "Isolation Forest", **grid_if},
        {"Dataset": "Grid Stability", "Model": "Random Forest", **grid_rf},
        {"Dataset": "SWaT ICS", "Model": "Isolation Forest", **swat_if},
        {"Dataset": "SWaT ICS", "Model": "Random Forest", **swat_rf},
    ])
    save_dataframe_table(detection_df, "detection_results")

    # ---------------------------------------
    # 
    # ---------------------------------------
    print("\n[5] Generating performance figures...")
    plot_model_comparison()

    # ---------------------------------------
    # 
    # ---------------------------------------
    print("\n[6] Generating confusion matrices...")

    save_confusion_matrix(
        yg_test,
        grid_rf["y_pred"],
        "Grid Dataset — Random Forest Confusion Matrix",
        "cm_grid_random_forest.pdf"
    )

    save_confusion_matrix(
        ys_test,
        swat_rf["y_pred"],
        "SWaT Dataset — Random Forest Confusion Matrix",
        "cm_swat_random_forest.pdf"
    )

    # ---------------------------------------
    # 
    # ---------------------------------------
    print("\n[7] Running Agentic AI defense workflow...")

    incident_context = {
        "dataset": "SWaT",
        "scenario": "actuator_manipulation_and_drift",
        "detection_summary": {
            "rf_accuracy": round(swat_rf["accuracy"], 4),
            "rf_f1": round(swat_rf["f1"], 4),
            "if_accuracy": round(swat_if["accuracy"], 4),
            "if_f1": round(swat_if["f1"], 4),
        },
        "affected_components": ["P101", "P201", "MV101", "MV201"],
        "observed_symptoms": [
            "unexpected actuator state changes",
            "slow telemetry drift",
            "anomalous process behavior"
        ]
    }

    run_agentic_defense("llama3.1:latest", incident_context)
    print(" Agentic AI defense workflow complete")

    # ---------------------------------------
    # 9. Autonomous Mitigation Experiments
    # ---------------------------------------
    print("\n[8] Running mitigation experiments...")

    mitigation_rows = []
    for scenario in ["fdi", "replay", "drift", "actuator"]:
        mitigation_rows.append(mitigation_result_to_dict(simulate_mitigation(scenario, False)))
        mitigation_rows.append(mitigation_result_to_dict(simulate_mitigation(scenario, True)))

    mitigation_df = pd.DataFrame(mitigation_rows)
    save_dataframe_table(mitigation_df, "mitigation_results")
    plot_mitigation_comparison(mitigation_df)

    # ---------------------------------------
    # n Study
    # ---------------------------------------
    print("\n[9] Running ablation study...")
    ablation_df = run_ablation_study()
    save_dataframe_table(ablation_df, "ablation_results")
    plot_ablation_study(ablation_df)

    # ---------------------------------------
    # 
    # ---------------------------------------
    print("\n[10] Summary")
    print(f"Grid test shape: {Xg_test.shape}")
    print(f"SWaT test shape: {Xs_test.shape}")
    print("\n Autonomous cyber-resilience pipeline finished successfully")


# -------------------------------------------
if __name__ == "__main__":
    main()