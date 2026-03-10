import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

sns.set_theme(style="whitegrid", palette="deep")


def plot_model_comparison():
    data = {
        "Dataset": ["Grid", "Grid", "SWaT", "SWaT"],
        "Model": ["IF", "RF", "IF", "RF"],
        "F1": [0.129, 0.940, 0.390, 0.992],
        "Accuracy": [0.358, 0.923, 0.914, 0.999],
        "Latency": [0.108, 0.183, 0.361, 1.563],
    }

    df = pd.DataFrame(data)

    # F1 Score
    plt.figure()
    sns.barplot(data=df, x="Dataset", y="F1", hue="Model")
    plt.title("F1-score Comparison")
    plt.tight_layout()
    plt.savefig("outputs/figures/f1_comparison.pdf")

    # Accuracy
    plt.figure()
    sns.barplot(data=df, x="Dataset", y="Accuracy", hue="Model")
    plt.title("Accuracy Comparison")
    plt.tight_layout()
    plt.savefig("outputs/figures/accuracy_comparison.pdf")

    # Latency
    plt.figure()
    sns.barplot(data=df, x="Dataset", y="Latency", hue="Model")
    plt.title("Detection Latency Comparison")
    plt.tight_layout()
    plt.savefig("outputs/figures/latency_comparison.pdf")

    print("📊 Figures saved to outputs/figures/")