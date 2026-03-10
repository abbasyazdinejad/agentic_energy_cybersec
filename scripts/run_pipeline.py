# -------------------------------------------
# Agentic Energy Cybersecurity Pipeline
# -------------------------------------------

import sys
from pathlib import Path

# MUST come first — enable src imports
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.agents.defense_workflow import run_agentic_defense

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
from agentic_energy_cybersec.src.models.detect_o import detect_isolation_forest, detect_random_forest

# Evaluation / Figures
from src.eval.plots import plot_model_comparison


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
    print(" Attack simulation complete")

    # 4. Detection Models
    print("\n[4] Training detection models...")

    print("\n=== GRID DATASET ===")
    detect_isolation_forest(Xg_train, Xg_test, yg_test)
    detect_random_forest(Xg_train, Xg_test, yg_train, yg_test)

    print("\n=== SWAT DATASET ===")
    detect_isolation_forest(Xs_train, Xs_test, ys_test)
    detect_random_forest(Xs_train, Xs_test, ys_train, ys_test)
    print("\n Detection complete")

    # 5. Generate Figures
    print("\n[5] Generating figures...")
    plot_model_comparison()

    # 6. Agentic AI Defense Layer
    print("\n[6] Running Agentic AI defense workflow...")
    incident_context = {
        "dataset": "SWaT",
        "scenario": "actuator_manipulation_and_drift",
        "detection_summary": {
            "random_forest_accuracy": 0.9994,
            "random_forest_f1": 0.9924,
            "isolation_forest_accuracy": 0.9144,
            "isolation_forest_f1": 0.3896
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

    # 7. Summary
    print("\n[7] Summary")
    print(f"Grid test shape: {Xg_test.shape}")
    print(f"SWaT test shape: {Xs_test.shape}")
    print("\n End-to-end pipeline finished successfully")


if __name__ == "__main__":
    main()