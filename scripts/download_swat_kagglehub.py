from pathlib import Path
import shutil
import kagglehub

DATASET = "vishala28/swat-dataset-secure-water-treatment-system"

def main():
    out_dir = Path("data/raw/swat")
    out_dir.mkdir(parents=True, exist_ok=True)

    path = kagglehub.dataset_download(DATASET)
    src_dir = Path(path)

    for p in src_dir.rglob("*"):
        if p.is_file():
            shutil.copy2(p, out_dir / p.name)

    print(" SWaT downloaded to:", out_dir.resolve())

if __name__ == "__main__":
    main()