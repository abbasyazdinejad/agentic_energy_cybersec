from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay


def save_confusion_matrix(y_true, y_pred, title: str, filename: str):
    """
    Save a publication-quality confusion matrix figure
    """
    out_dir = Path("outputs/figures")
    out_dir.mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(5.5, 5))
    disp = ConfusionMatrixDisplay.from_predictions(
        y_true,
        y_pred,
        cmap="Blues",
        colorbar=False,
        ax=ax
    )

    ax.set_title(title)
    plt.tight_layout()
    plt.savefig(out_dir / filename, dpi=300)
    plt.close()

    print(f"🧩 Confusion matrix saved: {filename}")